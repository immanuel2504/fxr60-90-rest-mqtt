#!/usr/bin/env python3
"""Generate the CA, broker, and client certificates for the MQTT TLS lab.

Same steps as Phases A-C of the lab notes, but driven from Python so it behaves
identically in Git Bash, PowerShell, and cmd (no MSYS_NO_PATHCONV needed, no
path rewriting of -subj).

  py -3 gen_certs.py                      # SAN gets the auto-detected LAN IP
  py -3 gen_certs.py --san-ip 10.117.129.205
  py -3 gen_certs.py --reader-ip 10.233.46.162   # detect the IP that routes there
  py -3 gen_certs.py --force              # overwrite existing certs

Produces, in ./certs:

  ca.key   ca.crt   ca.pem        CA (ca.pem is a copy of ca.crt)
  server.key  server.csr  server.crt   broker, SAN = LAN IP + 127.0.0.1 + localhost
  client.key  client.csr  client.crt  client.pem   client / reader identity

The SAN matters: a broker certificate whose SAN is only 127.0.0.1 cannot be
validated by anything off this PC, so an FXR reader with verifyHostName: true
will fail the handshake.
"""

from __future__ import annotations

import argparse
import os
import shutil
import socket
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CERTS = os.path.join(HERE, "certs")

CA_DAYS = 3650
LEAF_DAYS = 365
KEY_BITS = 2048


def run(*cmd: str) -> None:
    print("  $ " + " ".join(cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"openssl failed ({proc.returncode}):\n{proc.stderr.strip()}")


def detect_lan_ip(toward: str) -> str:
    """The local address the OS would use to reach `toward` — no traffic sent."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect((toward, 80))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--san-ip", help="IP to put in the broker certificate SAN")
    ap.add_argument("--reader-ip", default="10.233.46.162",
                    help="used only to auto-detect which local IP faces the reader")
    ap.add_argument("--org", default="Zebra", help="O= in the subject (default: Zebra)")
    ap.add_argument("--country", default="IN", help="C= in the subject (default: IN)")
    ap.add_argument("--ca-cn", default="ZebraRootCA")
    ap.add_argument("--broker-cn", default="mqtt-broker")
    ap.add_argument("--client-cn", default="fxr-reader-01")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    args = ap.parse_args()

    if not shutil.which("openssl"):
        sys.exit("openssl not found on PATH")

    san_ip = args.san_ip or detect_lan_ip(args.reader_ip)
    os.makedirs(CERTS, exist_ok=True)
    os.chdir(CERTS)

    existing = [f for f in ("ca.key", "server.key", "client.key") if os.path.exists(f)]
    if existing and not args.force:
        sys.exit(f"{', '.join(existing)} already exist in {CERTS}\n"
                 f"Pass --force to regenerate (this invalidates every cert already "
                 f"deployed from this CA).")

    subj = f"/C={args.country}/O={args.org}/CN="

    print(f"\nPhase A - CA ({args.ca_cn})")
    run("openssl", "genrsa", "-out", "ca.key", str(KEY_BITS))
    run("openssl", "req", "-x509", "-new", "-nodes", "-key", "ca.key", "-sha256",
        "-days", str(CA_DAYS), "-out", "ca.crt", "-subj", subj + args.ca_cn)
    shutil.copyfile("ca.crt", "ca.pem")
    print("  ca.key, ca.crt, ca.pem")

    print(f"\nPhase B - broker ({args.broker_cn}), SAN IP {san_ip}")
    run("openssl", "genrsa", "-out", "server.key", str(KEY_BITS))
    run("openssl", "req", "-new", "-key", "server.key", "-out", "server.csr",
        "-subj", subj + args.broker_cn)
    # 127.0.0.1 and localhost stay in the list so anything running on this PC
    # keeps working alongside the reader.
    san = f"subjectAltName=IP:{san_ip},IP:127.0.0.1,DNS:localhost\n"
    if san_ip == "127.0.0.1":
        san = "subjectAltName=IP:127.0.0.1,DNS:localhost\n"
        print("  WARNING: no LAN IP detected; this cert will only work on this PC")
    with open("san.ext", "w", encoding="utf-8") as fh:
        fh.write("basicConstraints=CA:FALSE\n")
        fh.write("keyUsage=digitalSignature,keyEncipherment\n")
        fh.write("extendedKeyUsage=serverAuth\n")
        fh.write(san)
    run("openssl", "x509", "-req", "-in", "server.csr", "-CA", "ca.crt",
        "-CAkey", "ca.key", "-CAcreateserial", "-out", "server.crt",
        "-days", str(LEAF_DAYS), "-sha256", "-extfile", "san.ext")
    print("  server.key, server.csr, server.crt, san.ext")

    print(f"\nPhase C - client ({args.client_cn})")
    run("openssl", "genrsa", "-out", "client.key", str(KEY_BITS))
    run("openssl", "req", "-new", "-key", "client.key", "-out", "client.csr",
        "-subj", subj + args.client_cn)
    with open("client.ext", "w", encoding="utf-8") as fh:
        fh.write("basicConstraints=CA:FALSE\n")
        fh.write("keyUsage=digitalSignature,keyEncipherment\n")
        fh.write("extendedKeyUsage=clientAuth\n")
    run("openssl", "x509", "-req", "-in", "client.csr", "-CA", "ca.crt",
        "-CAkey", "ca.key", "-CAcreateserial", "-out", "client.crt",
        "-days", str(LEAF_DAYS), "-sha256", "-extfile", "client.ext")
    # The FXR config field publicKeyFileLocation expects a .pem name.
    shutil.copyfile("client.crt", "client.pem")
    print("  client.key, client.csr, client.crt, client.pem")

    print("\nVerify")
    for cmd in (
        ("openssl", "x509", "-in", "ca.crt", "-noout", "-subject"),
        ("openssl", "x509", "-in", "server.crt", "-noout", "-subject", "-ext",
         "subjectAltName"),
        ("openssl", "x509", "-in", "client.crt", "-noout", "-subject"),
        ("openssl", "verify", "-CAfile", "ca.crt", "server.crt"),
        ("openssl", "verify", "-CAfile", "ca.crt", "client.crt"),
    ):
        out = subprocess.run(cmd, capture_output=True, text=True)
        print("  " + (out.stdout or out.stderr).strip().replace("\n", "\n  "))

    print(f"\nCerts in {CERTS}")
    print(f"Broker will be reachable at {san_ip}:8883 — use that as `hostName` "
          f"in the reader's endpoint config.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
