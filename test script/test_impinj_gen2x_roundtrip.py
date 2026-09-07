#!/usr/bin/env python3
"""PUT a simple Gen2X config, then GET /cloud/impinjGen2X and save the bodies.

Uses lab_rest.json. Does not store the login token.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

import urllib3
from requests.auth import HTTPBasicAuth

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from _paths import FAILURE_DIR, LAB_REST, SUCCESS_DIR, save_split_result, write_split_indexes

try:
    import requests
except ImportError:
    sys.exit("requests is required:  pip install requests")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PUT_BODY = {"fastID": {"enabled": True}}


def load_cfg() -> dict:
    with open(LAB_REST, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    cfg = load_cfg()
    host = str(cfg.get("host") or "").strip()
    scheme = str(cfg.get("scheme") or "https")
    user = str(cfg.get("user") or "admin")
    password = cfg.get("password")
    if not host or not password:
        print("lab_rest.json needs host and password")
        return 2
    base = f"{scheme}://{host}"
    session = requests.Session()
    session.verify = False
    session.headers["Accept"] = "application/json"
    timeout = 15

    print(f"Login {base} as {user} ...")
    try:
        login = session.get(
            f"{base}/cloud/localRestLogin",
            auth=HTTPBasicAuth(user, password),
            timeout=timeout,
        )
    except requests.RequestException as exc:
        print(f"FAIL  login: {exc}")
        return 2
    if login.status_code != 200:
        print(f"FAIL  login HTTP {login.status_code}: {login.text[:300]}")
        return 2
    token = login.json().get("message")
    if not token:
        print("FAIL  login: no token in message")
        return 2
    session.headers["Authorization"] = f"Bearer {token}"

    before = session.get(f"{base}/cloud/impinjGen2X", timeout=timeout)
    print(f"GET before  HTTP {before.status_code}  {before.text!r}")

    put = session.put(f"{base}/cloud/impinjGen2X", json=PUT_BODY, timeout=timeout)
    print(f"PUT fastID  HTTP {put.status_code}  {put.text!r}")

    after = session.get(f"{base}/cloud/impinjGen2X", timeout=timeout)
    print(f"GET after   HTTP {after.status_code}  {after.text!r}")

    def parse(resp):
        text = (resp.text or "").strip()
        if not text:
            return {}
        try:
            return resp.json()
        except ValueError:
            return {"_raw": resp.text}

    result = {
        "verdict": "PASS" if after.status_code == 200 and put.status_code == 200 else "FAIL",
        "method": "GET",
        "url_path": "/cloud/impinjGen2X",
        "step": "configure fastID then GET",
        "when": datetime.now(timezone.utc).isoformat(),
        "put_request": PUT_BODY,
        "put_status": put.status_code,
        "put_body": parse(put),
        "get_before_status": before.status_code,
        "get_before": parse(before),
        "get_after_status": after.status_code,
        "get_after": parse(after),
    }
    path = save_split_result("GET_cloud_impinjGen2X_after_fastID", result)
    write_split_indexes()
    print(f"saved {path}")
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
