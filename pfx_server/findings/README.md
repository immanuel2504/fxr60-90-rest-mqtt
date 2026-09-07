# FXR60 API findings — one folder per finding

Every finding from the REST API testing, split into its own folder with the
**request body and response body of the test(s) that prove it** — the same layout
as the `rest/<endpoint>-PUT/` test folders.

**Only findings backed by a real test are here.** Predictions, expectations and
claims that were later disproved are not given folders of their own; they are
recorded as corrections inside the finding they relate to.

```
findings/
├── settings-endpoints/     10 findings — the six settings endpoints
├── cloud-config/           10 findings — PUT /cloud/config
├── cloud-cloudconfig/       9 findings — PUT /cloud/cloudConfig
└── logs/                   10 findings — the nine Logs operations
```

Each finding folder contains:

| Path | Contents |
|---|---|
| `finding.md` | The finding: what happens, how it was proven, why it matters, what to ask Zebra |
| `request body/` | The exact request that demonstrates it |
| `response body/` | The response, HTTP status, and verification notes |
| `SOURCE.txt` | Which `rest/` test folder this evidence was copied from |

Where a finding needs more than one test to establish it — usually an A/B pair —
the evidence sits in `evidence-N-<label>/` subfolders instead, each with its own
`request body/` and `response body/`.

The `rest/` test folders remain the canonical record; these are copies kept beside
each finding so the evidence travels with it.

---

## Severity

| | Finding | Endpoint |
|---|---|---|
| 🐛 | [01 — Unresolvable NTP hostname returns 200 and wipes the setting](settings-endpoints/01-ntpserver-unresolvable-hostname-wipes-setting/finding.md) | `ntpServer` |
| 🐛 | [16 — `CLOUD_CONNECT` fires on a connection *attempt*](cloud-config/16-cloud-connect-fires-on-failed-attempt/finding.md) | `config` |
| 🔥 | [21 — AWS port 8883 blocked, 443 works — error 255 hides it](cloud-cloudconfig/21-aws-port-8883-blocked-443-works-error-hides-it/finding.md) | `cloudConfig` |
| 🔥 | [27 — `WEBSOCKET` has no working configuration at all](cloud-cloudconfig/27-websocket-has-no-working-configuration/finding.md) | both |
| 🔥 | [26 — `basicAuthentication` works but intermittently](cloud-cloudconfig/26-basicauthentication-works-but-intermittently/finding.md) | `cloudConfig` |
| ⚠️ | [29 — An accepted config is applied even if unreachable](cloud-cloudconfig/29-accepted-config-is-applied-even-if-unreachable/finding.md) | `cloudConfig` |
| 🐛 | [30 — `radio_control` log level cannot be set](logs/30-radio-control-level-cannot-be-set/finding.md) | `logs` |
| 🐛 | [31 — Three of five `componentName` values silently redirected](logs/31-component-names-silently-redirected/finding.md) | `logs` |
| ⚠️ | [38 — Log purges have no confirmation step](logs/38-purges-work-but-have-no-confirmation-step/finding.md) | `logs` |

🐛 defect · 🔥 blocks or badly slows integration · ⚠️ operational hazard

---

## settings-endpoints — the six settings endpoints

| # | Finding | Endpoint | Type |
|---|---|---|---|
| [01](settings-endpoints/01-ntpserver-unresolvable-hostname-wipes-setting/finding.md) | Unresolvable hostname returns 200 and wipes the setting | `ntpServer` | 🐛 defect |
| [02](settings-endpoints/02-oneof-branches-both-work/finding.md) | Both `oneOf` branches work — a correction | `ntpServer` | ✅ withdrawn |
| [03](settings-endpoints/03-required-fields-undeclared-in-both-directions/finding.md) | No required fields declared; both wrong, opposite directions | `app-led`, `displayConfig` | spec mismatch |
| [04](settings-endpoints/04-timezone-undocumented-input-vocabulary/finding.md) | Accepts an undocumented input vocabulary, and returns it | `timeZone` | spec mismatch |
| [05](settings-endpoints/05-region-silently-ignores-inapplicable-fields/finding.md) | Silently ignores fields it cannot apply | `region` | silent no-op |
| [06](settings-endpoints/06-region-spec-example-fails-on-us-canada-reader/finding.md) | The spec's example fails on a US/Canada reader | `region` | doc defect |
| [07](settings-endpoints/07-app-led-not-verifiable-and-cannot-reset/finding.md) | Not verifiable, and cannot be reset to `DEFAULT` | `app-led` | observability |
| [08](settings-endpoints/08-displayconfig-merges-partial-updates/finding.md) | Merges partial updates — opposite of `/cloud/config` | `displayConfig` | undocumented |
| [09](settings-endpoints/09-displayconfig-error-messages-best-and-worst/finding.md) | Best error messages on the API — and one bad one | `displayConfig` | mixed |
| [10](settings-endpoints/10-gpo-is-the-model-endpoint/finding.md) | The model the other endpoints should follow | `gpo` | ✅ positive |

Covers all six endpoints tested: `app-led`, `displayConfig`, `gpo`, `region`,
`timeZone`, `ntpServer`. Full report: [`../rest/SETTINGS_ENDPOINTS_TEST_REPORT.md`](../rest/SETTINGS_ENDPOINTS_TEST_REPORT.md)

## cloud-config — `PUT /cloud/config`

| # | Finding | Object | Type |
|---|---|---|---|
| [11](cloud-config/11-batching-retention-require-endpointconfig/finding.md) | `batching`/`retention` need `endpointConfig` | `READER-GATEWAY` | spec mismatch |
| [12](cloud-config/12-batching-dependency-is-one-way/finding.md) | The dependency runs one way only | `READER-GATEWAY` | clarification |
| [13](cloud-config/13-gpio-led-replaces-wholesale/finding.md) | `GPIO-LED` replaces wholesale — it does not merge | `GPIO-LED` | undocumented |
| [14](cloud-config/14-conditions-are-enum-strings-not-objects/finding.md) | Conditions are enum strings, not objects | `GPIO-LED` | clarification |
| [15](cloud-config/15-conditions-are-genuinely-enforced/finding.md) | Conditions are genuinely enforced at runtime | `GPIO-LED` | ✅ positive |
| [16](cloud-config/16-cloud-connect-fires-on-failed-attempt/finding.md) | `CLOUD_CONNECT` fires on a connection *attempt* | `GPIO-LED` | 🐛 defect |
| [17](cloud-config/17-gpo-actions-latch/finding.md) | GPO actions latch; the pin pair cannot show state | `GPIO-LED` | limitation |
| [18](cloud-config/18-gpio-led-does-drive-hardware/finding.md) | `GPIO-LED` does drive hardware — corrected | `GPIO-LED` | ✅ withdrawn |
| [19](cloud-config/19-gpi-events-cannot-be-triggered-via-api/finding.md) | GPI events cannot be triggered through the API | `GPIO-LED` | coverage gap |
| [20](cloud-config/20-xml-field-fails-with-core-service-timeout/finding.md) | The `xml` field fails with a Core Service timeout | `xml` | unresolved |

Full report: [`../rest/cloud-config-PUT/CONFIG_TEST_REPORT.md`](../rest/cloud-config-PUT/CONFIG_TEST_REPORT.md)

## cloud-cloudconfig — `PUT /cloud/cloudConfig`

| # | Finding | Type |
|---|---|---|
| [21](cloud-cloudconfig/21-aws-port-8883-blocked-443-works-error-hides-it/finding.md) | Port 8883 to AWS blocked; 443 works — error 255 hides it | 🔥 diagnosis |
| [22](cloud-cloudconfig/22-reader-requires-alpn-on-port-443/finding.md) | `alpnProtocolNames` is **required** on port 443 — corrected | schema gap |
| [23](cloud-cloudconfig/23-schema-is-incomplete-not-authoritative/finding.md) | The schema is incomplete, not authoritative — corrected | methodological |
| [24](cloud-cloudconfig/24-data-event-requires-client-certificate/finding.md) | `data.event` requires a client certificate | undocumented |
| [25](cloud-cloudconfig/25-installedcertificatename-needs-a-ca-alongside/finding.md) | `installedCertificateName` needs a CA alongside it | root cause |
| [26](cloud-cloudconfig/26-basicauthentication-works-but-intermittently/finding.md) | `basicAuthentication` works — but intermittently | 🔥 reliability |
| [27](cloud-cloudconfig/27-websocket-has-no-working-configuration/finding.md) | `WEBSOCKET` has no working configuration on either endpoint | 🔥 unusable |
| [28](cloud-cloudconfig/28-tcpip-server-reader-listens/finding.md) | `tcpip-server`: the reader listens — confirmed | clarification |
| [29](cloud-cloudconfig/29-accepted-config-is-applied-even-if-unreachable/finding.md) | A rejected config is safe; an accepted one is not | ⚠️ hazard |

Full report: [`../rest/cloud-cloudConfig-PUT/CLOUDCONFIG_TEST_REPORT.md`](../rest/cloud-cloudConfig-PUT/CLOUDCONFIG_TEST_REPORT.md)

## logs — the nine Logs operations

| # | Finding | Operation | Type |
|---|---|---|---|
| [30](logs/30-radio-control-level-cannot-be-set/finding.md) | `radio_control` log level cannot be set — 200, value discarded | `PUT /cloud/logs` | 🐛 defect |
| [31](logs/31-component-names-silently-redirected/finding.md) | Three of five `componentName` values silently redirected | `PUT /cloud/logs` | 🐛 defect |
| [32](logs/32-level-enum-is-per-component/finding.md) | The level enum is per-component, not shared | `PUT /cloud/logs` | spec mismatch |
| [33](logs/33-spec-put-example-is-half-ignored/finding.md) | The spec's own example is half-ignored | `PUT /cloud/logs` | doc defect |
| [34](logs/34-omitting-radiopacketlog-disables-it/finding.md) | Omitting `radioPacketLog` silently turns it off | `PUT /cloud/logs` | undocumented |
| [35](logs/35-log-gets-return-undocumented-envelope/finding.md) | All four retrievals return an undocumented envelope; no filtering | log GETs | schema gap |
| [36](logs/36-empty-log-status-code-inconsistent/finding.md) | `radioPacketLog` returns 422 when empty; `syslog` returns 200 | log GETs | ⚠️ inconsistency |
| [37](logs/37-radiopacketlog-gates-generation-not-retrieval/finding.md) | `radioPacketLog` gates generation, not retrieval | both | ✅ positive |
| [38](logs/38-purges-work-but-have-no-confirmation-step/finding.md) | Purges work and are idempotent — but no confirmation step | log DELETEs | ✅ + ⚠️ |
| [39](logs/39-logs-validation-good-with-two-gaps/finding.md) | Validation mostly good, with one gap and one inconsistency | `PUT /cloud/logs` | mixed |

All nine operations function. Full report: [`../rest/LOGS_ENDPOINTS_TEST_REPORT.md`](../rest/LOGS_ENDPOINTS_TEST_REPORT.md)

---

## Corrections — findings we withdrew or reversed

Four conclusions were wrong and were corrected by later testing. Each is kept
rather than deleted, because the reasoning that produced it recurred:

| Finding | Original claim | What testing showed |
|---|---|---|
| [02](settings-endpoints/02-oneof-branches-both-work/finding.md) | The `server1` key silently wipes the NTP setting | Confounded variable — every `server1` hostname was NXDOMAIN. `server1` works |
| [18](cloud-config/18-gpio-led-does-drive-hardware/finding.md) | The GPIO-LED engine may not be functional at all | One negative test generalised to a subsystem. It does drive hardware |
| [22](cloud-cloudconfig/22-reader-requires-alpn-on-port-443/finding.md) | `alpnProtocolNames` is output-only and must not be sent | It is **required** input on port 443 |
| [23](cloud-cloudconfig/23-schema-is-incomplete-not-authoritative/finding.md) | `httpPost`/`tcpip-server` will be rejected for schema gaps | Both accepted; `httpPost` delivers tag data end to end |

Three of the four share one root cause: **treating absence from the schema, or a
single negative result, as proof.** On this API the schema is an incomplete
description of what the validator enforces — only a test settles it.

Finding 02 is a different error: a clean 5/5 split that looked conclusive but had
two variables moving together.

---

## Related

| File | Contents |
|---|---|
| [`../rest/README.md`](../rest/README.md) | The REST endpoint captures |
| [`../rest/LOGS_ENDPOINTS_TEST_REPORT.md`](../rest/LOGS_ENDPOINTS_TEST_REPORT.md) | The nine Logs operations, 18 tests |
| [`../rest/cloud-certificates-PUT/`](../rest/cloud-certificates-PUT/) | Certificate installation tests |
| `../MQTT_API_Findings.xlsx` | Findings across both REST and MQTT |
