#!/usr/bin/env python3
"""Subscribe to the lab broker over TLS and print everything that arrives.

This is the stand-in for whatever consumes reader data — it proves the broker
side works before an actual FXR reader is pointed at it.

  py -3 listener.py                                  # 127.0.0.1:8883
  py -3 listener.py --host 10.117.129.205            # over the LAN
  py -3 listener.py --topic 'site/dock01/#'
  py -3 listener.py --count 5                        # exit after 5 messages

Identity comes from certs/client.crt + client.key; the broker is validated
against certs/ca.pem. That mirrors the FXR `security` block:
CACertificateFileLocation / privateKeyFileLocation / publicKeyFileLocation.
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import time

try:
    import paho.mqtt.client as mqtt
except ImportError:
    sys.exit("paho-mqtt is required:  py -3 -m pip install paho-mqtt")

HERE = os.path.dirname(os.path.abspath(__file__))
CERTS = os.path.join(HERE, "certs")


def log(*parts: object) -> None:
    print(f"[{time.strftime('%H:%M:%S')}]", *parts, flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8883)
    ap.add_argument("--topic", default="site/dock01/tevents")
    ap.add_argument("--qos", type=int, default=1, choices=[0, 1])
    ap.add_argument("--client-id", default="lab-listener")
    ap.add_argument("--certs", default=CERTS)
    ap.add_argument("--count", type=int, default=0,
                    help="exit after this many messages (0 = run until Ctrl+C)")
    ap.add_argument("--timeout", type=float, default=0,
                    help="exit after this many seconds (0 = no limit)")
    ap.add_argument("--no-verify-hostname", action="store_true",
                    help="skip hostname/SAN check (the verifyHostName:false case)")
    ap.add_argument("--raw", action="store_true", help="do not pretty-print JSON")
    args = ap.parse_args()

    ca = os.path.join(args.certs, "ca.pem")
    crt = os.path.join(args.certs, "client.crt")
    key = os.path.join(args.certs, "client.key")
    for path in (ca, crt, key):
        if not os.path.isfile(path):
            sys.exit(f"missing {path} — run: py -3 gen_certs.py")

    state = {"messages": 0, "connected": False}

    def on_connect(client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            state["connected"] = True
            log(f"connected to {args.host}:{args.port} (TLS, mutual auth)")
            client.subscribe(args.topic, qos=args.qos)
        else:
            log(f"connect refused: {reason_code}")

    def on_subscribe(client, userdata, mid, reason_codes, properties=None):
        log(f"subscribed to {args.topic!r} (qos {args.qos})")

    def on_message(client, userdata, msg):
        state["messages"] += 1
        body = msg.payload.decode("utf-8", "replace")
        if not args.raw:
            try:
                body = json.dumps(json.loads(body), indent=2)
            except json.JSONDecodeError:
                pass
        log(f"#{state['messages']} {msg.topic} (qos {msg.qos}"
            f"{', retained' if msg.retain else ''})")
        print(body, flush=True)
        if args.count and state["messages"] >= args.count:
            client.disconnect()

    def on_disconnect(client, userdata, flags, reason_code=None, properties=None):
        log(f"disconnected ({reason_code})")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=args.client_id)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.tls_set(ca_certs=ca, certfile=crt, keyfile=key,
                   tls_version=ssl.PROTOCOL_TLS_CLIENT)
    if args.no_verify_hostname:
        client.tls_insecure_set(True)
        log("hostname verification disabled")

    log(f"connecting to {args.host}:{args.port} ...")
    try:
        client.connect(args.host, args.port, keepalive=60)
    except Exception as exc:
        log(f"FAILED: {type(exc).__name__}: {exc}")
        return 2

    started = time.time()
    try:
        client.loop_start()
        while True:
            time.sleep(0.2)
            if args.count and state["messages"] >= args.count:
                break
            if args.timeout and time.time() - started > args.timeout:
                log(f"timeout after {args.timeout}s")
                break
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()

    log(f"{state['messages']} message(s) received")
    return 0 if state["messages"] or not args.count else 1


if __name__ == "__main__":
    sys.exit(main())
