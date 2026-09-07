# FXR60 REST API — read-only sweep results

Real request/response captures from a live reader. One folder per endpoint,
each containing `request body/` and `response body/`.

Write-operation tests and their reports are in `cloud-certificates-PUT/` — see
[Write-operation tests](#write-operation-tests).

## Reader tested

| | |
|---|---|
| Address | `https://10.233.48.36` |
| Model | FXR60 |
| Reader application | **5.0.7** |
| Cloud agent | 0.6.2.64 |
| Radio firmware | 2.1.70.0 |
| Serial | 260975251E0049 |

Note this is a **different reader** from the one used for the MQTT work
(`10.117.229.9`, reader application 5.0.5). Findings may not transfer directly.

## Authentication

```bash
TOKEN=$(curl -sk -u 'admin:Zebra@123' \
  https://10.233.48.36/cloud/localRestLogin \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['message'])")

curl -sk -H "Authorization: Bearer $TOKEN" https://10.233.48.36/cloud/version
```

Tokens are admin role and last ~8 hours. `GET /cloud/localRestLogin` with Basic
auth mints a fresh one, so expiry is never a blocker.

## Results — 29/31 returned HTTP 200

| Endpoint | HTTP | Response | Folder |
|---|---|---|---|
| `/cloud/app-led` | ✅ 200 | json, 26 B | `cloud-app-led/` |
| `/cloud/apps` | ✅ 200 | json, 3 B | `cloud-apps/` |
| `/cloud/bleConfig` | ✅ 200 | json, 423 B | `cloud-bleConfig/` |
| `/cloud/caCertificates` | ✅ 200 | json, 3 B | `cloud-caCertificates/` |
| `/cloud/cableLossCompensation` | ✅ 200 | json, 275 B | `cloud-cableLossCompensation/` |
| `/cloud/certificates` | ✅ 200 | json, 1079 B | `cloud-certificates/` |
| `/cloud/config` | ✅ 200 | json, 9053 B | `cloud-config/` |
| `/cloud/displayConfig` | ✅ 200 | json, 209 B | `cloud-displayConfig/` |
| `/cloud/eSimConfig` | ❌ 422 | json, 114 B | `cloud-eSimConfig/` |
| `/cloud/gpi` | ✅ 200 | json, 63 B | `cloud-gpi/` |
| `/cloud/gpo` | ✅ 200 | json, 59 B | `cloud-gpo/` |
| `/cloud/hostName` | ✅ 200 | json, 32 B | `cloud-hostName/` |
| `/cloud/impinjGen2X` | ✅ 200 | empty/text, 1 B | `cloud-impinjGen2X/` |
| `/cloud/inputOutputDevices` | ✅ 200 | json, 629 B | `cloud-inputOutputDevices/` |
| `/cloud/logs` | ✅ 200 | json, 203 B | `cloud-logs/` |
| `/cloud/mode` | ✅ 200 | json, 498 B | `cloud-mode/` |
| `/cloud/network` | ✅ 200 | json, 1755 B | `cloud-network/` |
| `/cloud/networkInterfaces` | ✅ 200 | json, 106 B | `cloud-networkInterfaces/` |
| `/cloud/ntpServer` | ✅ 200 | json, 31 B | `cloud-ntpServer/` |
| `/cloud/preSelection` | ✅ 200 | json, 33 B | `cloud-preSelection/` |
| `/cloud/readPoints` | ✅ 200 | json, 45 B | `cloud-readPoints/` |
| `/cloud/readerCapabilities` | ✅ 200 | json, 4468 B | `cloud-readerCapabilities/` |
| `/cloud/readerLocation` | ✅ 200 | json, 89 B | `cloud-readerLocation/` |
| `/cloud/region` | ✅ 200 | json, 936 B | `cloud-region/` |
| `/cloud/stack-led` | ✅ 200 | json, 26 B | `cloud-stack-led/` |
| `/cloud/status` | ✅ 200 | json, 1376 B | `cloud-status/` |
| `/cloud/supportedRegionList` | ✅ 200 | json, 59 B | `cloud-supportedRegionList/` |
| `/cloud/supportedStandardList` | ✅ 200 | json, 5494 B | `cloud-supportedStandardList/` |
| `/cloud/timeZone` | ✅ 200 | json, 24 B | `cloud-timeZone/` |
| `/cloud/version` | ✅ 200 | json, 259 B | `cloud-version/` |
| `/cloud/wifiNetworks` | ❌ 422 | json, 98 B | `cloud-wifiNetworks/` |

## The two non-200 responses

Both are legitimate hardware-state reports, not faults:

| Endpoint | Reason |
|---|---|
| `/cloud/wifiNetworks` | `NETWORK INTERFACE DISABLED` — Wi-Fi is off on this reader |
| `/cloud/eSimConfig` | `eSIM slot is not active` — no eSIM provisioned |

Enable the interface or provision an eSIM and these should succeed.

## One deviation worth reporting

`GET /cloud/impinjGen2X` returns **HTTP 200 with `Content-Length: 0`** while
declaring `Content-Type: application/json`. A zero-byte body is not valid JSON, so
a strict client fails to parse it.

The spec's own `200` response for this endpoint documents an `empty` example of
`{}` — an empty JSON *object*. The reader should return `{}`, not nothing.

Minor, but it will break any client that parses responses unconditionally.

## Notes on individual endpoints

| Endpoint | Observation |
|---|---|
| `/cloud/supportedStandardList` | Requires a `region` query parameter. Called with `region=United States/Canada` |
| `/cloud/supportedRegionList` | This reader supports one region only — see the response |
| `/cloud/caCertificates` | Returns `[]` — no CA certificates installed |
| `/cloud/apps` | Returns `[]` — no user applications installed |
| `/cloud/certificates` | Several certificates present — see the response |

## Write-operation tests

Two folders hold `PUT` tests, each with request/response captures per test and a
report alongside them.

### `cloud-cloudConfig-PUT/` — endpoint configuration

14 tests covering `mqtt`, `mqtt-AWS`, `httpPost`, `WEBSOCKET` and `tcpip-server`,
plus a recovery config. Report: `CLOUDCONFIG_TEST_REPORT.md`.

Two configurations confirmed working: **plain MQTT** and **AWS IoT Core on port
443**. Headline findings: port 8883 to AWS is blocked and the error is
indistinguishable from a certificate fault; `data.event` requires a client
certificate though the schema does not say so; and several fields used by the
spec's own examples are absent from its schema, making three of six documented
connection types unconfigurable as documented.

### `cloud-certificates-PUT/` — certificate download authentication

```
cloud-certificates-PUT/
├── CERTIFICATE_AUTH_TEST_REPORT_507.md   reader app 5.0.7 — five methods, with evidence
├── CERTIFICATE_AUTH_TEST_REPORT_505.md   reader app 5.0.5 — kept for comparison
├── 01-BASIC-success/
├── 02-BEARER-header-failed/
├── 03-NONE-anonymous-failed/
├── 04-mTLS-optional-success/
└── 05-mTLS-required-failed/
```

Headline result: **Basic authentication is the only working download auth method
on both firmware versions.** `authenticationType: NONE`, Bearer tokens via
`headers`, and `installedCertificateName` for download mTLS are all accepted by the
API and then silently fail. Nothing changed between 5.0.5 and 5.0.7.

---

## What is stored, and how

Every value in these files is what was **actually sent or received** on a live
reader — no invented or illustrative data.

| File | Contents |
|---|---|
| `request body/request.json` | The real request: method, URL, headers, and body |
| `response body/response.json` | The response, when it was JSON |
| `response body/response.txt` | The response when it was **not** JSON — including genuinely empty bodies, stored as 0 bytes |
| `response body/http_status.txt` | The HTTP status code |
| `response body/verification.txt` | For write operations: how the effect was independently confirmed |

Two deliberate choices:

**Bearer tokens are not stored.** The requests used real admin JWTs minted at run
time, but a token is a live credential. Each `request.json` records the exact
command that produces one instead:

```bash
TOKEN=$(curl -sk -u 'admin:Zebra@123' \
  https://10.233.48.36/cloud/localRestLogin \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['message'])")
```

**Empty responses are stored as empty files.** The successful `PUT
/cloud/certificates` calls returned HTTP 200 with a zero-byte body. Rather than
writing a description into `response.json` as if the reader had sent one, the body
is recorded as an empty `response.txt` and the confirmation evidence sits in
`verification.txt`. So a 0-byte file means the reader really returned nothing.

Certificate PEM content, passwords, hostnames and certificate names are all stored
verbatim as sent.

---

## Reproducing

```bash
cd /home/altautoadmin/pfx_server
.venv/bin/python /tmp/rest_sweep.py
```

Read-only — GET requests only, nothing is modified.

## Endpoints not covered

This sweep covers GETs without required path parameters. Not included:

- Log downloads (`/cloud/logs/syslog`, `RcLog`, `RgErrorLog`, `RgWarningLog`,
  `radioPacketLog`) — these return compressed tar archives rather than JSON
- `/cloud/localRestLogin` — used for authentication, not a data endpoint
- All `PUT`/`DELETE` operations — these modify the reader and were deliberately
  excluded from a read-only sweep
