# FXR60 `PUT /cloud/cloudConfig` — Endpoint Configuration Test Report

Every cloudConfig test run so far, with real request bodies and responses in the
numbered folders beside this report.

## Scope

| | |
|---|---|
| Endpoint | `PUT /cloud/cloudConfig` (MQTT: `set_importCloudConfig`) |
| Readers | `10.117.229.9` (reader app 5.0.5) for MQTT and AWS work; `10.233.48.36` (5.0.7) for REST |
| Connection types documented | `mqtt`, `mqtt-AWS`, `mqtt-Azure`, `httpPost`, `WEBSOCKET`, `tcpip-server` |
| Tested here | `mqtt`, `mqtt-AWS`, and the three non-MQTT types. `mqtt-Azure` skipped by request |

---

## Results

| # | Test | Type | Result |
|---|---|---|---|
| 01 | Plain MQTT, port 1883 | `mqtt` | ✅ **Working** |
| 02 | TLS 8883, CA-only security | `mqtt` | ❌ Rejected — data.event needs a client cert |
| 03 | mTLS 8884, file paths | `mqtt` | ✅ **Working** |
| 04 | mTLS 8884, cert store | `mqtt` | ❌ Accepted, TLS fails — `unknown ca`, no CA supplied |
| 04b | mTLS 8884, cert store **+ CA** | `mqtt` | ✅ **Working** — resolves 04 |
| 05 | AWS, installedCert, port 8883 | `mqtt-AWS` | ❌ Accepted but never connected |
| 06 | AWS, installedCert, port 443 | `mqtt-AWS` | ✅ **Working** |
| 07 | AWS, inline `*FileContent` | `mqtt-AWS` | ❌ Rejected — fields not in schema |
| 08 | AWS, `*FileLocation` | `mqtt-AWS` | ✅ **Working** — needs `alpnProtocolNames` |
| 09 | Username/password, port 1884 | `mqtt` | ⚠️ **Works, but intermittent** |
| 10 | httpPost | `httpPost` | ✅ **Working, tag data delivered** |
| 11 | WebSocket, spec shape | `WEBSOCKET` | ⚠️ Accepted, never connects |
| 12 | WebSocket, endpoint added | `WEBSOCKET` | ❌ Rejected — security accepts only `verifyPeer` |
| 13 | tcpip-server | `tcpip-server` | ✅ **Accepted — reader listens on 8081** |
| 99 | Rollback to reader's own broker | `mqtt` | ✅ **Working** (recovery) |

Confirmed working end to end: **plain MQTT** (01), **mTLS by file paths** (03),
**mTLS via cert store + CA** (04b), **AWS on port 443** with both
`installedCertificateName` (06) and `*FileLocation` (08), and **httpPost** (10),
which delivered 170 real tag events. `tcpip-server` (13) is accepted and the
reader listens as designed.

Two remain unusable: **`WEBSOCKET`** on any shape (11, 12) and
**`basicAuthentication`**, which works only intermittently (09).

> **Note.** This table was stale for a period — tests 03, 08, 10, 11, 12 and 13
> were recorded as "Untested" after they had in fact been run, and the
> `Findings` section below still carries predictions those tests disproved.
> Findings 5, 7 and 8 in particular are superseded. The per-finding folders in
> [`../../findings/cloud-cloudconfig/`](../../findings/cloud-cloudconfig/) are
> built from the tests' own `verification.txt` files and are the accurate
> record.

---

## Findings

### 1. Port 8883 to AWS is blocked; 443 works — and the error hides this

Tests 05 and 06 differ **only** in the port. 8883 failed, 443 succeeded.

The failure looked like a certificate problem:

```
[DATA#1]/[EVENTS]/[CTRL]/[MGMT]: connection initialization failed with return code (255), retry count (0)
```

All four channels failing within ~2 ms, zero retries — which reads like a local
config fault, not a network one. It cost hours before the cause was found.

Before finding it, we had proved AWS itself was fine: connecting from this host
with the reader's exact certificate files, MQTT connect, publish and subscribe all
succeeded. Credentials, policy, endpoint and reachability were all confirmed good.

**The same generic error is returned for a blocked port and for a certificate
fault, with nothing to distinguish them.** That is the single most costly issue in
this whole exercise.

### 2. AWS also needed the IoT Policy fixing first

Separately from the port, the certificate had AWS's SDK **sample** policy attached,
permitting only client IDs `sdk-java`/`basicPubSub`/`sdk-nodejs-*` and topics
`sdk/test/*`. Nothing matching `FXR60-LAB-*`.

Symptom: TLS handshake succeeds, then AWS immediately drops the MQTT session.

### 3. The reader adds `alpnProtocolNames` itself on port 443

The applied config fetched back with `get_config` contains:

```json
"alpnProtocolNames": ["x-amzn-mqtt-ca"]
```

on every port-443 connection. This is the ALPN identifier AWS IoT requires to
carry MQTT over 443. **We did not set it** — the firmware adds it. It is also
**not** a valid input field, being absent from the `additional` schema, so it must
not be sent.

### 4. `data.event` requires a client certificate — undocumented

Test 02 sent a CA-only security block on all four channels. Only one was rejected:

```json
{"code":3,"message":"Invalid Cloud Config File Schema - DATA config: event - invalid configuration (invalid \"security\" JSON object)"}
```

`control.commandResponse`, `management.event` and `management.commandResponse` all
accepted the identical block.

Confirmed by the spec's own examples — every `data.event` example supplies a full
client identity:

| Spec example | data.event security |
|---|---|
| `mqtt_tls_all_channels` | CA + `privateKeyFileLocation` + `publicKeyFileLocation` |
| `data_mqtt_tls_installed_cert` | `installedCertificateName` + `installedCertificateType` |

**The schema does not express this.** It is identical across all four channels with
`required: None` on each.

Consequence: server-auth-only TLS cannot be configured for tag data — mutual TLS
is effectively mandatory on that channel.

### 5. Three groups of fields appear in examples but not in the schema

The same defect, three times:

| Field(s) | Used in example | In schema? | Reader's verdict |
|---|---|---|---|
| `CACertificateFileContent`, `privateKeyFileContent`, `publicKeyFileContent` | `mqtt_aws_all_channels` | ❌ | **Rejected** (test 07) |
| `basicAuthentication` | `mqtt-Azure` examples | ❌ | **Rejected** in that placement (test 09) |
| `URL`, `authenticationType`, `verifyHost` | `data_http_post` | ❌ | Untested (test 10) |
| `tcpipport` | `data_tcpip_server` | ❌ | Untested (test 13) |

The schema for `data.event.options` permits exactly six fields:

```
additional  enableSecurity  endpoint  publishTopic  security  subscribeTopic
```

There is nowhere to express an HTTP URL, a TCP port, or a WebSocket address. Given
the two confirmed rejections, tests 10 and 13 are expected to fail the same way.

### 6. Username/password is supported by firmware but unreachable via the API

`basicAuthentication` appears in the reader's own `get_config` output — nested
inside `options.additional` — and the web UI has a "BASIC Authentication" checkbox.
So the capability exists.

But the field is in no schema, and the one example showing it puts it inside
`options`, not `options.additional`. Neither placement worked.

### 7. `WEBSOCKET` has no address field at all

Its example carries only `security.verifyPeer`. Nothing states where the reader
should connect. Tests 11 and 12 are designed to answer this: 11 is the example
verbatim, 12 adds a schema-valid `endpoint` block.

### 8. `tcpip-server` appears to make the reader the server

Its example has a port and no hostname, implying the reader listens on 8081 and
clients connect to it — the reverse of the other types. Worth stating explicitly
in the docs, as it changes the integration architecture.

### 9. A rejected config is safe; an accepted one is not

| Response | Effect |
|---|---|
| Schema rejection | Nothing changes — reader keeps its current connection |
| `{"response":"success"}` | Applied immediately, even if the endpoint is unreachable |

An accepted-but-unreachable config drops the reader off both the new endpoint and
the old one. Recovery needs the local web UI, which stays reachable only because
every config here sets `enableLocalRest: true`. That is what made recovery possible
each time — test 99 was used several times.

---

## Questions for Zebra

1. **Error code 255.** What does it mean at MQTT client initialization? It is
   currently returned for a blocked TCP port *and* for certificate faults. Please
   distinguish them — this was the most expensive issue here by a wide margin.

2. **Port guidance for AWS.** 8883 is blocked on many corporate networks. Is 443 +
   ALPN the recommended path? It is not mentioned in the spec.

3. **`data.event` client-certificate requirement.** Please document it in the
   schema, or confirm it is a bug and CA-only should be accepted as the schema
   implies.

4. **Schema vs examples.** Either add the missing fields to the schema
   (`*FileContent`, `basicAuthentication`, `URL`, `authenticationType`,
   `verifyHost`, `tcpipport`) or correct the examples. Currently three of six
   documented connection types cannot be configured from the documented schema.

5. **`WEBSOCKET` address.** Where does it go? The example has no address field.

6. **`tcpip-server` direction.** Does the reader listen, or connect out? The
   absence of a hostname implies it listens; please state it.

7. **`basicAuthentication`.** Is it supported, and in which object? The reader
   reports it inside `options.additional`; the spec's example puts it in `options`.

---

## Folder contents

```
01-mqtt-plain-1883-SUCCESS/
02-mqtt-tls-8883-CAonly-REJECTED/
03-mqtt-mtls-8884-filepaths-UNTESTED/
04-mqtt-mtls-8884-certstore-UNTESTED/
05-aws-installedCert-port8883-FAILED/
06-aws-installedCert-port443-SUCCESS/
07-aws-inline-FileContent-REJECTED/
08-aws-fileLocation-UNTESTED/
09-mqtt-username-password-1884-UNRESOLVED/
10-httpPost-UNTESTED-schema-gap/
11-websocket-spec-shape-UNTESTED/
12-websocket-with-endpoint-UNTESTED/
13-tcpip-server-UNTESTED-schema-gap/
99-rollback-reader-own-broker-SUCCESS/
```

Each contains:

| Path | Contents |
|---|---|
| `request body/request.json` | The real request — method, URL, reader, headers, body |
| `response body/response.json` | The response, or `{"_status": "not yet sent"}` if untested |
| `response body/http_status.txt` | HTTP status, or `-` if untested |
| `response body/verification.txt` | How the result was confirmed, and what was learned |

Bearer tokens are not stored — they are live credentials. Each `request.json`
records the command that mints one instead. All other values are verbatim as sent.

---

## Test infrastructure

Everything the reader connects to is on `10.117.229.18`, all systemd-managed and
enabled at boot:

| Port | Service | For |
|---|---|---|
| 443 | `pfx-file-server` | Certificate/PFX downloads |
| 1883 | `mosquitto` | Plain MQTT |
| 1884 | `mosquitto-fxr60-auth-1884` | Username/password MQTT |
| 8883 | `mosquitto-fxr60-tls-8883` | MQTT over TLS |
| 8884 | `mosquitto-fxr60-mtls-8884` | Mutual TLS MQTT |
| 9443 | `fxr60-recv-http-post` | httpPost receiver |
| 9444 | `fxr60-recv-websocket` | WebSocket receiver |

Details: `../../BROKER_REFERENCE.md` and `../../receivers/README.md`.

---

## Suggested next steps

Schema-valid tests first, so a later rejection is clearly attributable:

1. **03** — mTLS via file paths. Satisfies the data.event constraint from test 02
2. **04** — mTLS via cert store. If 03 works and 04 does not, that isolates
   `installedCertificateName` as faulty on a local broker
3. **11** then **12** — resolves where the WebSocket address belongs
4. **10** and **13** — expected rejections; the messages confirm the schema gaps
5. **08** — AWS file paths, once the certs are on the reader

Keep test 99 to hand throughout.
