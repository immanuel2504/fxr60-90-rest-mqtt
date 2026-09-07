#!/usr/bin/env python3
"""HTTPS receiver for the reader's `httpPost` connection type.

Accepts POSTs on any path, logs and stores each body, and always replies 200 so
the reader never has a delivery reason to retry. Runs TLS using the same lab CA
chain as the broker, so the reader can verify it.

    python3 http_post_receiver.py --port 9443

Received bodies are appended to receivers/received/http_post.log (one JSON object
per line) and the newest is also written to received/http_post_latest.json.
"""
import argparse
import datetime
import http.server
import json
import os
import ssl
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "receivers", "received")
os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(OUT, "http_post.log")
LATEST = os.path.join(OUT, "http_post_latest.json")


def stamp():
    return datetime.datetime.now().isoformat(timespec="seconds")


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _record(self, body):
        entry = {
            "received": stamp(),
            "from": self.client_address[0],
            "method": self.command,
            "path": self.path,
            "headers": dict(self.headers),
        }
        try:
            entry["body"] = json.loads(body)
        except Exception:
            entry["body_raw"] = body.decode("utf-8", "replace")

        with open(LOG, "a") as fh:
            fh.write(json.dumps(entry) + "\n")
        with open(LATEST, "w") as fh:
            json.dump(entry, fh, indent=2)
            fh.write("\n")

        preview = entry.get("body", entry.get("body_raw", ""))
        print(f"[{stamp()}] {self.command} {self.path} from {self.client_address[0]} "
              f"({len(body)} bytes)", flush=True)
        print(f"    {json.dumps(preview)[:400]}", flush=True)

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        self._record(body)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", "2")
        self.end_headers()
        self.wfile.write(b"{}")

    do_PUT = do_POST

    def do_GET(self):
        msg = b'{"status":"http_post receiver running"}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(msg)))
        self.end_headers()
        self.wfile.write(msg)

    def log_message(self, fmt, *args):
        pass  # we do our own logging


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=9443)
    ap.add_argument("--cert", default=os.path.join(BASE, "broker-certs", "broker.crt"))
    ap.add_argument("--key", default=os.path.join(BASE, "broker-certs", "broker.key"))
    ap.add_argument("--plain", action="store_true", help="serve HTTP instead of HTTPS")
    a = ap.parse_args()

    srv = http.server.ThreadingHTTPServer((a.host, a.port), Handler)
    scheme = "http"
    if not a.plain:
        if not (os.path.exists(a.cert) and os.path.exists(a.key)):
            sys.exit(f"cert/key not found: {a.cert} / {a.key}")
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(a.cert, a.key)
        srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
        scheme = "https"

    print(f"httpPost receiver on {scheme}://{a.host}:{a.port}", flush=True)
    print(f"logging to {LOG}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
