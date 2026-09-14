"""Sync important schemas from rest/openAPISpec 12.yaml into mqtt/openapi_md.json."""
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent
SPEC12 = REPO / "rest" / "openAPISpec 12.yaml"
REST_PUBLISHED = REPO / "rest" / "FXR_60-90_rest_api.yaml"
MQTT_OPENAPI = REPO / "mqtt" / "openapi_md.json"

SEED_SCHEMAS = [
    "access_cmds.v1",
    "actionBlink.v1",
    "actionConditions.v1",
    "antennaStopCondition.v1",
    "conditionsArray.v1",
    "gpi.v1",
    "gpoledAction.v1",
    "query.v1",
    "select.v1",
    "tagMetaData.v1",
    "operatingModes",
    "gpioLedConfig",
    "mgmtEventConfig",
]


def collect_deps(schemas: dict, name: str, seen: set[str] | None = None) -> set[str]:
    if seen is None:
        seen = set()
    if name in seen or name not in schemas:
        return seen
    seen.add(name)
    blob = json.dumps(schemas[name])
    for dep in re.findall(r'#/components/schemas/([^"\\]+)', blob):
        collect_deps(schemas, dep, seen)
    return seen


def dedupe_enum_list(items: list) -> list:
    out = []
    for x in items:
        if x not in out:
            out.append(x)
    return out


def walk_fix_write_unlock(node) -> None:
    """Remove duplicate WRITE_UNLOCK_USER_BANK entries in any enum list."""
    if isinstance(node, dict):
        enum = node.get("enum")
        if isinstance(enum, list) and "WRITE_UNLOCK_USER_BANK" in enum:
            node["enum"] = dedupe_enum_list(enum)
        for v in node.values():
            walk_fix_write_unlock(v)
    elif isinstance(node, list):
        for v in node:
            walk_fix_write_unlock(v)


def replace_inline_tag_metadata(node) -> int:
    """Replace broken inline tagMetaData schema objects with Spec12 $ref."""
    count = 0
    if isinstance(node, dict):
        tmd = node.get("tagMetaData")
        if isinstance(tmd, dict) and tmd.get("type") == "array" and "items" in tmd:
            node["tagMetaData"] = {"$ref": "#/components/schemas/tagMetaData.v1"}
            count += 1
        for v in node.values():
            count += replace_inline_tag_metadata(v)
    elif isinstance(node, list):
        for v in node:
            count += replace_inline_tag_metadata(v)
    return count


def main() -> None:
    with SPEC12.open(encoding="utf-8") as f:
        spec12 = yaml.safe_load(f)
    src_schemas = spec12["components"]["schemas"]

    # Spec 12 still has the broken tagMetaData items shape (type: [string, object]).
    # Prefer the published REST oneOf definition when available.
    with REST_PUBLISHED.open(encoding="utf-8") as f:
        rest_pub = yaml.safe_load(f)
    rest_schemas = rest_pub.get("components", {}).get("schemas", {})
    pub_tmd = rest_schemas.get("tagMetaData.v1")
    if isinstance(pub_tmd, dict) and "oneOf" in (pub_tmd.get("items") or {}):
        src_schemas = dict(src_schemas)
        src_schemas["tagMetaData.v1"] = deepcopy(pub_tmd)
        print("Using published REST tagMetaData.v1 (oneOf) instead of Spec 12")

    needed: set[str] = set()
    for name in SEED_SCHEMAS:
        needed |= collect_deps(src_schemas, name)
    # Ensure published tagMetaData deps are included if any
    if "tagMetaData.v1" in src_schemas:
        needed |= collect_deps(src_schemas, "tagMetaData.v1")

    mqtt = json.loads(MQTT_OPENAPI.read_text(encoding="utf-8"))
    components = mqtt.setdefault("components", {})
    schemas = components.setdefault("schemas", {})

    copied = []
    for name in sorted(needed):
        if name not in src_schemas:
            print(f"WARNING: missing schema {name}")
            continue
        schemas[name] = deepcopy(src_schemas[name])
        copied.append(name)

    walk_fix_write_unlock(schemas)
    walk_fix_write_unlock(mqtt)
    replaced = replace_inline_tag_metadata(mqtt)

    MQTT_OPENAPI.write_text(
        json.dumps(mqtt, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Copied {len(copied)} schemas into mqtt/openapi_md.json components.schemas")
    for n in copied:
        print(" ", n)
    print(f"Replaced inline tagMetaData schemas with $ref: {replaced}")
    print("Deduped WRITE_UNLOCK_USER_BANK enums")


if __name__ == "__main__":
    main()
