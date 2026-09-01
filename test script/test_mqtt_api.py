#!/usr/bin/env python3
"""Exercise FXR60/FXR90 MQTT commands against a live reader via a broker.

The PC publishes on the reader's *command* topic (what the reader subscribes to)
and listens on the reader's *response* topic (what the reader publishes).

That matches cloudConfig: reader subscribeTopic = commands, publishTopic = replies.

Commands are discovered from mqtt/examples/<command>/request/*.json.
One body is sent per command (prefers request/default.json).

Tiers (same idea as rest/scripts/test_rest_api.py):

  read    get_* commands. Default. No side effects.
  write   reversible sets (LED, BLE config, start/stop, timezone, …)
  danger  reboot, password, network, certs, OS, uninstall, log delete.
          Requires --tier danger AND --confirm-danger.

Usage
-----
  # On a lab PC that can reach the broker in lab_mqtt.json:
  python test_mqtt_api.py
  python test_mqtt_api.py --list
  python test_mqtt_api.py --only get_status

Edit lab_mqtt.json (broker + topics) for another site. CLI flags override the file.

Each command result is saved to `reports/success/` (PASS) or `reports/failure/` (FAIL/WARN).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import threading
import time
import uuid
from collections import OrderedDict

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from _paths import LAB_MQTT as DEFAULT_CONFIG
from _paths import MQTT_EXAMPLES as EXAMPLES
from _paths import FAILURE_DIR, REPORT_DIR, SUCCESS_DIR
from _paths import TAG_CONFIG
from _paths import save_split_result, write_split_indexes

WRITE_OPS = {
    "set_appled", "set_stackled", "set_gpo", "set_hostname", "set_hostName",
    "set_timeZone", "set_cableLossCompensation", "set_bleConfig", "set_impinjGen2X",
    "set_logs", "set_mode", "set_region", "set_eSimConfig", "set_ntpServer",
    "set_dataToRG", "autostart_user_app", "set_autostartUserapp", "set_passthru",
    "set_req_usr_app", "set_reqToUserapp", "start", "stop", "start_user_app",
    "set_startUserapp", "stop_user_app", "set_stopUserapp", "set_preSelection",
    "set_displayConfig",
}
DANGER_OPS = {
    "reboot", "set_os", "revertback", "set_password", "set_network",
    "set_importCloudConfig", "set_config", "set_update_cert", "refresh-cert",
    "del_certs", "set_installCACertificate", "del_CACertificate",
    "install_user_app", "uninstall-user-app", "del_syslogs", "del_radio_pkt_logs",
}

RESET = "\033[0m"
COLOR = {
    "PASS": "\033[32m", "WARN": "\033[33m", "FAIL": "\033[31m",
    "SKIP": "\033[90m", "head": "\033[1m",
}


def paint(text: str, key: str, enabled: bool) -> str:
    return f"{COLOR[key]}{text}{RESET}" if enabled and key in COLOR else text


def load_broker_config(path: str) -> dict:
    if not path or not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return data if isinstance(data, dict) else {}


def load_tag_config() -> dict:
    if not os.path.isfile(TAG_CONFIG):
        return {}
    with open(TAG_CONFIG, encoding="utf-8") as fh:
        return json.load(fh)


def control_commands(tag_cfg: dict) -> set[str]:
    names = set()
    order = tag_cfg.get("operation_order") or {}
    for group in ("Control", "ImpinjGen2X"):
        names.update(order.get(group) or [])
    return names


def skip_commands(tag_cfg: dict) -> set[str]:
    names = set()
    order = tag_cfg.get("operation_order") or {}
    for group in ("Management-events", "Tag-data-events", "Network"):
        names.update(order.get(group) or [])
    names.update({
        "get_network", "set_network", "get_availableWifiNetworks",
        "get_networkInterfaces", "get_readPoints", "get_gpsCoordinates",
        "get_eSimConfig", "set_eSimConfig",
    })
    return names


def tier_of(command: str, folder: str = "") -> str:
    """Classify by example folder first (stable), then wire command name."""
    for key in (folder, command):
        if not key:
            continue
        if key in DANGER_OPS:
            return "danger"
        if key in WRITE_OPS:
            return "write"
        if key.startswith("get_"):
            return "read"
    return "danger"


# When several request examples exist, pick the least surprising body.
PREFERRED_REQUEST = {
    "start": "start_Inventory.json",
    "stop": "stop_RFID_default.json",
    "set_bleConfig": "enable_ble.json",
    "get_mode": "default_configured_only.json",
}


def pick_request(command_dir: str) -> tuple[str | None, dict | None]:
    req_dir = os.path.join(command_dir, "request")
    if not os.path.isdir(req_dir):
        return None, None
    files = sorted(n for n in os.listdir(req_dir) if n.endswith(".json"))
    if not files:
        return None, None
    folder = os.path.basename(command_dir)
    preferred = PREFERRED_REQUEST.get(folder)
    if preferred and preferred in files:
        chosen = preferred
    elif "default.json" in files:
        chosen = "default.json"
    else:
        chosen = files[0]
    path = os.path.join(req_dir, chosen)
    with open(path, encoding="utf-8") as fh:
        body = json.load(fh)
    return f"request/{chosen}", body


def discover_commands(tag_cfg: dict) -> list[dict]:
    skip = skip_commands(tag_cfg)
    out = []
    if not os.path.isdir(EXAMPLES):
        return out
    for name in sorted(os.listdir(EXAMPLES)):
        folder = os.path.join(EXAMPLES, name)
        if not os.path.isdir(folder) or name in skip:
            continue
        source, body = pick_request(folder)
        if body is None or not isinstance(body, dict):
            continue
        command = body.get("command") or name
        if command in skip:
            continue
        out.append({
            "folder": name,
            "command": command,
            "tier": tier_of(command, name),
            "source": source,
            "body": body,
            "channel": "control" if command in control_commands(tag_cfg) else "management",
        })
    return out


class MqttSession:
    def __init__(self, args):
        try:
            import paho.mqtt.client as mqtt
        except ImportError:
            sys.exit("paho-mqtt is required:  pip install paho-mqtt")
        self._mqtt = mqtt
        self.args = args
        self._lock = threading.Lock()
        self._inbox: dict[str, dict] = {}
        self._connected = threading.Event()
        cid = args.client_id or f"fxr-api-test-{uuid.uuid4().hex[:8]}"
        try:
            self.client = mqtt.Client(
                mqtt.CallbackAPIVersion.VERSION2, client_id=cid
            )
            self.client.on_connect = self._on_connect_v2
            self.client.on_message = self._on_message_v2
        except AttributeError:
            self.client = mqtt.Client(client_id=cid)
            self.client.on_connect = self._on_connect_v1
            self.client.on_message = self._on_message_v1
        if args.username:
            self.client.username_pw_set(args.username, args.password or "")
        if args.tls:
            ctx = ssl.create_default_context()
            if args.ca_cert:
                ctx.load_verify_locations(args.ca_cert)
            if args.insecure:
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
            if args.cert and args.key:
                ctx.load_cert_chain(args.cert, args.key)
            self.client.tls_set_context(ctx)

    def _on_connect_v1(self, client, userdata, flags, rc):
        if rc == 0:
            self._connected.set()

    def _on_connect_v2(self, client, userdata, flags, reason_code, properties):
        ok = getattr(reason_code, "value", reason_code) in (0, "Success")
        if ok or str(reason_code) in ("Success", "0"):
            self._connected.set()

    def _store(self, payload: bytes) -> None:
        try:
            data = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return
        cid = data.get("command_id")
        if cid:
            with self._lock:
                self._inbox[str(cid)] = data

    def _on_message_v1(self, client, userdata, msg):
        self._store(msg.payload)

    def _on_message_v2(self, client, userdata, msg):
        self._store(msg.payload)

    def connect(self) -> None:
        self.client.connect(self.args.broker, self.args.port, keepalive=60)
        self.client.loop_start()
        if not self._connected.wait(self.args.timeout):
            raise TimeoutError(
                f"MQTT connect timed out ({self.args.broker}:{self.args.port})"
            )
        topics = {self.args.rsp_topic}
        if self.args.ctrl_rsp_topic:
            topics.add(self.args.ctrl_rsp_topic)
        for topic in topics:
            self.client.subscribe(topic, qos=self.args.qos)

    def close(self) -> None:
        try:
            self.client.loop_stop()
            self.client.disconnect()
        except Exception:
            pass

    def call(self, cmd_topic: str, body: dict, timeout: float) -> dict | None:
        command_id = body["command_id"]
        with self._lock:
            self._inbox.pop(command_id, None)
        self.client.publish(cmd_topic, json.dumps(body), qos=self.args.qos)
        deadline = time.time() + timeout
        while time.time() < deadline:
            with self._lock:
                if command_id in self._inbox:
                    return self._inbox.pop(command_id)
            time.sleep(0.05)
        return None


def parse_args(argv=None):
    ap = argparse.ArgumentParser(
        description="Test FXR MQTT commands one by one via a broker.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Usage\n-----\n")[-1],
    )
    ap.add_argument("--config", default=DEFAULT_CONFIG,
                    help="JSON with broker/topics (default: test script/lab_mqtt.json)")
    ap.add_argument("--broker", default=None, help="MQTT broker host (overrides config)")
    ap.add_argument("--port", type=int, default=None)
    ap.add_argument("--cmd-topic", default=None, help="management command topic")
    ap.add_argument("--rsp-topic", default=None, help="management response topic")
    ap.add_argument("--ctrl-cmd-topic", default=None, help="control command topic")
    ap.add_argument("--ctrl-rsp-topic", default=None, help="control response topic")
    ap.add_argument("--username", default=os.environ.get("FXR_MQTT_USER", ""))
    ap.add_argument("--password", default=os.environ.get("FXR_MQTT_PASSWORD", ""))
    ap.add_argument("--qos", type=int, default=None, help="0, 1, or 2 (default from lab_mqtt.json)")
    ap.add_argument("--client-id", default="")
    ap.add_argument("--tls", action="store_true")
    ap.add_argument("--ca-cert", default="")
    ap.add_argument("--cert", default="")
    ap.add_argument("--key", default="")
    ap.add_argument("--insecure", action="store_true", help="skip TLS hostname verify")
    ap.add_argument("--tier", action="append", choices=["read", "write", "danger"])
    ap.add_argument("--confirm-danger", action="store_true")
    ap.add_argument("--only", action="append", default=[], help="regex on command name")
    ap.add_argument("--skip", action="append", default=[], help="regex to exclude")
    ap.add_argument("--timeout", type=float, default=15.0)
    ap.add_argument("--delay", type=float, default=0.2)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--no-color", action="store_true")
    args = ap.parse_args(argv)

    cfg = load_broker_config(args.config)
    mgmt = cfg.get("management") or {}
    ctrl = cfg.get("control") or {}

    args.broker = args.broker or os.environ.get("FXR_MQTT_BROKER") or cfg.get("broker")
    if args.port is None:
        env_port = os.environ.get("FXR_MQTT_PORT")
        args.port = int(env_port) if env_port else int(cfg.get("port") or 1883)
    args.cmd_topic = args.cmd_topic or os.environ.get("FXR_MQTT_CMD_TOPIC") or mgmt.get("cmd")
    args.rsp_topic = args.rsp_topic or os.environ.get("FXR_MQTT_RSP_TOPIC") or mgmt.get("rsp")
    args.ctrl_cmd_topic = args.ctrl_cmd_topic or ctrl.get("cmd") or ""
    args.ctrl_rsp_topic = args.ctrl_rsp_topic or ctrl.get("rsp") or ""
    if args.qos is None:
        env_qos = os.environ.get("FXR_MQTT_QOS")
        args.qos = int(env_qos) if env_qos is not None else int(cfg.get("qos") or 0)
    if args.qos not in (0, 1, 2):
        ap.error("--qos must be 0, 1, or 2")
    if cfg.get("tls"):
        args.tls = True
    args.tier = args.tier or ["read"]
    if "danger" in args.tier and not args.confirm_danger and not args.list:
        ap.error("--tier danger also requires --confirm-danger")
    if not args.list:
        if not args.broker:
            ap.error("broker missing: set test script/lab_mqtt.json or pass --broker")
        if not args.cmd_topic or not args.rsp_topic:
            ap.error("command/response topics missing: set lab_mqtt.json or --cmd-topic / --rsp-topic")
    return args


def selected(plan: list[dict], args) -> list[dict]:
    out = []
    for item in plan:
        if item["tier"] not in args.tier:
            continue
        blob = item["command"]
        if args.only and not any(re.search(p, blob) for p in args.only):
            continue
        if args.skip and any(re.search(p, blob) for p in args.skip):
            continue
        out.append(item)
    return out


def write_reports(results: list[dict], meta: dict) -> tuple[str, str]:
    os.makedirs(REPORT_DIR, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    json_path = os.path.join(REPORT_DIR, f"mqtt_test_{stamp}.json")
    md_path = os.path.join(REPORT_DIR, f"mqtt_test_{stamp}.md")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump({"meta": meta, "results": results}, fh, indent=2)
        fh.write("\n")
    lines = [
        f"# MQTT API test {stamp}",
        "",
        f"- Broker: `{meta.get('broker')}:{meta.get('port')}`",
        f"- Cmd topic: `{meta.get('cmd_topic')}`",
        f"- Rsp topic: `{meta.get('rsp_topic')}`",
        f"- Tiers: {', '.join(meta.get('tiers') or [])}",
        "",
        "| Verdict | Command | Channel | Example | ms | Note |",
        "|---|---|---|---|---:|---|",
    ]
    for r in results:
        note = (r.get("note") or "").replace("|", "/")
        lines.append(
            f"| {r['verdict']} | `{r['command']}` | {r['channel']} | "
            f"{r.get('source') or ''} | {r.get('ms', 0):.0f} | {note} |"
        )
        save_split_result(f"mqtt_{r.get('command')}", r)
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    write_split_indexes()
    return md_path, json_path


def run_one(session: MqttSession, item: dict, args) -> dict:
    body = json.loads(json.dumps(item["body"]))
    body["command"] = item["command"]
    body["command_id"] = f"test-{item['command']}-{uuid.uuid4().hex[:10]}"
    if "payload" not in body:
        body["payload"] = {}
    topic = args.cmd_topic
    if item["channel"] == "control" and args.ctrl_cmd_topic:
        topic = args.ctrl_cmd_topic
    t0 = time.perf_counter()
    reply = session.call(topic, body, args.timeout)
    ms = (time.perf_counter() - t0) * 1000
    if reply is None:
        return {
            "command": item["command"], "channel": item["channel"],
            "source": item["source"], "tier": item["tier"],
            "verdict": "FAIL", "ms": ms, "note": "no MQTT response (timeout)",
            "request_id": body["command_id"], "response": None,
        }
    status = reply.get("response")
    verdict = "PASS" if status == "success" else "WARN"
    note = "" if status == "success" else f"response={status!r}"
    payload = reply.get("payload")
    if isinstance(payload, dict) and payload.get("error"):
        verdict = "FAIL"
        note = str(payload.get("error"))
    return {
        "command": item["command"], "channel": item["channel"],
        "source": item["source"], "tier": item["tier"],
        "verdict": verdict, "ms": round(ms, 1), "note": note,
        "request_id": body["command_id"],
        "response": status,
        "response_preview": json.dumps(reply)[:500],
    }


def main(argv=None) -> int:
    args = parse_args(argv)
    color = not args.no_color and sys.stdout.isatty()
    tag_cfg = load_tag_config()
    plan = discover_commands(tag_cfg)
    chosen = selected(plan, args)

    if args.list:
        print(paint(
            f"{len(plan)} MQTT command(s) with request examples, "
            f"{len(chosen)} selected (tiers: {', '.join(args.tier)})",
            "head", color,
        ))
        for item in plan:
            mark = "x" if item in chosen else " "
            print(
                f" [{mark}] {item['tier']:<6} {item['channel']:<11} "
                f"{item['command']:<32} {item['source']}"
            )
        return 0

    print(paint(
        f"MQTT {args.broker}:{args.port}  cmd={args.cmd_topic}  rsp={args.rsp_topic}",
        "head", color,
    ))
    if args.ctrl_cmd_topic:
        print(paint(
            f"      control cmd={args.ctrl_cmd_topic}  rsp={args.ctrl_rsp_topic}",
            "head", color,
        ))
    if os.path.isfile(args.config):
        print(f"      config {args.config}")
    session = MqttSession(args)
    try:
        session.connect()
    except Exception as exc:
        print(paint(f"FAIL  connect: {exc}", "FAIL", color))
        return 2

    results = []
    print(paint(f"\n{len(chosen)} command(s) (tiers: {', '.join(args.tier)})\n", "head", color))
    try:
        for item in chosen:
            res = run_one(session, item, args)
            results.append(res)
            print(
                f"  {paint(res['verdict'].ljust(4), res['verdict'], color)}  "
                f"{item['channel']:<11} {item['command']:<32} "
                f"{res['ms']:.0f} ms  {res.get('note') or ''}"
            )
            if args.delay:
                time.sleep(args.delay)
    finally:
        session.close()

    meta = {
        "broker": args.broker, "port": args.port,
        "cmd_topic": args.cmd_topic, "rsp_topic": args.rsp_topic,
        "tiers": args.tier, "started": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    md_path, json_path = write_reports(results, meta)
    counts = {v: sum(1 for r in results if r["verdict"] == v)
              for v in ("PASS", "WARN", "FAIL", "SKIP")}
    print(paint("\nSummary", "head", color))
    for verdict, count in counts.items():
        if count:
            print(f"  {paint(verdict, verdict, color)}  {count}")
    print(f"\nReports:\n  {md_path}\n  {json_path}")
    print(f"  success: {SUCCESS_DIR}")
    print(f"  failure: {FAILURE_DIR}")
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
