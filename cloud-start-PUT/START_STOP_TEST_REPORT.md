# FXR60 `PUT /cloud/start` and `PUT /cloud/stop` — Test Report

Every start/stop example from the **latest** spec, tested against a live reader.

## Scope

| | |
|---|---|
| Spec | `openAPISpec 11.yaml` — **IoT Connector REST API v3.0.0** |
| Endpoints | `PUT /cloud/start` (`startInventory`), `PUT /cloud/stop` (`stopInventory`) |
| Reader | `10.233.48.36`, reader app 5.0.7 |
| Date | 2026-09-06 |
| Spec examples | **10** — 6 start, 4 stop |
| Extra tests | 2 — the documented cross-field constraint, and 5 validation probes |

---

## Answer: yes, all ten examples work

**10 / 10 spec examples returned HTTP 200 and produced the documented effect**,
each confirmed by reading the reader's actual state back — not just by the status
code.

| # | Example | Body | Result |
|---|---|---|---|
| 1 | `start_Inventory` | `{}` | ✅ `radio: inactive → active` |
| 2 | `start_RFID_only` | `{"scanType":["rfid"]}` | ✅ `radio: inactive → active` |
| 3 | `start_Inventory with AutoStart` | `{"doNotPersistState":false}` | ✅ accepted, inventory started |
| 4 | `start_Inventory with ImpinjGen2X` | `{"applyImpinjGen2X":true}` | ✅ `gen2x: none/false → fastID/true` |
| 5 | `start_BLE_only` | `{"scanType":["ble"]}` | ✅ `ble: stopped → running` ⚠️ needs `ble.enable` first |
| 6 | `start_BLE_and_RFID` | `{"scanType":["ble","rfid"]}` | ✅ both started, **624 real events** |
| 7 | `stop_RFID_default` | `{}` | ✅ `radio: active → inactive` |
| 8 | `stop_RFID_explicit` | `{"scanType":["rfid"]}` | ✅ `radio: active → inactive` |
| 9 | `stop_BLE_only` | `{"scanType":["ble"]}` | ✅ `ble: running → stopped` |
| 10 | `stop_BLE_and_RFID` | `{"scanType":["ble","rfid"]}` | ✅ both stopped |

One example (5) needed an **undocumented prerequisite** before it would work —
see [finding 2](#2--start_ble_only-needs-bleenable-first-and-the-error-hides-it).

### Proof it is real, not just status flags

Test 6 routed tag data to a local MQTT broker and captured a 15-second combined
scan:

```
624 events
  BLE_DATA : 558
  CUSTOM   :  66      ← RFID tag reads
unique RFID tags: 8
```

One `start` call drove **both radios**, and both delivered real data to the same
endpoint, distinguishable by the `type` field.

---

## Findings

### 1. ✅ `scanType` is honoured per type — the default really is RFID-only

The schema says *"Omit for RFID-only (default)"*. Confirmed on every combination:

| Body | `radioActivity` | `ble.scanState` |
|---|---|---|
| `{}` | **active** | stopped |
| `{"scanType":["rfid"]}` | **active** | stopped |
| `{"scanType":["ble"]}` | inactive | **running** |
| `{"scanType":["ble","rfid"]}` | **active** | **running** |

BLE-only leaves the RFID radio untouched and vice versa. `stop` mirrors this
exactly. Nothing starts "everything" implicitly.

### 2. ⚠️ `start_BLE_only` needs `ble.enable` first — and the error hides it

The spec's example, sent verbatim against a default reader:

```json
PUT /cloud/start {"scanType":["ble"]}
→ 422 {"code":3,"message":"CS:'startBleScan' failed, Reason: Invalid BLE configuration: unknown or unexpected field in request payload, refer to API documentation for supported fields"}
```

**The message is wrong.** It reports *"unknown or unexpected field in request
payload"* — but the payload is the spec's own example, contains exactly one
field, and that field matches the schema. Nothing about it is unknown.

The real cause is `ble.enable: false` in `bleConfig` (the reader's default). The
message never hints at it, which cost real time to diagnose.

After enabling BLE:

```json
PUT /cloud/bleConfig {"ble":{"enable":true, …full object… }}   → 200
PUT /cloud/start {"scanType":["ble"]}                          → 200 ✅
   ble.scanState: stopped → running
```

The full `bleConfig` object is required — a minimal `{"ble":{"enable":true}}` is
rejected, a separate known finding.

**Ask:** document the `ble.enable` prerequisite on `/cloud/start`, and make the
error name the actual cause.

### 3. ✅ `applyImpinjGen2X` works — with a clean negative control

Test 4 is the cleanest demonstration of the two-step Gen2X flow. With
`{"fastID":{"enabled":true}}` saved beforehand:

| Start body | `impinjGen2X` after |
|---|---|
| `{"applyImpinjGen2X":true}` | **`fastID` / `isActive: true`** ✅ |
| `{}` (same saved config) | `none` / `isActive: false` ❌ |

So the flag is genuinely required — a plain `start` ignores a saved Gen2X config
entirely.

**Also confirmed:** the config persists across sessions but the **activation does
not**. After `PUT /cloud/stop`, status returns to `none/false`, so the flag must
be re-sent on every start. This matches the finding in
[`cloud-impinjGen2X-PUT/TAG_PROTECT_REPORT.md`](../cloud-impinjGen2X-PUT/TAG_PROTECT_REPORT.md).

The reader states the requirement itself in the `impinjGen2X` response:
*"Use applyImpinjGen2X flag in start command to apply features."*

### 4. ✅ The documented cross-field constraint is enforced — and reveals `_sim`

The schema says `applyImpinjGen2X` *"Cannot be used with `scanType: ["ble"]`"*:

```json
PUT /cloud/start {"scanType":["ble"],"applyImpinjGen2X":true}
→ 422 {"code":1,"message":"scanType with 'ble' cannot be combined with _sim or applyImpinjGen2X"}
```

Correctly rejected — Gen2X is an RFID air-protocol feature with no BLE meaning.

**But the message names `_sim`, which appears nowhere in `openAPISpec 11.yaml`.**
Presumably a simulation flag. If internal it should not surface in a
customer-facing error; if usable it should be documented.

### 5. 🐛 The removed per-endpoint `scanType` object form still works

v3.0.0 defines `scanType` as an **array only**:

```yaml
scanType:
  type: array
  items: {enum: [ble, rfid]}
```

The previous revision also allowed a per-endpoint **object** form, with examples
named `start_Targeted`, `start_targeted_RFID`, `start_targeted_BLE` and others.
**Those examples are gone from v3.0.0 and the object form is no longer in the
schema.**

The firmware still accepts it:

```json
PUT /cloud/start {"scanType":{"dataEndpoint1":["rfid"]}}   → 200 ✅
```

Corroborated by the reader's own error messages, two of which **still mention
"object"**:

```
"scanType must be a non-empty object or array"
"payload.scanType must be a valid json object or array"
```

So the validator still implements the object form — only the documentation
dropped it.

**Ask:** was the object form deliberately removed, deprecated, or dropped from
the docs by accident? If deprecated, keep it working but say so in the schema. If
removed, the firmware should reject it and those two messages should stop
mentioning "object".

### 6. ✅ Validation is strong, with the best error messages on this API

| Probe | Response |
|---|---|
| `{"scanType":[]}` | 422 `scanType must be a non-empty object or array` |
| `{"scanType":["rfid","rfid"]}` | 422 `duplicate 'rfid' in scanType` |
| `{"scanType":["zigbee"]}` | 422 `unknown scanType value 'zigbee': expected 'ble' or 'rfid'` |
| `{"scanType":"rfid"}` | 422 `Unknown type in payload.scanType must be a valid json object or array.` |

`minItems: 1` and `uniqueItems: true` are both enforced, and the enum error
**lists the valid values** — the standard the rest of this API should meet
(compare `app-led`'s bare `Invalid color`, or error 255 in the cloudConfig
report).

### 7. `stop` is not idempotent

Stopping something that is not running is an **error**, not a no-op:

```json
PUT /cloud/stop {"scanType":["ble"]}    (BLE not running)
→ 422 {"code":1,"message":"No scan is currently active"}
```

The message is clear and names the real condition — a useful contrast with
[finding 2](#2--start_ble_only-needs-bleenable-first-and-the-error-hides-it).

Worth noting for client authors, since `DELETE /cloud/logs/syslog` **is**
idempotent on this same API. Two different conventions; neither documented.

### 8. `doNotPersistState` — accepted, but persistence not verified

Both values return 200 and start the inventory:

```
{"doNotPersistState": false}  → 200, radio active
{"doNotPersistState": true}   → 200, radio active
```

**Not verified:** the actual reboot-persistence and auto-start behaviour, which is
the entire point of the field. Confirming it requires rebooting the reader, which
was out of scope — the reader is shared and in use.

So the field is confirmed *accepted and harmless*; the documented effect is
**untested and not claimed here**.

---

## What changed in v3.0.0

| | Previous revision | v3.0.0 |
|---|---|---|
| `scanType` type | array **or** per-endpoint object | **array only** |
| `start` examples | 13 (incl. 6 `*targeted*`) | **6** |
| `stop` examples | — | **4** |
| Targeted examples | `start_Targeted`, `start_targeted_RFID`, … | **removed** |
| `doNotPersistState` | present | present |
| `applyImpinjGen2X` | present | present |

The example set is much tidier — 10 focused examples instead of 13 with heavy
overlap, and `stop` now has examples at all, which it lacked before. The only
issue is that the removed object form still works ([finding 5](#5--the-removed-per-endpoint-scantype-object-form-still-works)).

---

## Questions for Zebra

1. **`scanType` object form (highest priority).** v3.0.0 removed it from the
   schema and deleted all six `*targeted*` examples, but the firmware still
   accepts `{"scanType":{"dataEndpoint1":["rfid"]}}` with HTTP 200, and two error
   messages still say "object or array". Deprecated, removed, or a docs
   oversight?

2. **`ble.enable` prerequisite.** `start_BLE_only` fails on a default reader
   because BLE is disabled in `bleConfig`. Please document that, and fix the
   error — *"unknown or unexpected field in request payload"* is actively
   misleading when the payload is the spec's own single-field example.

3. **`_sim`.** The constraint error names a field that appears nowhere in the
   spec. Internal or usable?

4. **`stop` idempotency.** Is 422 on an inactive scan intended? `DELETE
   /cloud/logs/syslog` is idempotent on the same API, so the convention is
   inconsistent.

5. **`applyImpinjGen2X` per-session activation.** The flag must be re-sent on
   every start; the saved config persists but the activation does not. The
   description mentions only reboot behaviour. Please state the per-session
   requirement.

---

## Reader state after testing

| | Pre-test | Post-test | |
|---|---|---|---|
| `radioActivity` | `inactive` | `inactive` | ✅ |
| `ble.scanState` | `stopped` | `stopped` | ✅ |
| `bleConfig.ble.enable` | `false` | `false` | ✅ |
| `impinjGen2X` | `{"feature":"none","isActive":false}` | same | ✅ |
| Data endpoint | `DATA_AWS_CLOUD_EVENTS` connected | same | ✅ |
| Mode | `CUSTOM`, antenna 1, 17 dBm | unchanged | ✅ |

BLE was enabled during testing and disabled again; the data endpoint was
temporarily routed to the local MQTT broker to capture the delivery proof in test
6, then restored to AWS.

---

## Folder contents

This report lives in `cloud-start-PUT/` and covers **both** endpoints — the stop
tests are in the sibling folder `cloud-stop-PUT/`.

```
cloud-start-PUT/
├── START_STOP_TEST_REPORT.md   ← this file (covers start AND stop)
├── 01-start_Inventory-empty-body-SUCCESS/
├── 02-start_RFID_only-SUCCESS/
├── 03-start_Inventory-with-AutoStart-SUCCESS/
├── 04-start_Inventory-with-ImpinjGen2X-SUCCESS/
├── 05-start_BLE_only-SUCCESS-requires-ble-enable/
├── 06-start_BLE_and_RFID-SUCCESS/
├── 07-constraint-ble-plus-applyImpinjGen2X-REJECTED/
└── 08-validation-probes/

cloud-stop-PUT/
├── 01-stop_RFID_default-empty-body-SUCCESS/
├── 02-stop_RFID_explicit-SUCCESS/
├── 03-stop_BLE_only-SUCCESS/
└── 04-stop_BLE_and_RFID-SUCCESS/
```

Each holds `request body/request.json` (with the spec example name recorded in
`specExampleName`), `response body/` with the verbatim response,
`http_status.txt`, and `verification.txt` giving the before/after state and what
it proved.

Successful start/stop calls return HTTP 200 with an **empty body** — stored as a
0-byte `response.txt`, so an empty file means the reader really returned nothing.

The runner used for every test is [`../startstop_test.sh`](../../startstop_test.sh);
it mints a token, prints the before state, sends the payload, and prints the
after state.

> **Token note.** Bearer tokens on this reader expire quickly — several probes in
> this run returned `401 Unauthorized` mid-sequence and had to be re-run with a
> fresh token. Mint one per call in long test runs.

---

## Related

| File | Contents |
|---|---|
| [`cloud-mode-PUT/MODE_TEST_REPORT.md`](../cloud-mode-PUT/MODE_TEST_REPORT.md) | `PUT /cloud/mode` — all five modes |
| [`cloud-impinjGen2X-PUT/TAG_PROTECT_REPORT.md`](../cloud-impinjGen2X-PUT/TAG_PROTECT_REPORT.md) | Gen2X TagProtect and the two-step apply flow |
| [`SETTINGS_ENDPOINTS_TEST_REPORT.md`](../SETTINGS_ENDPOINTS_TEST_REPORT.md) | The six settings endpoints |
| [`../findings/`](../../findings/) | Every finding as its own folder with evidence |
