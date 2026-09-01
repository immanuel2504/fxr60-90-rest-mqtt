#!/usr/bin/env python3
"""Run FXR REST and/or MQTT live tests from one entry point.

REST wraps test_rest_api.py (HTTPS to the reader).
MQTT wraps test_mqtt_api.py (commands through a broker).

Default tier is read-only for both (GET / get_*). Write and danger tiers
are opt-in and can change reader state.

Usage
-----
  python test_all_apis.py --list

  python test_all_apis.py rest
  python test_all_apis.py rest --only "/cloud/status"

  python test_all_apis.py mqtt
  python test_all_apis.py mqtt --only get_status

  python test_all_apis.py both --only status
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REST = os.path.join(HERE, "test_rest_api.py")
MQTT = os.path.join(HERE, "test_mqtt_api.py")


def parse_args(argv=None):
    ap = argparse.ArgumentParser(
        description="Test FXR REST and MQTT APIs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Usage\n-----\n")[-1],
    )
    ap.add_argument(
        "api",
        nargs="?",
        default="both",
        choices=["rest", "mqtt", "both"],
        help="which API to run (default: both)",
    )
    ap.add_argument("--list", action="store_true", help="print the plan, contact nothing")
    ap.add_argument("--tier", action="append", choices=["read", "write", "danger"])
    ap.add_argument("--confirm-danger", action="store_true")
    ap.add_argument("--only", action="append", default=[])
    ap.add_argument("--skip", action="append", default=[])
    ap.add_argument("--timeout", type=float)
    ap.add_argument("--delay", type=float)
    ap.add_argument("--no-color", action="store_true")

    ap.add_argument("--host", help="REST reader IP (overrides lab_rest.json)")
    ap.add_argument("--user", default="")
    ap.add_argument("-p", "--password", dest="password")
    ap.add_argument("--token")
    ap.add_argument("--scheme", choices=["https", "http"])
    ap.add_argument("--verify-tls", action="store_true")
    ap.add_argument("--rest-config", default="", help="REST lab JSON (default: test script/lab_rest.json)")

    ap.add_argument("--broker", help="MQTT broker host (env FXR_MQTT_BROKER)")
    ap.add_argument("--port", type=int)
    ap.add_argument("--cmd-topic")
    ap.add_argument("--rsp-topic")
    ap.add_argument("--ctrl-cmd-topic", default="")
    ap.add_argument("--ctrl-rsp-topic", default="")
    ap.add_argument("--mqtt-user", default="")
    ap.add_argument("--mqtt-password", default="")
    ap.add_argument("--tls", action="store_true")
    ap.add_argument("--ca-cert", default="")
    ap.add_argument("--cert", default="")
    ap.add_argument("--key", default="")
    ap.add_argument("--insecure", action="store_true", help="skip MQTT TLS hostname verify")
    ap.add_argument("--config", default="", help="MQTT lab JSON (default: test script/lab_mqtt.json)")
    return ap.parse_args(argv)


def extra_common(args) -> list[str]:
    cmd: list[str] = []
    for t in args.tier or []:
        cmd += ["--tier", t]
    if args.confirm_danger:
        cmd.append("--confirm-danger")
    for p in args.only:
        cmd += ["--only", p]
    for p in args.skip:
        cmd += ["--skip", p]
    if args.timeout is not None:
        cmd += ["--timeout", str(args.timeout)]
    if args.delay is not None:
        cmd += ["--delay", str(args.delay)]
    if args.no_color:
        cmd.append("--no-color")
    if args.list:
        cmd.append("--list")
    return cmd


def rest_argv(args) -> list[str]:
    cmd = [sys.executable, REST]
    if getattr(args, "rest_config", None):
        cmd += ["--config", args.rest_config]
    if args.host:
        cmd += ["--host", args.host]
    if args.user:
        cmd += ["--user", args.user]
    if args.password:
        cmd += ["--password", args.password]
    if args.token:
        cmd += ["--token", args.token]
    if args.scheme:
        cmd += ["--scheme", args.scheme]
    if args.verify_tls:
        cmd.append("--verify-tls")
    cmd += extra_common(args)
    return cmd


def mqtt_argv(args) -> list[str]:
    cmd = [sys.executable, MQTT]
    if getattr(args, "config", None):
        cmd += ["--config", args.config]
    if args.broker:
        cmd += ["--broker", args.broker]
    if args.port is not None:
        cmd += ["--port", str(args.port)]
    if args.cmd_topic:
        cmd += ["--cmd-topic", args.cmd_topic]
    if args.rsp_topic:
        cmd += ["--rsp-topic", args.rsp_topic]
    if args.ctrl_cmd_topic:
        cmd += ["--ctrl-cmd-topic", args.ctrl_cmd_topic]
    if args.ctrl_rsp_topic:
        cmd += ["--ctrl-rsp-topic", args.ctrl_rsp_topic]
    if args.mqtt_user:
        cmd += ["--username", args.mqtt_user]
    if args.mqtt_password:
        cmd += ["--password", args.mqtt_password]
    if args.tls:
        cmd.append("--tls")
    if args.ca_cert:
        cmd += ["--ca-cert", args.ca_cert]
    if args.cert:
        cmd += ["--cert", args.cert]
    if args.key:
        cmd += ["--key", args.key]
    if args.insecure:
        cmd.append("--insecure")
    cmd += extra_common(args)
    return cmd


def run(label: str, argv: list[str]) -> int:
    print(f"\n======== {label} ========\n", flush=True)
    return subprocess.call(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    codes = []
    if args.api in ("rest", "both"):
        codes.append(run("REST", rest_argv(args)))
    if args.api in ("mqtt", "both"):
        codes.append(run("MQTT", mqtt_argv(args)))
    if any(c == 2 for c in codes):
        return 2
    return 1 if any(c != 0 for c in codes) else 0


if __name__ == "__main__":
    sys.exit(main())
