#!/usr/bin/env python3
import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request


READER_URL = "https://10.233.48.36/cloud/certificates"
FILE_URL = "https://10.117.229.18"

SCENARIOS = {
    "sync-success": {
        "description": "Synchronous Bearer-authenticated PFX installation.",
        "name": "scenario-sync",
        "url": f"{FILE_URL}/reader-test.pfx",
    },
    "retry-success": {
        "description": "Two file-server failures, then successful asynchronous installation.",
        "name": "scenario-retry",
        "url": f"{FILE_URL}/fail/2/reader-test.pfx",
        "retry": {
            "type": "randomWait",
            "policy": {"retries": 3, "wait": {"min": 1, "max": 2}},
        },
        "timeouts": {"connection": 5, "read": 15},
    },
    "read-timeout": {
        "description": "Slow file transfer expected to fail its HTTPS read timeout asynchronously.",
        "name": "scenario-timeout",
        "url": f"{FILE_URL}/slow/30/reader-test.pfx",
        "retry": {
            "type": "randomWait",
            "policy": {"retries": 1, "wait": {"min": 1, "max": 2}},
        },
        "timeouts": {"connection": 5, "read": 2},
    },
    "bad-file-token": {
        "description": "File-server authentication failure; no certificate should be installed.",
        "name": "scenario-bad-token",
        "url": f"{FILE_URL}/reader-test.pfx",
        "file_token": "invalid-token",
    },
}


def credential_value(name):
    credentials_path = os.path.join(os.path.dirname(__file__), ".credentials")
    try:
        with open(credentials_path, encoding="utf-8") as credentials_file:
            for line in credentials_file:
                key, separator, value = line.strip().partition("=")
                if separator and key == name:
                    return value
    except OSError as error:
        raise RuntimeError(f"cannot read {credentials_path}: {error}") from error
    raise RuntimeError(f"missing {name} in {credentials_path}")


def build_payload(scenario, file_token, pfx_password):
    payload = {
        "name": scenario["name"],
        "type": "client",
        "url": scenario["url"],
        "authenticationType": "NONE",
        "pfxPassword": pfx_password,
        "verifyPeer": False,
        "verifyHost": False,
        "headers": {"Authorization": f"Bearer {scenario.get('file_token', file_token)}"},
    }
    for field in ("retry", "timeouts"):
        if field in scenario:
            payload[field] = scenario[field]
    return payload


def main():
    parser = argparse.ArgumentParser(
        description="Run explicitly selected certificate installation test scenarios."
    )
    parser.add_argument("scenario", nargs="?", choices=SCENARIOS)
    parser.add_argument("--list", action="store_true", help="show available scenarios")
    parser.add_argument(
        "--execute", action="store_true", help="send the request to the reader"
    )
    args = parser.parse_args()

    if args.list:
        for name, scenario in SCENARIOS.items():
            print(f"{name}: {scenario['description']}")
        return
    if not args.scenario:
        parser.error("choose a scenario or use --list")

    reader_token = os.environ.get("READER_TOKEN")
    file_token = os.environ.get("FILE_TOKEN")
    if not reader_token:
        parser.error("set READER_TOKEN to the reader REST API Bearer token")
    if not file_token and "file_token" not in SCENARIOS[args.scenario]:
        parser.error("set FILE_TOKEN to the certificate file-server Bearer token")

    payload = build_payload(
        SCENARIOS[args.scenario],
        file_token,
        credential_value("PFX_READER_TEST_PASSWORD"),
    )
    display_payload = {**payload, "pfxPassword": "<redacted>"}
    print(json.dumps(display_payload, indent=2))
    if not args.execute:
        print("Dry run only. Add --execute to send this request.")
        return

    request = urllib.request.Request(
        READER_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {reader_token}",
            "Content-Type": "application/json",
        },
        method="PUT",
    )
    try:
        with urllib.request.urlopen(
            request, context=ssl._create_unverified_context(), timeout=60
        ) as response:
            print(f"Reader response: HTTP {response.status}")
            print(response.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as error:
        print(f"Reader response: HTTP {error.code}", file=sys.stderr)
        print(error.read().decode("utf-8", "replace"), file=sys.stderr)
        raise SystemExit(1) from error
    except urllib.error.URLError as error:
        print(f"Reader request failed: {error.reason}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()