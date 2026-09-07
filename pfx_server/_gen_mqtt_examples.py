#!/usr/bin/env python3
"""One-shot generator: build mqtt/examples/<command>/request/*.json from the
REST OpenAPI spec's own body examples, keyed by the spec's documented
'MQTT Command' value. Run once; not imported by test_mqtt_api.py."""
import json
import os
import re

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC_PATH = os.path.join(HERE, "FXR_60-90_rest_api.yaml")
OUT_DIR = os.path.join(HERE, "mqtt", "examples")

METHODS = ("get", "put", "post", "delete", "patch")

# Spec lists this as "set_updateCertificate (set_update_cert)" - the wire
# command is the first token.
CMD_OVERRIDES = {
    "set_updateCertificate (set_update_cert)": "set_updateCertificate",
}

# get_mode's spec example is a GET-with-body oddity; give it a clean name so
# PREFERRED_REQUEST in test_mqtt_api.py resolves.
FILENAME_OVERRIDES = {
    ("get_mode", "example"): "default_configured_only.json",
}


def slugify(name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9_]+", "_", name).strip("_")
    return name or "default"


def main() -> None:
    with open(SPEC_PATH, encoding="utf-8") as fh:
        spec = yaml.safe_load(fh)

    written = 0
    commands = 0
    for path, item in spec.get("paths", {}).items():
        if not isinstance(item, dict):
            continue
        for method, op in item.items():
            if method not in METHODS or not isinstance(op, dict):
                continue
            desc = op.get("description", "")
            m = re.search(r"MQTT Command \| `([^`]+)`", desc)
            if not m:
                continue
            command = CMD_OVERRIDES.get(m.group(1), m.group(1))
            media = ((op.get("requestBody") or {}).get("content") or {}).get(
                "application/json"
            ) or {}

            bodies = []  # list of (filename, body_dict)
            if "example" in media:
                fname = FILENAME_OVERRIDES.get((command, "example"), "default.json")
                bodies.append((fname, media["example"]))
            elif "examples" in media:
                for ex_name, wrapper in media["examples"].items():
                    value = wrapper.get("value") if isinstance(wrapper, dict) else wrapper
                    if value is None:
                        continue
                    bodies.append((f"{slugify(ex_name)}.json", value))

            if not bodies:
                # No declared body (GET, or POST/PUT with no example) - still
                # register the command with an empty payload so it's discovered.
                bodies.append(("default.json", {}))

            folder = os.path.join(OUT_DIR, command, "request")
            os.makedirs(folder, exist_ok=True)
            for fname, body in bodies:
                envelope = {
                    "command": command,
                    "payload": body if isinstance(body, dict) else {"value": body},
                }
                with open(os.path.join(folder, fname), "w", encoding="utf-8") as out:
                    json.dump(envelope, out, indent=2)
                    out.write("\n")
                written += 1
            commands += 1

    print(f"{commands} commands, {written} request files -> {OUT_DIR}")


if __name__ == "__main__":
    main()
