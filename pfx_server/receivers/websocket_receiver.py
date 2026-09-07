#!/usr/bin/env python3
"""WebSocket receiver for the reader's `WEBSOCKET` connection type.

Accepts connections on any path and logs every frame. TLS uses the lab CA chain,
matching the broker, so the reader can verify it.

    python3 websocket_receiver.py --port 9444           # wss
    python3 websocket_receiver.py --port 9444 --plain   # ws

Frames are appended to receivers/received/websocket.log (one JSON object per line)
and the newest is written to received/websocket_latest.json.

Note: the spec's `data_websocket` example carries no URL or endpoint field at all,
only `security`. Where the reader is meant to learn the WebSocket address is an
open question — see receivers/README.md.
"""
import argparse
import asyncio
import datetime
import json
import os
import ssl
import sys

import websockets

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "receivers", "received")
os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(OUT, "websocket.log")
LATEST = os.path.join(OUT, "websocket_latest.json")


def stamp():
    return datetime.datetime.now().isoformat(timespec="seconds")


async def handler(ws):
    peer = ws.remote_address[0] if ws.remote_address else "?"
    path = getattr(ws, "request", None)
    path = getattr(path, "path", "/") if path else "/"
    print(f"[{stamp()}] connected: {peer} path={path}", flush=True)

    try:
        async for message in ws:
            entry = {"received": stamp(), "from": peer, "path": path}
            if isinstance(message, bytes):
                entry["binary_len"] = len(message)
                entry["body_raw"] = message.decode("utf-8", "replace")
            else:
                try:
                    entry["body"] = json.loads(message)
                except Exception:
                    entry["body_raw"] = message

            with open(LOG, "a") as fh:
                fh.write(json.dumps(entry) + "\n")
            with open(LATEST, "w") as fh:
                json.dump(entry, fh, indent=2)
                fh.write("\n")

            preview = entry.get("body", entry.get("body_raw", ""))
            print(f"[{stamp()}] frame from {peer} ({len(str(message))} chars)", flush=True)
            print(f"    {json.dumps(preview)[:400]}", flush=True)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        print(f"[{stamp()}] disconnected: {peer}", flush=True)


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=9444)
    ap.add_argument("--cert", default=os.path.join(BASE, "broker-certs", "broker.crt"))
    ap.add_argument("--key", default=os.path.join(BASE, "broker-certs", "broker.key"))
    ap.add_argument("--plain", action="store_true", help="ws instead of wss")
    a = ap.parse_args()

    ctx = None
    scheme = "ws"
    if not a.plain:
        if not (os.path.exists(a.cert) and os.path.exists(a.key)):
            sys.exit(f"cert/key not found: {a.cert} / {a.key}")
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(a.cert, a.key)
        scheme = "wss"

    print(f"WEBSOCKET receiver on {scheme}://{a.host}:{a.port}", flush=True)
    print(f"logging to {LOG}", flush=True)
    async with websockets.serve(handler, a.host, a.port, ssl=ctx):
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
