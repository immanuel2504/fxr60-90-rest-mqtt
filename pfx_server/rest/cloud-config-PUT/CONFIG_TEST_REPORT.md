# FXR60 `PUT /cloud/config` — Test Report

Real request/response captures in the numbered folders beside this report.

## Scope

| | |
|---|---|
| Endpoint | `PUT /cloud/config` (`setConfigMqtt`; MQTT: `set_config`) |
| Schema | `SetConfigMqttRequest` |
| Reader | `10.233.48.36`, reader application **5.0.7**, serial 260975251E0049 |
| Tests | 18 — all schema-validated before sending |

## How this differs from `PUT /cloud/cloudConfig`

The two endpoints are complementary, not duplicates. Per the schema:

> Only the data endpoint (`endpointConfig.data`) is configurable via this API. Use
> `PUT /cloud/cloudConfig` to configure control and management plane endpoints.

Confirmed: `endpointConfig` here allows exactly one key, `data`.

But this endpoint also carries something `/cloud/cloudConfig` does not — the
**`GPIO-LED`** object, for driving GPO pins and LEDs from reader events. That is the
larger part of this endpoint's value, and six of the nine tests cover it.

Top-level keys: `xml`, `GPIO-LED`, `READER-GATEWAY`.

---

## Results

| # | Test | Result |
|---|---|---|
| 01 | Data endpoint → our MQTT broker | ✅ **Working, tag data delivered** |
| 02 | batching + retention **with** `endpointConfig` | ✅ **Working** |
| 02b | batching + retention **alone** | ❌ Rejected — needs `endpointConfig` |
| 03 | GPIO-LED defaults | ✅ Accepted |
| 04 | GPIO-LED radio events | ✅ Accepted |
| 05 | GPIO-LED cloud events, GPO + LED combined | ✅ Accepted |
| 06 | GPIO-LED GPI-triggered | ✅ Accepted (not triggerable — see below) |
| 07 | GPIO-LED with conditions | ✅ Accepted, stored verbatim |
| 08 | GPIO-LED complete reference, all 9 events | ⚠️ **Accepted and stored, but actions never fire** |
| 09 | Data endpoint → AWS IoT (port 443 + ALPN) | ✅ **Connected** |
| 10 | Data endpoint → httpPost receiver | ✅ **Working, tag data delivered** |
| 11 | Data endpoint → tcpip-server | ✅ **Working, tag data received** |
| 12 | Data endpoint → WEBSOCKET | ⚠️ Accepted, never connects |
| 13 | Clear the data endpoint | ✅ **Working** |
| 14 | `xml` operational profile | ❌ Core Service timeout |
| 15 | **Combined** — MQTT data + GPIO-LED | ✅ **Both halves working; GPIO fires** |
| 16 | **Combined** — httpPost + conditional GPIO | ✅ **Working; conditions enforced** |
| 17 | **Combined** — clear data + GPIO-LED | ✅ **Working; GPIO fires with no data endpoint** |
| 18 | **Combined** — AWS data + cloud-event GPIO | ✅ **Working; `CLOUD_CONNECT` fires** |
| 19 | `CLOUD_DISCONNECT` isolated, unreachable broker | 🐛 **`CLOUD_DISCONNECT` works; `CLOUD_CONNECT` fires on a FAILED connection** |

17 of 20 accepted. **Seven configurations verified delivering real tag data or
producing a confirmed effect**, two rejections with documented causes, one
acceptance that does not work, and **one firmware defect found and reproduced**.

Verified working end to end: MQTT (01), batching/retention (02), httpPost (10),
tcpip-server (11), clear-data (13), AWS connected (09), AWS + cloud GPIO (18).

Both cloud events are now confirmed to drive hardware — but `CLOUD_CONNECT`
fires on a connection *attempt* rather than a successful connection. See
finding 12.

---

## Findings

### 1. `batching` and `retention` cannot be sent without `endpointConfig`

The schema says READER-GATEWAY "must contain at least one of: `endpointConfig`,
`batching`, `retention`, or `managementEventConfig`" — implying any one alone is
valid. It is not.

Sending batching + retention alone:

```json
{"code":1,"message":"Invalid global batching payload fields: Batching configuration error: Incorrect number of batching objects for the given endpoints"}
```

Retention alone gave the equivalent error.

**The count was not the problem.** At the time the reader had exactly one data
endpoint, its stored batching had exactly one object, and one object was sent.

**Root cause:** the reader counts these objects against the endpoints **in the same
request**, not against stored configuration. With no `endpointConfig` present there
are zero endpoints, so any number is "incorrect".

**Proven** by test 01: the identical batching and retention values were accepted as
soon as `endpointConfig` was included.

So `endpointConfig` is effectively mandatory whenever batching or retention is
present — contradicting the schema.

### 2. `GPIO-LED` *can* be sent alone

Unlike batching/retention, test 03 sent only `GPIO-LED` with no `READER-GATEWAY`
at all, and was accepted. The two objects behave differently.

### 3. `GPIO-LED` replaces wholesale — it does not merge

After test 07, `GET /cloud/config` showed only the events in that request. Test 06's
`GPI_1_*` and `GPI_2_*` events were gone.

Any `GPIO-LED` write must therefore contain the **complete** desired configuration.
Sending one event does not add to what is already there — it discards the rest.

### 4. Conditions are enum strings, not objects

`actionConditions` accepts exactly four values:

| Condition | Meaning |
|---|---|
| `IS_CLOUD_CONNECTED` | reader connected to cloud |
| `~IS_CLOUD_CONNECTED` | reader lost cloud connectivity |
| `IS_RADIO_ONGOING` | inventory running |
| `~IS_RADIO_ONGOING` | inventory not running |

Both forms work, confirmed stored verbatim:

```json
"conditions": ["IS_CLOUD_CONNECTED", "IS_RADIO_ONGOING"]
"conditions": {"operator": "or", "operands": ["~IS_CLOUD_CONNECTED"]}
```

A bare array implies `and`.

**There is no GPI-based condition.** An earlier draft of test 07 used
`{type: "GPI", pin: 1, state: "HIGH"}`, inferred from other condition schemas in the
spec. Checking `conditionsArray.v1` showed that shape does not exist. Corrected
before any request was sent.

### 5. GPI events cannot be triggered through the API

Test 06 binds actions to `GPI_1_H`/`GPI_1_L`/`GPI_2_H`/`GPI_2_L`. All were accepted,
but none can be fired: GPI transitions need a physical input change, and the API can
only **read** GPIs (`GET /cloud/gpi`), never drive them. `PUT /cloud/gpo` drives
outputs, not inputs.

All four GPIs currently read HIGH, so the `_L` events could not fire either.

Only GPI 1 and 2 were used — the spec states GPI 3 and 4 events are unsupported on
FXR60/FXR90.

### 6. Data-plane configuration works end to end

Test 01 pointed `data.event` at our MQTT broker and delivered real tag reads:

```json
{"data":{"idHex":"e2806894000040017790e471","antenna":1,"channel":909.75,
         "peakRssi":-45,"phase":32.68,"reads":1,"CRC":"f3b3","PC":"3000",
         "eventNum":170},
 "timestamp":"2026-09-05T15:36:04.395+0000","type":"CUSTOM"}
```

Batching `{8192, 1000}` and retention `{120, 50000, 200}` applied in the same
request.

### 7. GPIO-LED **does** drive hardware — an earlier conclusion corrected

This finding originally stated the GPIO-LED engine was a silent no-op, based on
test 08 where `RADIO_START` was stored with a GPO HIGH action and the pin never
changed. **That conclusion was wrong**, and tests 15–17 disproved it.

Test 15 fired correctly:

```
before : {"1":"LOW","2":"LOW", "3":"HIGH","4":"LOW"}
start  : {"1":"LOW","2":"HIGH","3":"HIGH","4":"LOW"}   <-- pin 2 fired
stop   : {"1":"LOW","2":"LOW", "3":"HIGH","4":"LOW"}   <-- pin 2 released
```

Reproduced over two further start/stop cycles — reliable, not a fluke.

Two follow-ups isolated the variables and cleared both suspicions:

| Suspicion | Test | Result |
|---|---|---|
| `READER-GATEWAY` must accompany `GPIO-LED` | Sent GPIO-LED alone | Pin 2 **fired** — not required |
| GPO pin 1 specifically is broken | Sent pin 1 on RADIO_START alone | Pin 1 **fired** — not the pin |

**Why test 08 did not fire is not established.** Most likely transient — possibly a
settling period needed after a config write before the engine acts, and test 08
started its inventory shortly after writing. Not confirmed, so recorded as unknown
rather than guessed at.

**The lesson:** one negative observation was over-generalised into a firmware
defect. Changing a single variable at a time is what disproved it.

### 7b. Conditions are genuinely enforced

Test 16 showed two actions in the same config behaving differently according to
their conditions:

| Action | Conditions | Result |
|---|---|---|
| pin 1 on `TAG_READ` | `[IS_CLOUD_CONNECTED, IS_RADIO_ONGOING]` | **Fired** |
| pin 2 on `RADIO_START` | `[IS_CLOUD_CONNECTED]` | **Suppressed** |

Both stored correctly, so this is the condition engine working rather than a fault.

Two things remain unexplained and are flagged rather than rationalised: pin 2's
`IS_CLOUD_CONNECTED` evaluated false while the data interface reported
`connected` — suggesting the condition tracks the management/control channel rather
than the data endpoint — yet pin 1's conditions *include* the same value and it
fired. Unresolved.

### 7c. GPIO-LED is independent of the data plane

Test 17 cleared the data endpoint to zero connections and set GPIO-LED in the same
request. Pin 4 still fired on `RADIO_START`.

So a reader can drive local signalling with no data endpoint and no cloud
connection at all.

### 7d. Both objects can be combined in one request

Tests 15–17 confirm `GPIO-LED` and `READER-GATEWAY` apply together from a single
request — the spec's `data_mqtt` pattern — including for opposing purposes
(test 17 tears down the data endpoint while building up GPIO behaviour).

### 8. The data plane works across four connection types

`PUT /cloud/config` successfully configures the data endpoint for every connection
type we can reach, with delivery verified rather than assumed:

| Type | Evidence |
|---|---|
| `mqtt` | Real tag reads captured on `fxr60-lab/tevents` |
| `httpPost` | Receiver log grew by 6 POSTs during an inventory |
| `tcpip-server` | Port 8081 **closed before, open after**; 2893 bytes of tag data received by connecting to the reader |
| `mqtt-AWS` | `connectionStatus: connected` on port 443 with ALPN |

`tcpip-server` gave the cleanest possible proof: the reader is the **server** for
this type, and the port transition from closed to open is unambiguous.

### 9. `WEBSOCKET` behaves identically here — it is not endpoint-specific

Test 12 was run specifically because WebSocket failed on `/cloud/cloudConfig`, to
see whether this endpoint validated it differently. It does not:

```
status: connectionStatus "disconnected", connectionError ""   <-- empty, no reason
stored: {"security": {"verifyPeer": false}}
receiver on 9444: no connection attempt at all
```

Combined with the earlier finding that WEBSOCKET security accepts **only**
`verifyPeer` — rejecting `CACertificateFileLocation`, `verifyHostName`,
`keyAlgorithm` — and that its example has no address field, WebSocket remains the
one connection type with **no working configuration** on either endpoint.

### 10. The batching/retention dependency runs one way only

Test 13 refines finding 1. `clear_data` sends `endpointConfig` with **no** batching
or retention, and is accepted.

So: batching/retention **require** `endpointConfig`; `endpointConfig` does **not**
require them.

### 11. The `xml` field fails with a Core Service timeout

```json
{"code":6,"message":"Profile configuration failed: Timeout: failed to receive Core Service response"}
```

Note `code 6` and the timeout wording — a different failure class from the `code 1`
/ `code 3` schema errors elsewhere. The request reached the Core Service and no
reply came back.

**This does not prove the field is broken.** The spec's only `xml` example is a
55-character placeholder containing nothing but a comment:

```xml
<RFID><!-- Cloud Connect operational profile --></RFID>
```

An empty profile may simply be unprocessable. Testing properly needs a real RFID
operational profile document, which the spec does not provide — which is itself
worth raising.

### 12. `CLOUD_CONNECT` fires on a connection *attempt*, not a connection

Tests 18 and 19 pair the two cloud events with GPO pins and drive them
deliberately. Both events reach the hardware — but only one is trustworthy.

**Test 18** — apply a working AWS endpoint from a verified all-LOW baseline:

| | GPO 1 (`CLOUD_CONNECT`) | GPO 2 (`CLOUD_DISCONNECT`) | GPO 3 (`RADIO_START`) |
|---|---|---|---|
| baseline | LOW | LOW | LOW |
| after apply | **HIGH** | **HIGH** | LOW |

`/cloud/status` confirmed `DATA_AWS_CLOUD_EVENTS` `connected`. Both cloud pins
latched because replacing an endpoint tears the old connection down and brings the
new one up in one PUT — so both events genuinely occur. Pin 3 staying LOW is the
negative control: the pins moved because of events, not because a config was
applied.

**Test 19** — point `data.event` at unreachable `10.255.255.1:1883`, so a connect
can never succeed:

| | GPO 1 (`CLOUD_CONNECT`) | GPO 2 (`CLOUD_DISCONNECT`) |
|---|---|---|
| baseline | LOW | LOW |
| t+20 s | LOW | **HIGH** ✅ |
| t+40 s | **HIGH** 🐛 | HIGH |

At t+20 s the behaviour is exactly right — this is the isolated confirmation that
`CLOUD_DISCONNECT` works. By t+40 s pin 1 was HIGH too, while the interface
reported:

```json
{"connectionStatus": "disconnected",
 "connectionError": "connection initialization failed with return code (255), retry count (0)"}
```

**Reproduced with the config untouched.** The pins were reset to LOW and *no new
configuration was sent* — the dead endpoint stayed active, so the only thing the
reader could be doing was retrying it:

| | GPO 1 | GPO 2 |
|---|---|---|
| baseline | LOW | LOW |
| t+20 s | LOW | LOW |
| t+40 s | **HIGH** 🐛 | LOW |
| t+100 s | HIGH | LOW |

That second run rules out every alternative: no config was applied, the baseline
was read back as LOW, the interface never once reported `connected`, and pin 1
behaves correctly in tests 15–18. The ~40 s onset against a
`reconnectDelay`/`reconnectDelayMax` of 2/10 s points at the event being hooked to
the *start of a connection attempt* rather than to a successful CONNACK.

**Impact.** `CLOUD_CONNECT` cannot be used as a cloud-connectivity indicator. Wired
to a stack light or PLC input it will show "cloud OK" on a reader that has never
connected and is retrying a dead endpoint — precisely the failure the indicator
exists to catch.

**Workaround.** Read
`GET /cloud/status → interfaceConnectionStatus[].connectionStatus`, which reported
`disconnected` correctly and consistently throughout both runs.

### 12b. GPO actions latch; the pair cannot show current state

Following from test 18: `CLOUD_CONNECT` and `CLOUD_DISCONNECT` each drive their own
pin HIGH and neither clears the other, so after a normal endpoint change **both**
are HIGH while the reader is connected. The pins are latched event markers, not a
state indicator.

To use them as state, each event must also clear the other's pin:

```json
"CLOUD_CONNECT":    [{"type":"GPO","pin":1,"state":"HIGH"},
                     {"type":"GPO","pin":2,"state":"LOW"}]
"CLOUD_DISCONNECT": [{"type":"GPO","pin":2,"state":"HIGH"},
                     {"type":"GPO","pin":1,"state":"LOW"}]
```

LED actions do not have this problem — LED 2 is one resource that both events set to
different colours, so the last event wins and the LED does track current state.

Note this pattern cannot rescue finding 12: a spuriously-firing `CLOUD_CONNECT`
would still clear the disconnect pin.

---

## What was not verified

Being explicit, since six tests are GPIO-LED and acceptance is not the same as
working:

| Test | Verified | Not verified |
|---|---|---|
| 01 | Config applied; **real tag data delivered** | — |
| 02 | Rejection reason established | — |
| 03–05, 07 | Accepted; stored correctly (07 checked verbatim) | LED colours — readable state is not exposed for LEDs |
| 06 | Accepted | **Cannot be triggered at all** without physical GPIO access |
| 15–17 | GPO pins observed changing on `RADIO_START` / `RADIO_STOP` | — |
| 18–19 | GPO pins observed on `CLOUD_CONNECT` / `CLOUD_DISCONNECT`; defect reproduced | — |

The GPIO-LED interface is confirmed to drive hardware, not merely to store
configuration — `GET /cloud/gpo` reports pin state, so GPO actions are verifiable
remotely. That is how findings 7 and 12 were established.

Two limits remain: **LED** actions cannot be confirmed (no equivalent read-back, and
no physical access), and **GPI**-triggered events cannot be exercised without
someone to close a contact at the reader.

Every GPO observation in this report was taken from a baseline of all four pins
driven LOW and **read back to confirm the reset** before applying anything. GPO
state persists across configuration changes, so without that step leftover pin
state from an earlier test reads as a fresh event — which is exactly what made an
earlier attempt at test 18 unusable, and why test 08 is marked inconclusive rather
than failed.

---

## Questions for Zebra

1. **batching / retention alone.** The schema says READER-GATEWAY needs "at least
   one of" four keys, but batching and retention are rejected unless
   `endpointConfig` accompanies them. Please correct the schema, or the validator.

2. **The error message.** "Incorrect number of batching objects for the given
   endpoints" points at the count, when the real problem is a missing
   `endpointConfig`. Something like "batching requires endpointConfig in the same
   request" would have been much faster to act on.

3. **GPIO-LED merge semantics.** Is replace-whole intended? It is not stated, and
   silently discarding unlisted events is easy to hit.

4. **GPI event testing.** Is there any way to trigger a GPI transition through the
   API for test purposes? Currently `GPI_*` event configuration cannot be validated
   without physical access.

5. **`CLOUD_CONNECT` fires on a failed connection attempt (highest priority).** Is
   the event specified to fire on a successful MQTT connection, or on an attempt?
   Observed: the pin goes HIGH while `/cloud/status` reports the same interface
   `disconnected` with error 255 — with no configuration change and no broker
   present. Reproduced twice from a verified-LOW baseline (finding 12). This makes
   the event unusable as a connectivity indicator: a reader retrying a dead
   endpoint signals healthy.

6. **Should `CLOUD_CONNECT` re-fire on every reconnect attempt?** If so, please say
   so in the docs, and please also expose an event that fires only on a *successful*
   connection — that is what integrators wiring a status lamp actually need.

7. **Are GPO actions intended to latch?** Applying a new endpoint config emits
   `CLOUD_DISCONNECT` then `CLOUD_CONNECT`, leaving both pins HIGH (finding 12b), so
   the pair cannot represent current state. Is driving both pins from both events
   the intended pattern, or is there a supported way for one event to clear
   another's pin?

8. **Error 255, again.** The same opaque code is returned here for an unreachable
   host as for a blocked port and for certificate faults (see the `cloudConfig`
   report, tests 05/06). Three distinct causes, one indistinguishable message.

Note: an earlier version of this report asked whether the GPIO-LED engine was
functional at all, based on test 08. **That was wrong** — tests 15–19 confirm GPIO
actions do drive hardware. Test 08's non-firing is still unexplained, but it is an
isolated case, not the general behaviour.

---

## Folder contents

```
01-data-endpoint-mqtt-SUCCESS/
02-batching-retention-with-endpointConfig/
02b-batching-retention-alone-REJECTED/
03-gpio-led-defaults-SUCCESS/
04-gpio-led-radio-events-SUCCESS/
05-gpio-led-cloud-events-SUCCESS/
06-gpio-led-gpi-events-SUCCESS/
07-gpio-led-conditions-SUCCESS/
08-gpio-led-complete-reference-INCONCLUSIVE/
09-data-endpoint-aws-SUCCESS/
10-data-endpoint-httpPost-SUCCESS/
11-data-endpoint-tcpip-server-SUCCESS/
12-data-endpoint-websocket-ACCEPTED-never-connects/
13-clear-data-endpoint-SUCCESS/
14-xml-operational-profile-FAILED/
15-combined-mqtt-and-gpio-led-SUCCESS/
16-combined-httpPost-and-conditional-gpio-SUCCESS/
17-combined-clear-data-keep-gpio-SUCCESS/
18-combined-aws-and-cloud-events-SUCCESS/
19-force-cloud-disconnect-BUG-FOUND/
```

Each contains `request body/request.json`, `response body/` with the response,
`http_status.txt`, and `verification.txt` recording how the result was confirmed and
what it revealed.

Successful PUTs return HTTP 200 with an **empty body** — stored as a 0-byte
`response.txt`, so an empty file means the reader really returned nothing.

Bearer tokens are not stored; each request records the command that mints one.

---

## Reference — GPIO-LED structure

Nine events, each taking an array of actions performed sequentially:

```
GPI_1_H  GPI_1_L  GPI_2_H  GPI_2_L
CLOUD_CONNECT  CLOUD_DISCONNECT
TAG_READ  RADIO_START  RADIO_STOP
```

Plus `GPODefaults` (pins 1–4, `HIGH`/`LOW`) and `LEDDefaults` (LEDs 1–3,
`RED`/`GREEN`/`AMBER`).

**GPO action** — requires `type`, `pin`, `state`:

```json
{"type":"GPO","pin":1,"state":"HIGH","postActionState":"LOW",
 "blink":{"ON":200,"OFF":200,"DURATION":1000}}
```

**LED action** — requires `type`, `led`, `color`:

```json
{"type":"LED","led":1,"color":"GREEN","postActionColor":"RED",
 "blink":{"ON":100,"OFF":100,"DURATION":500}}
```

`blink` requires all three of `ON`, `OFF`, `DURATION` (milliseconds).
`DURATION: 0` blinks indefinitely.

Hardware on this reader: 4 GPI, 4 GPO, LEDs supporting RED/GREEN/AMBER.

---

## Related

| File | Contents |
|---|---|
| `../cloud-cloudConfig-PUT/` | `PUT /cloud/cloudConfig` — control and management endpoints, all connection types |
| `../cloud-certificates-PUT/` | Certificate download authentication |
| `../cloud-config/` | `GET /cloud/config` capture |
| `../../MQTT_API_Findings.xlsx` | All findings and open questions |

---

## Per-finding folders

Every finding in this report also exists as its own folder under
[`../../findings/cloud-config/`](../../findings/cloud-config/), carrying the request body and
response body of the test(s) that prove it — the same layout as the numbered test
folders here.
