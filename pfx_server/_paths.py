"""Shared paths/config for test_mqtt_api.py and test_rest_api.py."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

LAB_MQTT = os.path.join(HERE, "lab_mqtt.json")
LAB_REST = os.path.join(HERE, "lab_rest.json")

MQTT_EXAMPLES = os.path.join(HERE, "mqtt", "examples")
TAG_CONFIG = os.path.join(HERE, "tag_config.json")

REST_DIR = HERE
SPEC = os.path.join(HERE, "FXR_60-90_rest_api.yaml")
REST_EXAMPLES = os.path.join(HERE, "rest", "operation_examples")

REPORT_DIR = os.path.join(HERE, "reports")
SUCCESS_DIR = os.path.join(REPORT_DIR, "success")
FAILURE_DIR = os.path.join(REPORT_DIR, "failure")


def _safe_name(name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip("_")
    return name or "result"


def save_split_result(name: str, result: dict) -> str:
    verdict = result.get("verdict")
    target_dir = SUCCESS_DIR if verdict == "PASS" else FAILURE_DIR
    os.makedirs(target_dir, exist_ok=True)
    path = os.path.join(target_dir, f"{_safe_name(name)}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
        fh.write("\n")
    return path


def write_split_indexes() -> None:
    for target_dir in (SUCCESS_DIR, FAILURE_DIR):
        if not os.path.isdir(target_dir):
            continue
        entries = sorted(n for n in os.listdir(target_dir) if n.endswith(".json"))
        index_path = os.path.join(target_dir, "index.json")
        with open(index_path, "w", encoding="utf-8") as fh:
            json.dump(entries, fh, indent=2)
            fh.write("\n")
