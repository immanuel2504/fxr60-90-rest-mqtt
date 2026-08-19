#!/usr/bin/env python3
"""Publish FXR-shaped tag events to the lab broker over TLS.

Stands in for a real reader so the broker and listener can be validated before
any reader configuration is touched. The payload matches the documented
`mode_tag_data_events` example in the MQTT spec — type / timestamp / data with
idHex, antenna, peakRssi, channel, phase, reads.

  py -3 fake_reader.py                            # 5 events to 127.0.0.1:8883
  py -3 fake_reader.py --count 20 --interval 0.2
  py -3 fake_reader.py --host 10.117.129.205      # over the LAN
  py -3 fake_reader.py --no-cert                  # broker must allow anonymous
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

# EPCs from the spec examples, so payloads look like real reader output.
EPCS = [
    "3005fb63ac1f3681ec880468",
    "3005fb63ac1f3681ec880469",
    "e28011606000020a1b2c3d4e",
    "3034257bf400b78000000001",
    "aabbccdd11223344556677 88".replace(" ", ""),
]


def log(*parts: object) -> None:
    print(f"[{time.strftime('%H:%M:%S')}]", *parts, flush=True)


def tag_event(index: int, mode: str) -> dict:
    epc = EPCS[index % len(EPCS)]
    return {
        "type": mode,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "data": {
            "eventNum": index + 1,
            "format": "epc",
            "idHex": epc,
            "antenna": (index % 4) + 1,
            "peakRssi": -39 - (index % 11),
            "channel": 911.75,
            "phase": 0,
            "reads": 1,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8883)
    ap.add_argument("--topic", default="site/dock01/tevents")
    ap.add_argument("--qos", type=int, default=1, choices=[0, 1])
    ap.add_argument("--count", type=int, default=5)
    ap.add_argument("--interval", type=float, default=0.5)
    ap.add_argument("--mode", default="SIMPLE",
                    help="operating mode reported in the event (default SIMPLE)")
    ap.add_argument("--client-id", default="fxr-fake-reader")
    ap.add_argument("--certs", default=CERTS)
    ap.add_argument("--retain", action="store_true", help="publish retained")
    ap.add_argument("--no-cert", action="store_true",
                    help="connect without a client certificate (should be rejected "
                         "unless the broker runs with --allow-anonymous)")
    ap.add_argument("--no-verify-hostname", action="store_true")
    args = ap.parse_args()

    ca = os.path.join(args.certs, "ca.pem")
    crt = os.path.join(args.certs, "client.crt")
    key = os.path.join(args.certs, "client.key")
    needed = (ca,) if args.no_cert else (ca, crt, key)
    for path in needed:
        if not os.path.isfile(path):
            sys.exit(f"missing {path} — run: py -3 gen_certs.py")

    state = {"published": 0, "acked": 0, "connected": False}

    def on_connect(client, userdata, flags, reason_code, properties=None):
        state["connected"] = reason_code == 0
        log(f"connected to {args.host}:{args.port} (reason {reason_code})")

    def on_publish(client, userdata, mid, reason_code=None, properties=None):
        state["acked"] += 1

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=args.client_id)
    client.on_connect = on_connect
    client.on_publish = on_publish
    if args.no_cert:
        client.tls_set(ca_certs=ca, tls_version=ssl.PROTOCOL_TLS_CLIENT)
        log("connecting WITHOUT a client certificate")
    else:
        client.tls_set(ca_certs=ca, certfile=crt, keyfile=key,
                       tls_version=ssl.PROTOCOL_TLS_CLIENT)
    if args.no_verify_hostname:
        client.tls_insecure_set(True)

    log(f"connecting to {args.host}:{args.port} ...")
    try:
        client.connect(args.host, args.port, keepalive=60)
    except Exception as exc:
        log(f"FAILED: {type(exc).__name__}: {exc}")
        return 2

    client.loop_start()

    # A TLS 1.3 client-certificate rejection is not raised by connect(); the
    # session simply never reaches CONNACK. Wait for it and fail loudly.
    deadline = time.time() + 10
    while not state["connected"] and time.time() < deadline:
        time.sleep(0.1)
    if not state["connected"]:
        log("FAILED: no CONNACK within 10s — the broker rejected the TLS session "
            "(client certificate missing, untrusted, or expired)")
        client.loop_stop()
        return 2

    try:
        for index in range(args.count):
            payload = json.dumps(tag_event(index, args.mode))
            info = client.publish(args.topic, payload, qos=args.qos,
                                  retain=args.retain)
            info.wait_for_publish(timeout=10)
            event = json.loads(payload)
            if not info.is_published():
                log(f"NOT CONFIRMED #{index + 1} -> {args.topic} "
                    f"(no broker acknowledgement within 10s)")
                continue
            state["published"] += 1
            log(f"published #{index + 1} -> {args.topic}  "
                f"idHex={event['data']['idHex']} "
                f"antenna={event['data']['antenna']} "
                f"rssi={event['data']['peakRssi']}")
            if index + 1 < args.count:
                time.sleep(args.interval)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()

    log(f"{state['published']}/{args.count} published and confirmed by broker")
    return 0 if state["published"] == args.count else 1


if __name__ == "__main__":
    sys.exit(main())
