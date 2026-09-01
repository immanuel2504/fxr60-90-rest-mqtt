"""Repo-root lookup so this folder can live inside the docs tree or be copied with it."""

from __future__ import annotations

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo_root() -> str:
    cur = HERE
    for _ in range(8):
        yaml_path = os.path.join(cur, "rest", "FXR_60-90_rest_api.yaml")
        mqtt_examples = os.path.join(cur, "mqtt", "examples")
        if os.path.isfile(yaml_path) and os.path.isdir(mqtt_examples):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return os.path.dirname(HERE)


ROOT = find_repo_root()
REST_DIR = os.path.join(ROOT, "rest")
SPEC = os.path.join(REST_DIR, "FXR_60-90_rest_api.yaml")
REST_EXAMPLES = os.path.join(REST_DIR, "operation_examples")
MQTT_EXAMPLES = os.path.join(ROOT, "mqtt", "examples")
TAG_CONFIG = os.path.join(ROOT, "mqtt", "tag_config.json")
REPORT_DIR = os.path.join(HERE, "reports")
SUCCESS_DIR = os.path.join(REPORT_DIR, "success")
FAILURE_DIR = os.path.join(REPORT_DIR, "failure")
LAB_REST = os.path.join(HERE, "lab_rest.json")
LAB_MQTT = os.path.join(HERE, "lab_mqtt.json")


def result_slug(text: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", text or "").strip("._-")
    return cleaned[:120] or "result"


def save_split_result(slug: str, result: dict) -> str | None:
    """Write one test into reports/success or reports/failure. SKIP is not saved."""
    verdict = str(result.get("verdict") or "").upper()
    if verdict == "SKIP":
        return None
    os.makedirs(SUCCESS_DIR, exist_ok=True)
    os.makedirs(FAILURE_DIR, exist_ok=True)
    name = result_slug(slug) + ".json"
    dest_dir = SUCCESS_DIR if verdict == "PASS" else FAILURE_DIR
    other_dir = FAILURE_DIR if dest_dir == SUCCESS_DIR else SUCCESS_DIR
    other_path = os.path.join(other_dir, name)
    if os.path.isfile(other_path):
        os.remove(other_path)
    path = os.path.join(dest_dir, name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
        fh.write("\n")
    return path


def write_split_indexes() -> None:
    """Refresh a short index in each of success/ and failure/."""
    for folder, title in ((SUCCESS_DIR, "Success"), (FAILURE_DIR, "Failure")):
        os.makedirs(folder, exist_ok=True)
        files = sorted(n for n in os.listdir(folder) if n.endswith(".json"))
        lines = [f"# {title}", "", f"{len(files)} result file(s).", ""]
        if files:
            lines += ["| File | Verdict | What |", "|---|---|---|"]
            for name in files:
                path = os.path.join(folder, name)
                try:
                    with open(path, encoding="utf-8") as fh:
                        data = json.load(fh)
                except (OSError, json.JSONDecodeError):
                    data = {}
                verdict = data.get("verdict") or ""
                what = (
                    data.get("command")
                    or f"{data.get('method', '')} {data.get('url_path') or data.get('path') or ''}".strip()
                    or data.get("step")
                    or name
                )
                lines.append(f"| `{name}` | {verdict} | `{what}` |")
        with open(os.path.join(folder, "_index.md"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
