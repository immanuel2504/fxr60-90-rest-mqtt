#!/usr/bin/env python3
"""Exercise the FXR60/FXR90 REST API against a live reader, one endpoint at a time.

Reads FXR_60-90_rest_api.yaml, builds a request for every operation from the
spec's own examples, calls the reader, and reports two things per endpoint:

  1. Did it work?           HTTP status, latency, response body
  2. Does it match the doc? response validated against the referenced schema,
                            with undocumented / missing fields listed

Endpoints are grouped into three tiers. Only `read` runs by default:

  read    GET operations. No side effects.
  write   Config changes that are reversible (LED, hostname, timezone, mode,
          inventory start/stop, ...). Requires --tier write.
  danger  Reboot, OS update, password change, network reconfig, certificate
          and app install/delete, log deletion. Requires --tier danger AND
          --confirm-danger. These can drop your connection or brick a session.

Usage
-----
  # read-only sweep (safe)
  python test_rest_api.py --host 10.0.0.42 --user admin --password 'PASSWORD'

  # one endpoint / a subset
  python test_rest_api.py --host 10.0.0.42 --user admin -p PW --only caCert

  # the CA-certificate lifecycle, end to end, with a real PEM
  python test_rest_api.py --host 10.0.0.42 --user admin -p PW \
      --flow ca-certificates --pem ./AmazonRootCA1.pem

  # show what would be called, contact nothing
  python test_rest_api.py --list --tier read --tier write

Reports land in rest/scripts/reports/ as .md and .json.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import OrderedDict
from typing import Any

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required:  pip install pyyaml")

try:
    import requests
    from requests.auth import HTTPBasicAuth
except ImportError:
    sys.exit("requests is required:  pip install requests")

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HERE = os.path.dirname(os.path.abspath(__file__))
REST_DIR = os.path.dirname(HERE)
SPEC = os.path.join(REST_DIR, "FXR_60-90_rest_api.yaml")
EXAMPLES_DIR = os.path.join(REST_DIR, "operation_examples")
REPORT_DIR = os.path.join(HERE, "reports")

METHODS = ("get", "put", "post", "delete", "patch")

# ---------------------------------------------------------------------------
# Tier classification. Anything not listed here defaults to: GET -> read,
# everything else -> danger (fail safe, not fail open).
# ---------------------------------------------------------------------------
WRITE_OPS = {
    "setAppled", "setStackled", "setGpo", "setHostName", "setTimezone",
    "setCablelosscompensation", "setBleConfig", "setImpinjGen2X", "setLogs",
    "setMode", "setRegion", "setConfigMqtt", "setEsimConfig", "updateNtpServer",
    "setDataToRG", "setAutostartuserapp", "setPassthru", "setReqtouserapp",
    "startInventory", "stopInventory", "setStartuserapp", "setStopuserapp",
    "PUT /cloud/preSelection",
}
DANGER_OPS = {
    "reboot", "setOs", "setRevertbackos", "updatePassword", "updateNetwork",
    "setImportcloudconfig", "setUpdatecertificate", "setRefreshcertificate",
    "delCertificate", "setInstallCACertificate", "delCACertificate",
    "setInstalluserapp", "setUninstalluserapp",
    "DELETE /cloud/logs/syslog", "DELETE /cloud/logs/radioPacketLog",
}

RESET = "\033[0m"
COLOR = {
    "PASS": "\033[32m", "WARN": "\033[33m", "FAIL": "\033[31m",
    "SKIP": "\033[90m", "head": "\033[1m",
}


def paint(text: str, key: str, enabled: bool) -> str:
    return f"{COLOR[key]}{text}{RESET}" if enabled and key in COLOR else text


# ---------------------------------------------------------------------------
# Spec loading
# ---------------------------------------------------------------------------
def load_spec(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def deref(node: Any, spec: dict, seen: int = 0) -> Any:
    """Resolve local $refs. Depth-capped so a recursive schema can't hang us."""
    while isinstance(node, dict) and "$ref" in node and seen < 50:
        target = node["$ref"]
        if not target.startswith("#/"):
            return {}
        cur: Any = spec
        for part in target[2:].split("/"):
            if not isinstance(cur, dict) or part not in cur:
                return {}
            cur = cur[part]
        node, seen = cur, seen + 1
    return node


def path_slug(path: str) -> str:
    """/cloud/apps/{appname}/autostart -> cloud-apps-appname-autostart"""
    return path.strip("/").replace("{", "").replace("}", "").replace("/", "-").lower()


def op_key(method: str, path: str, op: dict) -> str:
    """operationId when present, else 'METHOD /path' (9 operations lack one)."""
    return op.get("operationId") or f"{method.upper()} {path}"


def tier_of(key: str, method: str) -> str:
    if key in DANGER_OPS:
        return "danger"
    if key in WRITE_OPS:
        return "write"
    return "read" if method == "get" else "danger"


# ---------------------------------------------------------------------------
# Request construction, entirely from spec + operation_examples
# ---------------------------------------------------------------------------
def load_param_overrides(path: str, overrides: dict) -> dict:
    """Merge, lowest precedence first: examples/parameters.json < --param."""
    values: dict[str, Any] = {}
    slug = path_slug(path)
    for candidate in (
        os.path.join(EXAMPLES_DIR, slug, "parameters.json"),
    ):
        if os.path.isfile(candidate):
            try:
                with open(candidate, encoding="utf-8") as fh:
                    data = json.load(fh)
                for name, meta in (data or {}).items():
                    if isinstance(meta, dict) and "example" in meta:
                        values[name] = meta["example"]
            except (OSError, json.JSONDecodeError):
                pass
    values.update(overrides)
    return values


def collect_params(item: dict, op: dict, spec: dict) -> list[dict]:
    params = []
    for src in (item.get("parameters") or [], op.get("parameters") or []):
        for p in src:
            p = deref(p, spec)
            if isinstance(p, dict) and p.get("name"):
                params.append(p)
    return params


def pick_example(container: dict) -> tuple[Any, str | None]:
    """Return (value, example_name) from an OpenAPI media-type object."""
    if "example" in container:
        return container["example"], "example"
    examples = container.get("examples") or {}
    for name, wrapper in examples.items():
        if isinstance(wrapper, dict) and "value" in wrapper:
            return wrapper["value"], name
        return wrapper, name
    return None, None


def body_from_examples_dir(path: str, method: str) -> tuple[Any, str | None]:
    """Fall back to rest/operation_examples/<slug>/<METHOD>/*.json."""
    folder = os.path.join(EXAMPLES_DIR, path_slug(path), method.upper())
    if not os.path.isdir(folder):
        return None, None
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".json") or name == "parameters.json":
            continue
        if name in ("success.json", "error.json"):  # response-side examples
            continue
        try:
            with open(os.path.join(folder, name), encoding="utf-8") as fh:
                return json.load(fh), f"{method.upper()}/{name}"
        except (OSError, json.JSONDecodeError):
            continue
    return None, None


# ---------------------------------------------------------------------------
# Lightweight schema check (jsonschema is optional / often broken on Windows)
# ---------------------------------------------------------------------------
TYPE_MAP = {
    "object": dict, "array": list, "string": str, "boolean": bool,
    "number": (int, float), "integer": int, "null": type(None),
}


def check_schema(value: Any, schema: Any, spec: dict, where: str = "$",
                 depth: int = 0) -> tuple[list[str], list[str], list[str]]:
    """Return (violations, undocumented_fields, missing_documented_fields)."""
    bad: list[str] = []
    extra: list[str] = []
    missing: list[str] = []
    schema = deref(schema, spec)
    if not isinstance(schema, dict) or depth > 12:
        return bad, extra, missing

    for combiner in ("oneOf", "anyOf", "allOf"):
        if combiner in schema:  # best-effort: don't guess a branch
            return bad, extra, missing

    expected = schema.get("type")
    if expected:
        wanted = expected if isinstance(expected, list) else [expected]
        pytypes = tuple(
            t for name in wanted for t in
            (TYPE_MAP.get(name, object) if isinstance(TYPE_MAP.get(name), tuple)
             else (TYPE_MAP.get(name, object),))
        )
        # bool is a subclass of int; keep them distinct
        if isinstance(value, bool) and "boolean" not in wanted:
            bad.append(f"{where}: expected {expected}, got boolean")
            return bad, extra, missing
        if not isinstance(value, pytypes):
            bad.append(f"{where}: expected {expected}, got {type(value).__name__}")
            return bad, extra, missing

    if "enum" in schema and value not in schema["enum"]:
        bad.append(f"{where}: {value!r} not in enum {schema['enum']}")

    if isinstance(value, dict):
        props = schema.get("properties") or {}
        for name in schema.get("required") or []:
            if name not in value:
                bad.append(f"{where}.{name}: required by schema but absent in response")
        if props:
            for name in value:
                if str(name) not in {str(k) for k in props}:
                    extra.append(f"{where}.{name}")
            for name in props:
                if str(name) not in {str(k) for k in value}:
                    missing.append(f"{where}.{name}")
            for name, sub in props.items():
                if str(name) in {str(k) for k in value}:
                    actual_key = next(k for k in value if str(k) == str(name))
                    b, e, m = check_schema(value[actual_key], sub, spec,
                                           f"{where}.{name}", depth + 1)
                    bad += b
                    extra += e
                    missing += m

    if isinstance(value, list) and schema.get("items"):
        for idx, entry in enumerate(value[:5]):  # sample, don't spam
            b, e, m = check_schema(entry, schema["items"], spec,
                                   f"{where}[{idx}]", depth + 1)
            bad += b
            extra += e
            missing += m

    return bad, extra, missing


# ---------------------------------------------------------------------------
# Planning
# ---------------------------------------------------------------------------
class Call:
    def __init__(self, method, path, op, item, spec, args):
        self.method = method
        self.path = path
        self.op = op
        self.key = op_key(method, path, op)
        self.tier = tier_of(self.key, method)
        self.summary = op.get("summary", "")
        self.skip_reason: str | None = None

        params = collect_params(item, op, spec)
        supplied = load_param_overrides(path, args.param)
        self.query: dict[str, Any] = {}
        self.url_path = path
        for p in params:
            name, loc = p["name"], p.get("in")
            if name in supplied:
                val = supplied[name]
            elif "example" in p:
                val = p["example"]
            elif isinstance(p.get("schema"), dict) and "example" in p["schema"]:
                val = p["schema"]["example"]
            else:
                if p.get("required"):
                    self.skip_reason = f"no value for required {loc} param '{name}' (pass --param {name}=...)"
                continue
            if loc == "path":
                self.url_path = self.url_path.replace("{" + name + "}", str(val))
            elif loc == "query":
                self.query[name] = val

        media = ((op.get("requestBody") or {}).get("content") or {}).get("application/json") or {}
        self.body, self.body_source = pick_example(media)
        if self.body is None and media:
            self.body, self.body_source = body_from_examples_dir(path, method)
        if self.body is None and method in ("put", "post", "patch") and media:
            self.skip_reason = "operation declares a JSON body but the spec carries no example"

        self.responses = op.get("responses") or {}


def build_plan(spec: dict, args) -> list[Call]:
    plan = []
    for path, item in spec.get("paths", {}).items():
        if not isinstance(item, dict):
            continue
        for method, op in item.items():
            if method not in METHODS or not isinstance(op, dict):
                continue
            if path == "/cloud/localRestLogin":
                continue  # handled by the auth step
            call = Call(method, path, op, item, spec, args)
            label = f"{call.method.upper()} {call.path} {call.key}"
            if args.only and not any(re.search(pat, label, re.I) for pat in args.only):
                continue
            if args.skip and any(re.search(pat, label, re.I) for pat in args.skip):
                continue
            plan.append(call)
    plan.sort(key=lambda c: (c.path, c.method))
    return plan


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------
def login(session: requests.Session, base: str, user: str, password: str,
          timeout: float) -> str:
    url = f"{base}/cloud/localRestLogin"
    resp = session.get(url, auth=HTTPBasicAuth(user, password), timeout=timeout)
    resp.raise_for_status()
    payload = resp.json()
    token = payload.get("message")
    if not token:
        raise RuntimeError(f"login returned no token: {payload}")
    return token


def run_call(session: requests.Session, base: str, call: Call, spec: dict,
             timeout: float) -> dict:
    result = {
        "operationId": call.key, "method": call.method.upper(), "path": call.path,
        "url_path": call.url_path, "tier": call.tier, "summary": call.summary,
        "query": call.query, "body_source": call.body_source,
        "status": None, "ms": None, "verdict": "SKIP", "notes": [],
        "response_preview": None,
        "schema_violations": [], "undocumented_fields": [], "missing_fields": [],
    }
    if call.skip_reason:
        result["notes"].append(call.skip_reason)
        return result

    url = base + call.url_path
    body = call.body
    if call.method == "get" and body is not None:
        # GET /cloud/mode declares a requestBody in the spec. Don't send one —
        # note it instead, since a body on GET is almost certainly a spec defect.
        result["notes"].append("spec declares a requestBody on a GET; body not sent")
        body = None

    started = time.perf_counter()
    try:
        resp = session.request(
            call.method.upper(), url,
            params=call.query or None,
            json=body if body is not None else None,
            timeout=timeout,
        )
    except requests.RequestException as exc:
        result["ms"] = round((time.perf_counter() - started) * 1000, 1)
        result["verdict"] = "FAIL"
        result["notes"].append(f"transport error: {type(exc).__name__}: {exc}")
        return result

    result["ms"] = round((time.perf_counter() - started) * 1000, 1)
    result["status"] = resp.status_code

    ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip()
    result["content_type"] = ctype
    try:
        parsed = resp.json()
        result["response_preview"] = json.dumps(parsed)[:600]
    except ValueError:
        parsed = None
        result["response_preview"] = resp.text[:600]
        if resp.text.strip():
            result["notes"].append(f"response is not JSON (Content-Type: {ctype or 'unset'})")

    code = str(resp.status_code)
    if code not in result_codes(call.responses):
        result["notes"].append(
            f"HTTP {code} is not documented for this operation "
            f"(spec lists: {', '.join(sorted(result_codes(call.responses))) or 'none'})"
        )

    if not resp.ok:
        result["verdict"] = "FAIL"
        return result

    documented = (call.responses.get(code)
                  or call.responses.get("200")
                  or call.responses.get("default") or {})
    media = ((documented.get("content") or {}).get("application/json") or {})
    schema = media.get("schema")
    if schema is not None and parsed is not None:
        bad, extra, missing = check_schema(parsed, schema, spec)
        result["schema_violations"] = bad
        result["undocumented_fields"] = extra
        result["missing_fields"] = missing

    result["verdict"] = "WARN" if (result["schema_violations"]
                                   or result["undocumented_fields"]
                                   or result["notes"]) else "PASS"
    return result


def result_codes(responses: dict) -> set[str]:
    return {str(c) for c in responses if str(c).isdigit()}


# ---------------------------------------------------------------------------
# CA-certificate lifecycle flow (the endpoints reported as not working)
# ---------------------------------------------------------------------------
def flow_ca_certificates(session, base, args, spec) -> list[dict]:
    """GET list -> PUT install -> GET list (present?) -> DELETE -> GET list (gone?)"""
    steps: list[dict] = []
    name = args.param.get("caname", "test-ca-" + str(int(time.time())))

    def record(label, method, path, **kw):
        started = time.perf_counter()
        try:
            resp = session.request(method, base + path, timeout=args.timeout, **kw)
            ms = round((time.perf_counter() - started) * 1000, 1)
            try:
                parsed = resp.json()
            except ValueError:
                parsed = resp.text
            step = {"step": label, "method": method, "path": path,
                    "status": resp.status_code, "ms": ms,
                    "verdict": "PASS" if resp.ok else "FAIL",
                    "response_preview": json.dumps(parsed)[:600] if not isinstance(parsed, str) else parsed[:600],
                    "notes": [], "parsed": parsed}
        except requests.RequestException as exc:
            step = {"step": label, "method": method, "path": path, "status": None,
                    "ms": round((time.perf_counter() - started) * 1000, 1),
                    "verdict": "FAIL", "response_preview": None,
                    "notes": [f"transport error: {exc}"], "parsed": None}
        steps.append(step)
        return step

    def finish() -> list[dict]:
        """Annotate the baseline, then drop parsed bodies before reporting."""
        baseline = before.get("parsed")
        if isinstance(baseline, list):
            before["notes"].append(f"{len(baseline)} CA certificate(s) installed at start: "
                                   f"{', '.join(map(str, baseline)) or '(none)'}")
        for step in steps:
            step.pop("parsed", None)
        return steps

    before = record("list CA certificates (baseline)", "GET", "/cloud/caCertificates")

    if not args.pem:
        steps.append({"step": "install CA certificate", "method": "PUT",
                      "path": f"/cloud/caCertificates/{name}", "status": None,
                      "ms": None, "verdict": "SKIP", "response_preview": None,
                      "notes": ["no --pem supplied; the PEM in the spec examples is "
                                "placeholder text and will not install"], "parsed": None})
        return finish()

    with open(args.pem, encoding="utf-8") as fh:
        pem = fh.read()
    if "BEGIN CERTIFICATE" not in pem:
        steps.append({"step": "install CA certificate", "method": "PUT",
                      "path": f"/cloud/caCertificates/{name}", "status": None,
                      "ms": None, "verdict": "SKIP", "response_preview": None,
                      "notes": [f"{args.pem} does not look like a PEM certificate"],
                      "parsed": None})
        return finish()

    # The spec marks only `content` as required and says `name` is MQTT-only,
    # so send the path-parameter form first, then retry with `name` in the body.
    install = record(f"install CA certificate '{name}' (content only)", "PUT",
                     f"/cloud/caCertificates/{name}", json={"content": pem})
    if install["verdict"] == "FAIL":
        install["notes"].append("retrying with `name` included in the body")
        record(f"install CA certificate '{name}' (name + content)", "PUT",
               f"/cloud/caCertificates/{name}",
               json={"name": name, "content": pem})

    after = record("list CA certificates (after install)", "GET", "/cloud/caCertificates")
    if isinstance(after.get("parsed"), list):
        if name in after["parsed"]:
            after["notes"].append(f"'{name}' is present — install confirmed")
        else:
            after["verdict"] = "FAIL"
            after["notes"].append(
                f"'{name}' absent after a successful install call — the reader "
                "accepted the request but did not persist the certificate, or it "
                "stored it under a different name")

    if args.keep:
        steps.append({"step": "delete CA certificate", "method": "DELETE",
                      "path": f"/cloud/caCertificates/{name}", "status": None,
                      "ms": None, "verdict": "SKIP", "response_preview": None,
                      "notes": ["--keep set; leaving the certificate installed"],
                      "parsed": None})
        return finish()

    record(f"delete CA certificate '{name}'", "DELETE", f"/cloud/caCertificates/{name}")
    final = record("list CA certificates (after delete)", "GET", "/cloud/caCertificates")
    if isinstance(final.get("parsed"), list):
        if name in final["parsed"]:
            final["verdict"] = "FAIL"
            final["notes"].append(f"'{name}' still present after DELETE")
        else:
            final["notes"].append(f"'{name}' removed — delete confirmed")

    return finish()


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
def print_row(res: dict, color: bool) -> None:
    verdict = res["verdict"]
    status = res.get("status") or "-"
    ms = f"{res['ms']:>7.1f}ms" if res.get("ms") is not None else "         -"
    line = (f"  {paint(verdict.ljust(4), verdict, color)}  "
            f"{res['method']:<6} {res.get('url_path', res['path']):<44} "
            f"{str(status):>4} {ms}")
    print(line)
    for note in res.get("notes", []):
        print(paint(f"          - {note}", "WARN" if verdict != "FAIL" else "FAIL", color))
    for field in res.get("schema_violations", [])[:6]:
        print(paint(f"          ! schema: {field}", "WARN", color))
    if res.get("undocumented_fields"):
        shown = ", ".join(f.lstrip("$.") for f in res["undocumented_fields"][:8])
        more = "" if len(res["undocumented_fields"]) <= 8 else f" (+{len(res['undocumented_fields']) - 8} more)"
        print(paint(f"          ? undocumented in spec: {shown}{more}", "WARN", color))
    if res.get("missing_fields"):
        shown = ", ".join(f.lstrip("$.") for f in res["missing_fields"][:8])
        more = "" if len(res["missing_fields"]) <= 8 else f" (+{len(res['missing_fields']) - 8} more)"
        print(paint(f"          ? documented but not returned: {shown}{more}", "SKIP", color))


def write_reports(results: list[dict], flow: list[dict], meta: dict) -> tuple[str, str]:
    os.makedirs(REPORT_DIR, exist_ok=True)
    stamp = meta["started"].replace(":", "").replace("-", "").replace(" ", "-")
    json_path = os.path.join(REPORT_DIR, f"api_test_{stamp}.json")
    md_path = os.path.join(REPORT_DIR, f"api_test_{stamp}.md")

    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump({"meta": meta, "results": results, "flow": flow}, fh, indent=2)

    counts = OrderedDict((v, sum(1 for r in results if r["verdict"] == v))
                         for v in ("PASS", "WARN", "FAIL", "SKIP"))
    lines = [
        f"# FXR60/FXR90 REST API test run",
        "",
        f"- Reader: `{meta['host']}`",
        f"- Started: {meta['started']}",
        f"- Tiers exercised: {', '.join(meta['tiers'])}",
        f"- Spec: `{os.path.relpath(SPEC, REST_DIR)}`",
        "",
        "| Verdict | Count |",
        "|---|---|",
    ]
    lines += [f"| {k} | {v} |" for k, v in counts.items()]
    lines += ["", "## Endpoints", "",
              "| Verdict | Method | Path | HTTP | ms | Notes |", "|---|---|---|---|---|---|"]
    for r in results:
        notes = r.get("notes", [])[:]
        if r.get("schema_violations"):
            notes.append(f"{len(r['schema_violations'])} schema violation(s)")
        if r.get("undocumented_fields"):
            notes.append(f"{len(r['undocumented_fields'])} undocumented field(s)")
        if r.get("missing_fields"):
            notes.append(f"{len(r['missing_fields'])} documented field(s) not returned")
        escaped = "; ".join(n.replace("|", r"\|") for n in notes)
        lines.append(
            f"| {r['verdict']} | {r['method']} | `{r.get('url_path', r['path'])}` | "
            f"{r.get('status') or '-'} | {r.get('ms') or '-'} | {escaped} |"
        )

    findings = [r for r in results if r.get("schema_violations")
                or r.get("undocumented_fields") or r.get("missing_fields")]
    if findings:
        lines += ["", "## Spec-conformance findings", ""]
        for r in findings:
            lines.append(f"### `{r['method']} {r['path']}` ({r['operationId']})")
            for v in r["schema_violations"]:
                lines.append(f"- **violation** {v}")
            for f in r["undocumented_fields"]:
                lines.append(f"- undocumented in spec: `{f}`")
            for f in r["missing_fields"]:
                lines.append(f"- documented but not returned: `{f}`")
            lines.append("")

    if flow:
        lines += ["", "## Flow", "", "| Verdict | Step | HTTP | ms | Notes |",
                  "|---|---|---|---|---|"]
        for s in flow:
            lines.append(f"| {s['verdict']} | {s['step']} | {s.get('status') or '-'} | "
                         f"{s.get('ms') or '-'} | {'; '.join(s.get('notes', []))} |")

    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return md_path, json_path


# ---------------------------------------------------------------------------
def parse_args(argv=None):
    ap = argparse.ArgumentParser(
        description="Test FXR60/FXR90 REST endpoints one by one against a reader.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Usage\n-----\n")[-1],
    )
    ap.add_argument("--host", help="reader IP or hostname (env FXR_HOST)")
    ap.add_argument("--user", default=os.environ.get("FXR_USER", "admin"),
                    help="admin username (env FXR_USER, default: admin)")
    ap.add_argument("-p", "--password", help="admin password (env FXR_PASSWORD)")
    ap.add_argument("--token", help="bearer token; skips the login call (env FXR_TOKEN)")
    ap.add_argument("--scheme", default="https", choices=["https", "http"])
    ap.add_argument("--tier", action="append", choices=["read", "write", "danger"],
                    help="tiers to exercise; repeatable. Default: read")
    ap.add_argument("--confirm-danger", action="store_true",
                    help="required alongside --tier danger; these calls can reboot "
                         "the reader, change its password, or cut its network")
    ap.add_argument("--only", action="append", default=[],
                    help="regex filter on 'METHOD /path operationId'; repeatable")
    ap.add_argument("--skip", action="append", default=[],
                    help="regex to exclude; repeatable")
    ap.add_argument("--param", action="append", default=[], metavar="NAME=VALUE",
                    help="path/query parameter value, e.g. --param appname=mylogger")
    ap.add_argument("--flow", choices=["ca-certificates"],
                    help="run a stateful lifecycle check instead of a flat sweep")
    ap.add_argument("--pem", help="path to a real PEM CA certificate for --flow")
    ap.add_argument("--keep", action="store_true",
                    help="in --flow, do not delete what was installed")
    ap.add_argument("--timeout", type=float, default=30.0)
    ap.add_argument("--delay", type=float, default=0.0,
                    help="seconds to pause between calls")
    ap.add_argument("--list", action="store_true",
                    help="print the plan and exit; contacts nothing")
    ap.add_argument("--verify-tls", action="store_true",
                    help="verify the reader certificate (off by default: self-signed)")
    ap.add_argument("--no-color", action="store_true")
    args = ap.parse_args(argv)

    args.host = args.host or os.environ.get("FXR_HOST")
    args.password = args.password or os.environ.get("FXR_PASSWORD")
    args.token = args.token or os.environ.get("FXR_TOKEN")
    args.tier = args.tier or ["read"]

    overrides = {}
    for entry in args.param:
        if "=" not in entry:
            ap.error(f"--param expects NAME=VALUE, got {entry!r}")
        name, value = entry.split("=", 1)
        overrides[name] = value
    args.param = overrides

    if "danger" in args.tier and not args.confirm_danger and not args.list:
        ap.error("--tier danger also requires --confirm-danger")
    if not args.list:
        if not args.host:
            ap.error("--host is required (or set FXR_HOST)")
        if not args.token and not args.password:
            ap.error("--password or --token is required (or set FXR_PASSWORD/FXR_TOKEN)")
    return args


def main(argv=None) -> int:
    args = parse_args(argv)
    color = not args.no_color and sys.stdout.isatty()
    spec = load_spec(SPEC)
    plan = build_plan(spec, args)
    selected = [c for c in plan if c.tier in args.tier]

    if args.list:
        print(paint(f"{len(plan)} operation(s) in spec, {len(selected)} selected "
                    f"(tiers: {', '.join(args.tier)})", "head", color))
        for call in plan:
            mark = "x" if call.tier in args.tier else " "
            body = f"  body<-{call.body_source}" if call.body_source else ""
            note = f"  SKIP: {call.skip_reason}" if call.skip_reason else ""
            print(f" [{mark}] {call.tier:<6} {call.method.upper():<6} "
                  f"{call.url_path:<46} {call.key}{body}{note}")
        return 0

    base = f"{args.scheme}://{args.host}"
    session = requests.Session()
    session.verify = args.verify_tls
    session.headers["Accept"] = "application/json"

    if args.token:
        token = args.token
        print(paint("Using supplied bearer token", "head", color))
    else:
        print(paint(f"Logging in to {base} as {args.user} ...", "head", color))
        try:
            token = login(session, base, args.user, args.password, args.timeout)
        except Exception as exc:
            print(paint(f"FAIL  login: {exc}", "FAIL", color))
            return 2
        print(paint(f"  token acquired ({len(token)} chars)", "PASS", color))
    session.headers["Authorization"] = f"Bearer {token}"

    meta = {
        "host": args.host, "user": args.user, "tiers": args.tier,
        "started": time.strftime("%Y-%m-%d %H:%M:%S"),
        "spec": os.path.relpath(SPEC, REST_DIR),
    }

    flow: list[dict] = []
    results: list[dict] = []

    if args.flow == "ca-certificates":
        print(paint("\nFlow: CA-certificate lifecycle", "head", color))
        flow = flow_ca_certificates(session, base, args, spec)
        for step in flow:
            print(f"  {paint(step['verdict'].ljust(4), step['verdict'], color)}  "
                  f"{step['method']:<6} {step['path']:<44} {step.get('status') or '-'}")
            for note in step.get("notes", []):
                print(paint(f"          - {note}", "WARN", color))
    else:
        print(paint(f"\n{len(selected)} endpoint(s) to exercise "
                    f"(tiers: {', '.join(args.tier)})\n", "head", color))
        for call in selected:
            res = run_call(session, base, call, spec, args.timeout)
            results.append(res)
            print_row(res, color)
            if args.delay:
                time.sleep(args.delay)

    md_path, json_path = write_reports(results, flow, meta)

    every = results or flow
    counts = {v: sum(1 for r in every if r["verdict"] == v)
              for v in ("PASS", "WARN", "FAIL", "SKIP")}
    print(paint("\nSummary", "head", color))
    for verdict, count in counts.items():
        if count:
            print(f"  {paint(verdict, verdict, color)}  {count}")
    print(f"\nReports:\n  {md_path}\n  {json_path}")
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
