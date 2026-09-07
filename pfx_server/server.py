#!/usr/bin/env python3
"""
HTTPS static file server for testing the setUpdatecertificate API.

Serves the contents of ./files over TLS so a reader can be pointed at it via
the API's `url` field. Exists to exercise the API's authentication and
transfer-failure handling, so it can present several auth modes and can be
told to fail or stall on purpose.

Auth modes (--auth), covering the header-based mechanisms the API can use:

    none      no authentication
    basic     HTTP Basic; needs PFX_USER and PFX_PASS
    bearer    Authorization: Bearer <token>; needs PFX_TOKEN
    any       accept Basic or Bearer, whichever the client sends

Mutual TLS (--mtls) is a separate axis and combines with any of the above,
so the six interesting combinations are reachable from one script:

    python3 server.py --auth none
    python3 server.py --auth basic
    python3 server.py --auth bearer
    python3 server.py --auth basic --mtls
    python3 server.py --auth bearer --mtls
    python3 server.py --auth none --mtls

Note that --mtls rejects unauthorised clients during the TLS handshake, so
a failure surfaces as a connection error rather than an HTTP status.

Fault injection (--test-mode) makes the API's `retry` and `timeouts` fields
testable by giving the download something to recover from:

    /fail/<n>/<path>     500 for the first n requests, then serve normally
    /slow/<seconds>/<path>   send headers, then trickle the body
    /hang/<seconds>      accept the request and never respond
    /reset-faults        clear the /fail counters

Credentials come from the environment; there are no defaults, so the server
refuses to start without the ones its mode requires:

    export PFX_USER=someone
    export PFX_PASS='a-long-random-password'
    export PFX_TOKEN='a-long-random-token'
"""

import argparse
import base64
import hmac
import html
import http.server
import io
import os
import posixpath
import re
import socketserver
import ssl
import sys
import threading
import time
import urllib.parse
import uuid
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REALM = "PFX Download"

# /fail/<n>/... needs to remember how many times each path has been hit, and
# the server is threaded, so the counters need a lock.
_fault_hits = {}
_fault_lock = threading.Lock()

FAIL_RE = re.compile(r"^/fail/(\d+)(/.*)$")
SLOW_RE = re.compile(r"^/slow/(\d+)(/.*)$")
HANG_RE = re.compile(r"^/hang/(\d+)/?$")


class AuthenticatedHandler(http.server.SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler with selectable authentication."""

    server_version = "PfxServer/2.0"
    # Force .pfx/.p12 to download rather than render as text.
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".pfx": "application/x-pkcs12",
        ".p12": "application/x-pkcs12",
        ".cer": "application/pkix-cert",
        ".crt": "application/x-x509-ca-cert",
        ".pem": "application/x-pem-file",
    }

    # ---------------------------------------------------------------- auth

    def _check_basic(self, credentials):
        try:
            decoded = base64.b64decode(credentials, validate=True).decode("utf-8")
        except Exception:
            return False
        user, sep, password = decoded.partition(":")
        if not sep:
            return False
        # compare_digest on both fields, unconditionally, to avoid leaking
        # which half was wrong via timing. Encode first: the str form rejects
        # non-ASCII with a TypeError, which would turn a bad username into a
        # 500 instead of a 401.
        user_ok = hmac.compare_digest(
            user.encode("utf-8"), self.server.auth_user.encode("utf-8")
        )
        pass_ok = hmac.compare_digest(
            password.encode("utf-8"), self.server.auth_pass.encode("utf-8")
        )
        return user_ok and pass_ok

    def _check_bearer(self, token):
        return hmac.compare_digest(
            token.strip().encode("utf-8"), self.server.auth_token.encode("utf-8")
        )

    def _authenticated(self):
        mode = self.server.auth_mode
        if mode == "none":
            return True

        header = self.headers.get("Authorization", "")
        scheme, _, credentials = header.partition(" ")
        scheme = scheme.lower()

        if mode in ("basic", "any") and scheme == "basic":
            return self._check_basic(credentials)
        if mode in ("bearer", "any") and scheme == "bearer":
            return self._check_bearer(credentials)
        return False

    def _request_auth(self):
        self.send_response(401)
        # Advertise whichever schemes this mode actually accepts, so a client
        # that inspects the challenge picks a scheme the server will honour.
        if self.server.auth_mode in ("basic", "any"):
            self.send_header(
                "WWW-Authenticate", f'Basic realm="{REALM}", charset="UTF-8"'
            )
        if self.server.auth_mode in ("bearer", "any"):
            self.send_header("WWW-Authenticate", f'Bearer realm="{REALM}"')
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _log_client(self):
        """Record what the client presented.

        Observing what the reader actually sends is most of the point of this
        server, so log the auth scheme and, under mTLS, the peer subject.
        The credentials themselves are deliberately not logged.
        """
        header = self.headers.get("Authorization", "")
        scheme = header.partition(" ")[0] or "<none>"
        detail = f"auth={scheme}"
        try:
            peer = self.connection.getpeercert()
        except (AttributeError, ValueError):
            peer = None
        if peer:
            subject = dict(
                x[0] for x in peer.get("subject", ()) if x
            ).get("commonName", "?")
            detail += f" peer_cn={subject}"
        self.log_message("%s %s (%s)", self.command, self.path, detail)

    def _guard(self):
        """Return True if the request may proceed."""
        self._log_client()
        if self._authenticated():
            return True
        self.log_message("AUTH FAILED for %s", self.path)
        self._request_auth()
        return False

    # ------------------------------------------------------ fault injection

    def _handle_faults(self):
        """Apply any fault-injection prefix on self.path.

        Returns True if the request was fully handled here and the caller
        should stop. Rewrites self.path to strip the prefix otherwise.
        """
        if not self.server.test_mode:
            return False

        path = self.path.split("?", 1)[0]

        if path.rstrip("/") == "/reset-faults":
            with _fault_lock:
                _fault_hits.clear()
            self._send_text(200, "fault counters reset\n")
            return True

        m = HANG_RE.match(path)
        if m:
            seconds = min(int(m.group(1)), 3600)
            self.log_message("FAULT hang %ss", seconds)
            time.sleep(seconds)
            # Close without responding, so the client hits its own timeout.
            self.close_connection = True
            return True

        m = FAIL_RE.match(path)
        if m:
            limit, rest = int(m.group(1)), m.group(2)
            key = f"fail:{rest}"
            with _fault_lock:
                seen = _fault_hits.get(key, 0) + 1
                _fault_hits[key] = seen
            if seen <= limit:
                self.log_message(
                    "FAULT fail %s (attempt %d of %d, returning 500)", rest, seen, limit
                )
                self._send_text(500, "injected failure\n")
                return True
            self.log_message(
                "FAULT fail %s (attempt %d, limit passed, serving)", rest, seen
            )
            self.path = rest
            return False

        m = SLOW_RE.match(path)
        if m:
            self.server_slow_seconds = min(int(m.group(1)), 3600)
            self.path = m.group(2)
            return False

        return False

    def _send_text(self, code, message):
        encoded = message.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(encoded)

    def _send_slowly(self, seconds):
        """Serve the current path, trickling the body over `seconds`."""
        path = self.translate_path(self.path)
        if os.path.isdir(path) or not os.path.isfile(path):
            self.send_error(404, "File not found")
            return
        try:
            with open(path, "rb") as handle:
                data = handle.read()
        except OSError:
            self.send_error(404, "File not found")
            return

        self.send_response(200)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if self.command == "HEAD":
            return

        # Ten chunks spread over the requested window, so a read timeout
        # shorter than `seconds` fires part-way through the body.
        chunks = 10
        size = max(1, len(data) // chunks)
        delay = seconds / chunks
        self.log_message("FAULT slow %s over %ss", self.path, seconds)
        for start in range(0, len(data), size):
            try:
                self.wfile.write(data[start : start + size])
                self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                self.log_message("FAULT slow %s aborted by client", self.path)
                return
            time.sleep(delay)

    # --------------------------------------------------------- HTTP methods

    def _serve(self, method):
        self.server_slow_seconds = 0
        if not self._guard():
            return
        if self._handle_faults():
            return
        if self.server_slow_seconds:
            self._send_slowly(self.server_slow_seconds)
            return
        method()

    def do_GET(self):
        self._serve(super().do_GET)

    def do_HEAD(self):
        self._serve(super().do_HEAD)

    # ------------------------------------------------------------ filesystem

    def translate_path(self, path):
        """Map a URL path to a file inside the served directory.

        SimpleHTTPRequestHandler resolves against the process cwd; anchor to
        the configured directory instead so the server does not depend on
        where it was launched from.
        """
        path = path.split("?", 1)[0].split("#", 1)[0]
        trailing_slash = path.rstrip().endswith("/")
        path = posixpath.normpath(urllib.parse.unquote(path))
        words = [w for w in path.split("/") if w and w not in (os.curdir, os.pardir)]
        result = self.server.serve_dir
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            result = os.path.join(result, word)

        # Stripping '..' above stops traversal via the URL, but a symlink
        # inside the served directory could still point outside it. Resolve
        # and confine.
        root = self.server.serve_dir_real
        resolved = os.path.realpath(result)
        if resolved != root and not resolved.startswith(root + os.sep):
            self.log_message("BLOCKED path escapes served dir: %s", result)
            # Point at a name that cannot exist, so the normal not-found path
            # produces a clean 404. A NUL byte would raise ValueError out of
            # open() instead, which drops the connection. The uuid keeps this
            # from colliding with a real file someone happens to have added.
            return os.path.join(root, f"__blocked__{uuid.uuid4().hex}")

        if trailing_slash:
            resolved += "/"
        return resolved

    def list_directory(self, path):
        """Render a plain listing; suppress dotfiles."""
        try:
            names = sorted(
                (n for n in os.listdir(path) if not n.startswith(".")),
                key=str.lower,
            )
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None

        display = html.escape(self.path, quote=False)
        rows = []

        # A parent link, so subdirectories are navigable without the URL bar.
        if self.path.rstrip("/"):
            rows.append(
                "<tr><td><a href='..'>../</a></td><td>-</td><td>-</td></tr>"
            )

        for name in names:
            full = os.path.join(path, name)
            link = name
            label = name
            if os.path.isdir(full):
                link += "/"
                label += "/"
                size = "-"
            else:
                size = f"{os.path.getsize(full):,} bytes"
            mtime = datetime.fromtimestamp(os.path.getmtime(full)).strftime(
                "%Y-%m-%d %H:%M"
            )
            rows.append(
                "<tr><td><a href='{}'>{}</a></td><td>{}</td><td>{}</td></tr>".format(
                    urllib.parse.quote(link), html.escape(label, quote=False), size, mtime
                )
            )

        body = """<!doctype html>
<html><head><meta charset="utf-8"><title>Index of {d}</title>
<style>
 body {{ font-family: system-ui, sans-serif; margin: 2rem; }}
 table {{ border-collapse: collapse; }}
 th, td {{ text-align: left; padding: .35rem 1.25rem .35rem 0;
          border-bottom: 1px solid #ddd; }}
 th {{ font-size: .8rem; text-transform: uppercase; color: #666; }}
 td:nth-child(2) {{ font-variant-numeric: tabular-nums; }}
 .mode {{ color: #666; font-size: .85rem; }}
</style></head><body>
<h2>Index of {d}</h2>
<p class="mode">auth: {auth}{mtls}{test}</p>
<table><tr><th>Name</th><th>Size</th><th>Modified</th></tr>
{rows}
</table>
{empty}
</body></html>""".format(
            d=display,
            auth=self.server.auth_mode,
            mtls=" + mTLS" if self.server.mtls else "",
            test=" | fault injection enabled" if self.server.test_mode else "",
            rows="\n".join(rows),
            empty="<p><em>Directory is empty.</em></p>" if not names else "",
        )

        encoded = body.encode("utf-8", "surrogateescape")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return io.BytesIO(encoded)


class ThreadedHTTPSServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    # Allow rebinding straight after a restart.
    allow_reuse_address = True

    def get_request(self):
        """Accept a client without blocking the listener on its TLS handshake."""
        request, client_address = super().get_request()
        return (
            self.ssl_context.wrap_socket(
                request, server_side=True, do_handshake_on_connect=False
            ),
            client_address,
        )

    def handle_error(self, request, client_address):
        """Keep TLS handshake rejections from dumping a traceback.

        Under --mtls a client without a valid certificate is refused during
        the handshake, which is expected rather than exceptional.
        """
        exc = sys.exc_info()[1]
        if isinstance(exc, ssl.SSLError):
            print(f"TLS handshake failed from {client_address[0]}: {exc.reason}")
            return
        super().handle_error(request, client_address)


def main():
    parser = argparse.ArgumentParser(
        description="HTTPS file server for setUpdatecertificate testing.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8443)
    parser.add_argument(
        "--auth",
        choices=("none", "basic", "bearer", "any"),
        default="basic",
        help="authentication mode (default: basic)",
    )
    parser.add_argument(
        "--mtls",
        action="store_true",
        help="require a client certificate signed by --ca",
    )
    parser.add_argument(
        "--ca",
        default=os.path.join(BASE_DIR, "ca", "ca.crt"),
        help="CA used to verify client certificates under --mtls",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="enable /fail, /slow and /hang fault injection",
    )
    parser.add_argument(
        "--dir",
        default=os.path.join(BASE_DIR, "files"),
        help="directory to serve (default: ./files)",
    )
    parser.add_argument("--cert", default=os.path.join(BASE_DIR, "cert.pem"))
    parser.add_argument("--key", default=os.path.join(BASE_DIR, "key.pem"))
    args = parser.parse_args()

    user = os.environ.get("PFX_USER")
    password = os.environ.get("PFX_PASS")
    token = os.environ.get("PFX_TOKEN")

    if args.auth in ("basic", "any") and (not user or not password):
        sys.exit(
            f"error: --auth {args.auth} needs PFX_USER and PFX_PASS.\n"
            "  export PFX_USER=someone\n"
            "  export PFX_PASS='a-long-random-password'"
        )
    if args.auth in ("bearer", "any") and not token:
        sys.exit(
            f"error: --auth {args.auth} needs PFX_TOKEN.\n"
            "  export PFX_TOKEN='a-long-random-token'"
        )

    serve_dir = os.path.abspath(args.dir)
    if not os.path.isdir(serve_dir):
        sys.exit(f"error: not a directory: {serve_dir}")
    for f in (args.cert, args.key):
        if not os.path.isfile(f):
            sys.exit(f"error: missing TLS file: {f}")
    if args.mtls and not os.path.isfile(args.ca):
        sys.exit(f"error: missing CA file for --mtls: {args.ca}")

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(certfile=args.cert, keyfile=args.key)
    if args.mtls:
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile=args.ca)

    httpd = ThreadedHTTPSServer((args.host, args.port), AuthenticatedHandler)
    httpd.auth_mode = args.auth
    httpd.auth_user = user or ""
    httpd.auth_pass = password or ""
    httpd.auth_token = token or ""
    httpd.mtls = args.mtls
    httpd.test_mode = args.test_mode
    httpd.serve_dir = serve_dir
    httpd.serve_dir_real = os.path.realpath(serve_dir)
    httpd.ssl_context = context

    print(f"serving {serve_dir}")
    print(f"listening on https://{args.host}:{args.port}/")
    print(f"auth mode: {args.auth}" + (" + mTLS" if args.mtls else ""))
    if args.auth in ("basic", "any"):
        print(f"  basic user: {user}")
    if args.auth in ("bearer", "any"):
        print("  bearer token: from PFX_TOKEN")
    if args.mtls:
        print(f"  client certs verified against: {args.ca}")
    if args.test_mode:
        print("fault injection enabled: /fail/<n>/<path>, /slow/<s>/<path>, /hang/<s>")
    print("Ctrl-C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
