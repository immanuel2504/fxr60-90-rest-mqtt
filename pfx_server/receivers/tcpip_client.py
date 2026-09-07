#!/usr/bin/env python3
"""Client for the reader's `tcpip-server` connection type.

Important: for this type the **reader** is the server. Its spec example carries a
`tcpipport` but no hostname, which means the reader opens a listening socket on
that port and we connect *to it* — the opposite of the other connection types.

    python3 tcpip_client.py --host 10.233.48.36 --port 8081

Also runs a local listener, in case the reader turns out to connect outward
instead — which would contradict the field naming but is worth being able to test:

    python3 tcpip_client.py --listen --port 8081

Received data is appended to receivers/received/tcpip.log and the newest payload
is written to received/tcpip_latest.json.
"""
import argparse
import datetime
import json
import os
import socket
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "receivers", "received")
os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(OUT, "tcpip.log")
LATEST = os.path.join(OUT, "tcpip_latest.json")


def stamp():
    return datetime.datetime.now().isoformat(timespec="seconds")


def record(peer, data):
    entry = {"received": stamp(), "from": peer, "bytes": len(data)}
    text = data.decode("utf-8", "replace")
    try:
        entry["body"] = json.loads(text)
    except Exception:
        entry["body_raw"] = text

    with open(LOG, "a") as fh:
        fh.write(json.dumps(entry) + "\n")
    with open(LATEST, "w") as fh:
        json.dump(entry, fh, indent=2)
        fh.write("\n")

    preview = entry.get("body", entry.get("body_raw", ""))
    print(f"[{stamp()}] {len(data)} bytes from {peer}", flush=True)
    print(f"    {json.dumps(preview)[:400]}", flush=True)


def connect(host, port, timeout):
    print(f"connecting to reader at {host}:{port} ...", flush=True)
    try:
        s = socket.create_connection((host, port), timeout=timeout)
    except OSError as e:
        sys.exit(f"could not connect: {e}\n"
                 f"The reader only listens once a tcpip-server connection is configured.")
    print(f"connected. logging to {LOG}", flush=True)
    s.settimeout(None)
    buf = b""
    with s:
        while True:
            chunk = s.recv(65536)
            if not chunk:
                print("reader closed the connection", flush=True)
                return
            buf += chunk
            # tag data tends to arrive newline-delimited; fall back to raw chunks
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                if line.strip():
                    record(f"{host}:{port}", line)
            if len(buf) > 1_000_000:
                record(f"{host}:{port}", buf)
                buf = b""


def listen(host, port):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, port))
    srv.listen(5)
    print(f"listening on {host}:{port} (in case the reader connects outward)", flush=True)
    print(f"logging to {LOG}", flush=True)
    while True:
        conn, addr = srv.accept()
        peer = f"{addr[0]}:{addr[1]}"
        print(f"[{stamp()}] connection from {peer}", flush=True)
        with conn:
            buf = b""
            while True:
                chunk = conn.recv(65536)
                if not chunk:
                    break
                buf += chunk
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    if line.strip():
                        record(peer, line)
            if buf.strip():
                record(peer, buf)
        print(f"[{stamp()}] {peer} disconnected", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="10.233.48.36",
                    help="reader address (client mode) or bind address (--listen)")
    ap.add_argument("--port", type=int, default=8081)
    ap.add_argument("--timeout", type=float, default=15)
    ap.add_argument("--listen", action="store_true",
                    help="listen locally instead of connecting to the reader")
    a = ap.parse_args()

    if a.listen:
        listen("0.0.0.0" if a.host == "10.233.48.36" else a.host, a.port)
    else:
        connect(a.host, a.port, a.timeout)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
