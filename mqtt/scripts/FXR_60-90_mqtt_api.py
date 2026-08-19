#!/usr/bin/env python3
"""
FXR_60-90_mqtt_api.py
=====================
Build the final MQTT OpenAPI from this package (self-contained):

 * ``openapi_md.json`` — OpenAPI input
 * ``examples/<command>/{request,response}/*.json`` — Swagger examples

Also refreshes:

 * ``openapi_md.json`` — synced to applied final
 * ``docs/openapi_md.json`` — docs viewer copy

Output: ``FXR_60-90_mqtt_api.json``

Run:

    python FXR60-90/mqtt/scripts/FXR_60-90_mqtt_api.py
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from collections import OrderedDict
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent.parent  # FXR60-90/mqtt
ROOT = PACKAGE_DIR.parent.parent  # repo root (display only)
BASE_OPENAPI = PACKAGE_DIR / "openapi_md.json"
EXAMPLES_DIR = PACKAGE_DIR / "examples"
FINAL_OUT = PACKAGE_DIR / "FXR_60-90_mqtt_api.json"
DOCS_OPENAPI = PACKAGE_DIR / "docs" / "openapi_md.json"


def normalize_mqtt_example(value):
    """MQTT payloads must be objects, not empty strings."""
    if isinstance(value, dict):
        normalized = OrderedDict()
        for key, item in value.items():
            if key == "payload" and item == "":
                normalized[key] = {}
            elif isinstance(item, dict):
                normalized[key] = normalize_mqtt_example(item)
            elif isinstance(item, list):
                normalized[key] = [
                    normalize_mqtt_example(entry) if isinstance(entry, dict) else entry
                    for entry in item
                ]
            else:
                normalized[key] = item
        return normalized
    return value


def _mqtt_example_entry(value, summary=""):
    entry = OrderedDict()
    if summary:
        entry["summary"] = summary
    entry["value"] = normalize_mqtt_example(value)
    return entry


def parse_pack_summaries(cmd_dir: Path) -> dict:
    """Parse an optional ``SUMMARIES.md`` -> ``request/foo.json`` -> {name, summary}.

    Same table format the REST packs use, so example names and titles can be copied
    verbatim from the developer OpenAPI instead of derived from the filename. Packs
    without a ``SUMMARIES.md`` keep the filename-derived behaviour.
    """
    path = cmd_dir / "SUMMARIES.md"
    if not path.is_file():
        return {}
    out: dict = {}
    for chunk in re.split(r"(?m)^###\s+", path.read_text(encoding="utf-8-sig"))[1:]:
        file_match = re.match(r"`(?P<file>[^`]+)`", chunk)
        name_match = re.search(r"\*\*Example name\*\*\s*\|\s*`(?P<name>[^`]+)`", chunk)
        summary_match = re.search(r"\*\*Summary title\*\*\s*\|\s*`(?P<summary>[^`]+)`", chunk)
        if not (file_match and name_match and summary_match):
            continue
        rel = file_match.group("file").replace("\\", "/")
        out[rel] = (name_match.group("name"), summary_match.group("summary"))
    return out


def load_mqtt_pack_examples(examples_dir: Path) -> dict:
    packs: dict = {}
    if not examples_dir.is_dir():
        return packs

    for cmd_dir in sorted(p for p in examples_dir.iterdir() if p.is_dir()):
        if cmd_dir.name.startswith(("_", ".")):
            continue
        pack = {"request": OrderedDict(), "response": OrderedDict()}
        summaries = parse_pack_summaries(cmd_dir)
        for direction in ("request", "response"):
            sub = cmd_dir / direction
            if not sub.is_dir():
                continue
            for path in sorted(sub.glob("*.json")):
                if path.name.startswith("_") or path.name == "parameters.json":
                    continue
                try:
                    with path.open("r", encoding="utf-8-sig") as fh:
                        value = json.load(fh, object_pairs_hook=OrderedDict)
                except Exception as exc:
                    print(f"  WARNING: skip invalid example {path}: {exc}")
                    continue
                stem = path.stem
                name, summary = summaries.get(
                    f"{direction}/{path.name}", (stem, stem.replace("_", " "))
                )
                pack[direction][name] = _mqtt_example_entry(value, summary)
        if pack["request"] or pack["response"]:
            packs[cmd_dir.name] = pack
    return packs


def apply_mqtt_pack_examples(openapi: dict, examples_dir: Path):
    packs = load_mqtt_pack_examples(examples_dir)
    if not packs:
        return 0, []

    paths = openapi.get("paths") or {}
    patched = 0
    missing = []
    for command, pack in packs.items():
        op = (paths.get(f"/{command}") or {}).get("post")
        if not isinstance(op, dict):
            missing.append(command)
            continue

        req_examples = pack.get("request") or OrderedDict()
        if req_examples:
            rb = op.setdefault("requestBody", OrderedDict())
            content = rb.setdefault("content", OrderedDict())
            app = content.setdefault("application/json", OrderedDict())
            app["examples"] = req_examples

        resp_examples = pack.get("response") or OrderedDict()
        if resp_examples:
            responses = op.setdefault("responses", OrderedDict())
            target = None
            for code in ("200", "201", "default"):
                candidate = responses.get(code)
                if isinstance(candidate, dict):
                    target = candidate
                    break
            if target is None:
                target = OrderedDict([("description", "Successful response")])
                responses["200"] = target
            content = target.setdefault("content", OrderedDict())
            app = content.setdefault("application/json", OrderedDict())
            app["examples"] = resp_examples

        patched += 1

    print(
        f"  Applied example packs for {patched} commands from {examples_dir}"
        + (f" ({len(missing)} packs with no matching path)" if missing else "")
    )
    return patched, missing


def main() -> int:
    if not BASE_OPENAPI.is_file():
        print(f"Missing base OpenAPI: {BASE_OPENAPI}", file=sys.stderr)
        return 1

    if not EXAMPLES_DIR.is_dir():
        print(f"Missing MQTT examples: {EXAMPLES_DIR}", file=sys.stderr)
        return 1

    packs = sum(
        1 for p in EXAMPLES_DIR.iterdir() if p.is_dir() and not p.name.startswith("_")
    )
    try:
        pkg_disp = PACKAGE_DIR.relative_to(ROOT)
        base_disp = BASE_OPENAPI.relative_to(ROOT)
        ex_disp = EXAMPLES_DIR.relative_to(ROOT)
    except ValueError:
        pkg_disp, base_disp, ex_disp = PACKAGE_DIR, BASE_OPENAPI, EXAMPLES_DIR

    print(f"Package         : {pkg_disp}")
    print(f"Base OpenAPI    : {base_disp}")
    print(f"Example packs   : {packs} under {ex_disp}")

    print("\n=== Load base OpenAPI ===")
    with BASE_OPENAPI.open("r", encoding="utf-8-sig") as fh:
        openapi = json.load(fh, object_pairs_hook=OrderedDict)
    print(f"  {len(openapi.get('paths') or {})} endpoints")

    print("\n=== Overlay examples ===")
    apply_mqtt_pack_examples(openapi, EXAMPLES_DIR)

    info = openapi.setdefault("info", OrderedDict())
    info["title"] = "Zebra Fixed Reader MQTT API (FXR readers)"
    info["description"] = (
        "# Overview\n"
        "\n"
        "This MQTT API controls Zebra **FXR** RFID readers. FXR documentation includes **FXR60** and **FXR90**.\n"
        "\n"
        "It covers command payloads, responses, events, and configuration workflows used to monitor and control reader operation."
    )

    print("\n=== Write final ===")
    with FINAL_OUT.open("w", encoding="utf-8") as fh:
        json.dump(openapi, fh, indent=4, ensure_ascii=False)
    print(f"  Written to {FINAL_OUT.name}")

    shutil.copyfile(FINAL_OUT, BASE_OPENAPI)
    print(f"  Synced        : {BASE_OPENAPI.name}")

    print("\n=== Refresh docs viewer OpenAPI ===")
    DOCS_OPENAPI.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(FINAL_OUT, DOCS_OPENAPI)
    print(f"  Copied to docs/{DOCS_OPENAPI.name}")

    print(f"\nOutput (final)  : {FINAL_OUT.name}")
    print("Docs viewer     : docs/index.html")
    print("Swagger UI      : docs/swagger.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
