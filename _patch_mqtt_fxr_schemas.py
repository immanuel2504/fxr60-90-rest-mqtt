"""Patch mqtt/openapi_md.json for FXR-specific schema and example alignment."""
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MQTT = ROOT / "mqtt" / "openapi_md.json"

UNSUPPORTED_PAYLOAD_KEYS = {"transfer_protocol", "retry", "timeouts"}

SCAN_TYPE_ONEOF = {
    "oneOf": [
        {
            "type": "array",
            "description": "Global start/stop. Array of ble and/or rfid.",
            "items": {"type": "string", "enum": ["ble", "rfid"]},
            "minItems": 1,
            "uniqueItems": True,
            "example": ["ble", "rfid"],
        },
        {
            "type": "object",
            "description": "Targeted start/stop per data-endpoint connection name.",
            "additionalProperties": {
                "type": "array",
                "items": {"type": "string", "enum": ["ble", "rfid"]},
                "minItems": 1,
                "uniqueItems": True,
            },
            "example": {"dataEndpoint1": ["ble", "rfid"], "dataEndpoint2": ["rfid"]},
        },
    ]
}

GET_STACKLED_PAYLOAD_ONEOF = {
    "oneOf": [
        {
            "type": "object",
            "required": ["status"],
            "properties": {
                "status": {"type": "string", "enum": ["DEFAULT"]},
            },
            "additionalProperties": False,
        },
        {
            "type": "object",
            "required": ["status", "color", "flash", "seconds"],
            "properties": {
                "status": {"type": "string", "enum": ["NON_DEFAULT"]},
                "color": {"type": "string", "enum": ["red", "amber", "green", "blue", "off"]},
                "brightness": {"type": "string", "enum": ["low", "med", "high"]},
                "flash": {"type": "boolean"},
                "seconds": {"type": "integer"},
                "seconds_remaining": {"type": "integer"},
            },
        },
        {
            "title": "failure",
            "type": "object",
            "description": "Error payload when response is failure.",
            "properties": {
                "code": {"type": "integer", "description": "The error code", "example": 1},
                "message": {"type": "string", "description": "The error message"},
            },
        },
    ]
}


def strip_keys(node: dict, keys: set[str]) -> None:
    props = node.get("properties")
    if isinstance(props, dict):
        for key in keys:
            props.pop(key, None)


def payload_schema(paths: dict, path_key: str) -> dict:
    post = paths.get(path_key, {}).get("post", {})
    return (
        post.get("requestBody", {})
        .get("content", {})
        .get("application/json", {})
        .get("schema", {})
        .get("properties", {})
        .get("payload", {})
    )


def response_payload_schema(paths: dict, path_key: str) -> dict | None:
    post = paths.get(path_key, {}).get("post", {})
    responses = post.get("responses", {})
    default = responses.get("default", {})
    content = default.get("content", {}).get("application/json", {})
    schema = content.get("schema", {})
    props = schema.get("properties", {})
    payload = props.get("payload")
    return payload if isinstance(payload, dict) else None


def main() -> None:
    data = json.loads(MQTT.read_text(encoding="utf-8"))
    paths = data.get("paths", {})

    for path_key in ("/set_os", "/install_user_app", "/set_update_cert"):
        strip_keys(payload_schema(paths, path_key), UNSUPPORTED_PAYLOAD_KEYS)

    for path_key in ("/start", "/stop"):
        payload = payload_schema(paths, path_key)
        if payload.get("properties", {}).get("scanType"):
            payload["properties"]["scanType"] = copy.deepcopy(SCAN_TYPE_ONEOF)

    stack_payload = response_payload_schema(paths, "/get_stackled")
    if stack_payload is not None:
        stack_payload.clear()
        stack_payload.update(copy.deepcopy(GET_STACKLED_PAYLOAD_ONEOF))

    set_stack_payload = response_payload_schema(paths, "/set_stackled")
    if set_stack_payload is not None and "oneOf" in set_stack_payload:
        for branch in set_stack_payload["oneOf"]:
            if branch.get("title") == "success":
                branch["description"] = (
                    "Empty object on success. REST returns HTTP 200 with an empty string body."
                )

    blob = json.dumps(data)
    blob = blob.replace(
        "A list of all resolutions supported by the monitor hardware.",
        "List of resolutions supported by the monitor hardware.",
    )
    MQTT.write_text(json.dumps(json.loads(blob), indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
    print("patched mqtt/openapi_md.json")


if __name__ == "__main__":
    main()
