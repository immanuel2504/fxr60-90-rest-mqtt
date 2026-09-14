#!/usr/bin/env python3
"""Sync mqtt/operation_descriptions/*.md into mqtt/openapi_md.json event paths."""
from __future__ import annotations

import json
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MQTT = ROOT / "mqtt" / "openapi_md.json"
DESC_DIR = ROOT / "mqtt" / "operation_descriptions"

EVENT_MAP = [
    ("heartbeat.md", "/heartbeat"),
    ("heartbeatRadioControl.md", "/heartbeat_radio_control"),
    ("heartbeatReaderGateway.md", "/heartbeat_reader_gateway"),
    ("heartbeatSystem.md", "/heartbeat_system"),
    ("heartbeatUserapps.md", "/heartbeat_userapps"),
    ("heartbeatInterval.md", "/heartbeat_interval"),
    ("gpi.md", "/gpi"),
    ("gpo.md", "/gpo"),
    ("userappEvent.md", "/userapp_event"),
    ("error.md", "/error"),
    ("warning.md", "/warning"),
    ("firmwareUpdateProgress.md", "/firmwareUpdateProgress"),
    ("tagDataEvents.md", "/tagDataEvents"),
    ("bleDataEvents.md", "/ble_data_events"),
]

EVENT_PATH_SUMMARIES = {
    "/heartbeat": "Heartbeat",
    "/heartbeat_radio_control": "Radio Control",
    "/heartbeat_reader_gateway": "Reader Gateway",
    "/heartbeat_system": "System",
    "/heartbeat_userapps": "User Apps",
    "/heartbeat_interval": "Heartbeat Interval",
    "/tagDataEvents": "Tag Data Events",
    "/ble_data_events": "BLE Data Events",
}


def ensure_event_paths(paths: dict) -> int:
    created = 0
    for path_key, summary in EVENT_PATH_SUMMARIES.items():
        if path_key in paths:
            continue
        paths[path_key] = OrderedDict(
            [
                (
                    "post",
                    OrderedDict(
                        [
                            ("tags", ["Management-events"]),
                            ("summary", summary),
                            ("description", ""),
                            (
                                "responses",
                                OrderedDict(
                                    [
                                        (
                                            "default",
                                            OrderedDict(
                                                [
                                                    ("description", "heartbeat event payload"),
                                                    (
                                                        "content",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "application/json",
                                                                    OrderedDict(
                                                                        [
                                                                            (
                                                                                "schema",
                                                                                OrderedDict(
                                                                                    [("type", "object")]
                                                                                ),
                                                                            )
                                                                        ]
                                                                    ),
                                                                )
                                                            ]
                                                        ),
                                                    ),
                                                ]
                                            ),
                                        )
                                    ]
                                ),
                            ),
                        ]
                    ),
                )
            ]
        )
        created += 1
        print(f"  created path stub {path_key}")
    return created


def main() -> int:
    if not MQTT.is_file():
        print(f"Missing {MQTT}", file=sys.stderr)
        return 1

    data = json.loads(MQTT.read_text(encoding="utf-8-sig"), object_pairs_hook=OrderedDict)
    paths = data.setdefault("paths", OrderedDict())
    ensure_event_paths(paths)
    updated = 0

    for filename, path_key in EVENT_MAP:
        md_path = DESC_DIR / filename
        if not md_path.is_file():
            print(f"  WARNING: missing {md_path}")
            continue
        op = (paths.get(path_key) or {}).get("post")
        if not isinstance(op, dict):
            print(f"  WARNING: no POST op at {path_key}")
            continue
        op["description"] = md_path.read_text(encoding="utf-8-sig").strip()
        if path_key in EVENT_PATH_SUMMARIES:
            op["summary"] = EVENT_PATH_SUMMARIES[path_key]
        updated += 1
        print(f"  synced {filename} -> {path_key}")

    MQTT.write_text(json.dumps(data, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {updated} management event descriptions in {MQTT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
