# FXR60 `PUT /cloud/mode` — Operating Mode Test Report

Every one of the five operating modes tested against a live reader with **real
tags in the field**, using two reference tags as a constant so results are
comparable across modes.

## Scope

| | |
|---|---|
| Endpoint | `PUT /cloud/mode` (`setMode`; MQTT: `set_mode`) |
| Schema | `operatingMode.v1` |
| Reader | `10.233.48.36`, reader app 5.0.7 |
| Date | 2026-09-06 |
| Modes | `SIMPLE`, `INVENTORY`, `PORTAL`, `CONVEYOR`, `CUSTOM` — all five |
| Tests | 18 |
| Spec examples | all 11 attempted |

## Reference tags

Chosen from a baseline inventory as the two strongest in the field, so they read
reliably in every mode:

| EPC | Baseline RSSI @17 dBm | RSSI @30 dBm |
|---|---|---|
| `e2806894000040017790e471` | −46..−44 | −39..−38 |
| `e2806894000040017790ac71` | −52..−50 | −46..−44 |

Having known tags is what makes several results interpretable. In test 11
(exclude filter) both reference tags are **absent** — without a known reference
set, "nothing read" and "the right tags were filtered out" look identical.

Tag data was routed to a local MQTT broker (`10.117.229.18:1883`, topic
`fxr60-lab/tevents`) for the duration, because the reader's normal AWS endpoint
cannot be read back. **Restored to AWS afterwards.**

---

## Results

| # | Test | Mode | Result | Ref tags |
|---|---|---|---|---|
| 01 | Spec example `simple_basic` verbatim | `SIMPLE` | ❌ **Rejected** — `transmitPower: 31.5` > 30.0 max | — |
| 02 | Same, power corrected to 30 | `SIMPLE` | ✅ **Working** | both read |
| 03 | Spec example, interval 60 s | `INVENTORY` | ✅ **Working** — 1 report/tag | 1 read each |
| 04 | Same, interval 5 s | `INVENTORY` | ✅ **Working** — interval proven | 4 and 5 reads |
| 05 | Spec example, GPI HIGH trigger | `PORTAL` | ⚠️ Accepted, **0 tags** (correct — GPI untriggerable) | not seen |
| 06 | Same, GPI LOW trigger | `PORTAL` | ⚠️ Accepted, **0 tags** | not seen |
| 07 | Spec example `conveyor_basic` | `CONVEYOR` | ✅ **Working** | 1 read each |
| 08 | Spec example, all 14 `tagMetaData` | `CUSTOM` | ❌ **Rejected** — `READER_LOCATION` not recognized | — |
| 09 | The 13 working metadata fields | `CUSTOM` | ✅ **Working** — richest payload | 1 read each |
| 10 | EPC prefix filter, `include` | `CUSTOM` | ✅ **Working** — 11/11 tags E280 | both read |
| 11 | EPC prefix filter, `exclude` | `CUSTOM` | ✅ **Working** — 0/14 tags E280 | correctly absent |
| 12 | `reportFilter` duration 5 | `CUSTOM` | ✅ **Working** — dedupe measured | 3 and 4 reads |
| 13 | `radioStopConditions` duration 60 | `CUSTOM` | ✅ Accepted, stop not reached in window | 1 read each |
| 14 | Spec example `with_accesses` verbatim | `CUSTOM` | ❌ **Rejected** — `wordCounter` should be `wordCount` | — |
| 15 | Same, field name corrected | `CUSTOM` | ✅ **Working** — TID read back per tag | 11 and 9 reads |
| 16 | Spec example `with_selects` | `CUSTOM` | ✅ Accepted — tags discriminated | 1 read / not seen |
| 17 | Four documented cross-field constraints | — | ✅ **All enforced** | — |
| 18 | Update semantics | — | Replaces wholesale | — |

**All five modes function.** 13 of 18 tests fully working, **3 of the 11
documented spec examples cannot be sent as written**, and PORTAL cannot be
exercised without physical GPI access.

---

## Findings

### 1. 🐛 Three of the eleven documented examples fail on this reader

| Example | Problem | Fix |
|---|---|---|
| `simple_basic` | `transmitPower: 31.5` exceeds the 30.0 dBm maximum | use `30` |
| `with_tag_metadata` | `READER_LOCATION` not recognized | drop that one value |
| `with_accesses` | `wordCounter` — firmware wants `wordCount` | rename the field |

Each was corrected and re-run successfully (tests 02, 09, 15), so in every case
the example is wrong rather than the feature being broken. But a developer
working from the documentation hits three dead ends on first contact, and the
`wordCounter`/`wordCount` one is a single character.

### 2. `transmitPower` maximum is 30.0 dBm — and the units differ between endpoints

Boundary established by bisection, each value sent alone:

| Value | Result |
|---|---|
| `31.5` (the spec's) | ❌ 422 |
| `30.5` | ❌ 422 |
| **`30`** | ✅ 200 |
| `29.5` | ✅ 200 |
| `0` | ✅ 200 |
| `-1` | ❌ 422 |

Accepted range is exactly **0.0–30.0 inclusive**.

Separately — and more likely to bite:

```
GET /cloud/region  →  minTxPowerSupported: 0,  maxTxPowerSupported: 300
PUT /cloud/mode    →  transmitPower must be 0–30
```

`300` is **deci-dBm**; `/cloud/mode` takes plain **dBm**. The same physical
quantity, two units, neither documented. A client copying
`maxTxPowerSupported` into `transmitPower` gets a 422.

### 3. `SIMPLE` mode strips tag metadata to three fields

The name suggests "simple to configure". The real consequence is a reduced
payload:

| Mode | Fields delivered |
|---|---|
| `SIMPLE` | `eventNum`, `format`, `idHex` — **that's all** |
| `INVENTORY` / `CONVEYOR` | + `antenna`, `peakRssi`, `channel`, `reads` |
| `CUSTOM` with 13 fields | + `phase`, `PC`, `CRC`, `EPC`, `TID`, `USER`, `MAC`, `hostName` |

No RSSI, no antenna number, no channel — and `SIMPLE` takes no `tagMetaData` key,
so there is no way to ask for more. Any integration needing signal strength or
antenna attribution cannot use `SIMPLE`.

Worth stating plainly in the docs, since the mode's name doesn't hint at it.

### 4. ✅ `INVENTORY` interval is genuinely enforced — measured

The cleanest A/B in this set. Identical configs, only the interval changed:

| | interval 60 s | interval 5 s |
|---|---|---|
| window | 20 s | 22 s |
| unique tags | 30 | 30 |
| **total reads** | **30** | **101** |
| ref `…e471` | 1 read | 4 reads |
| ref `…ac71` | 1 read | 5 reads |

At 60 s, `unique == total` — every tag reported exactly once. At 5 s, 22/5 ≈ 4.4
reports expected per tag; observed 4 and 5.

The arithmetic matching is the point: reporting rate tracks the configured
interval, so deduplication is real and predictable. **This is the knob that
controls event volume** — a tag sitting in the field generates 1 event/minute at
60 s and 12 at 5 s.

### 5. ✅ EPC prefix filtering works, and is enforced at the reader

Both reference tags begin `E2806894`, which makes this pair testable:

| | `include` E280 | `exclude` E280 |
|---|---|---|
| unique tags | 11 | 14 |
| E280 tags present | **11 (all)** | **0 (none)** |
| ref `…e471` | read | correctly absent |
| ref `…ac71` | read | correctly absent |

Complementary sets, zero leakage either direction. The non-E280 tags from the
baseline (`20004035…`, `41544035…`, `333311112222…`) are correctly dropped by
`include` and correctly returned by `exclude`.

Filtering happens **at the reader** — filtered tags never reach the network,
which matters for bandwidth on a busy portal.

### 6. `PORTAL` mode: `radioActivity: active` while reading nothing

PORTAL was accepted and produced **zero tags** — which is correct, since reads are
gated on a GPI transition. But:

```
PUT /cloud/start        → 200
GET /cloud/status       → radioActivity: "active"
tags read               → 0
```

So in PORTAL mode `radioActivity: active` means **"armed and waiting for its
trigger"**, not "reading". Those are very different operational states and the
field does not distinguish them. Anyone monitoring `radioActivity` to confirm a
portal is healthy would see `active` on a portal reading nothing because its
trigger is miswired.

`PUT /cloud/start` does **not** override the GPI trigger.

**Cannot be fully tested from the API.** All four GPIs read `HIGH` with nothing
wired, so no transition can occur — and GPI inputs cannot be driven through REST
(`PUT /cloud/gpo` drives outputs only). Both trigger polarities were tried; both
produced nothing, confirming the cause is a static input rather than wrong
polarity. Same limitation as the `GPI_*` events in
[`findings/cloud-config/19-gpi-events-cannot-be-triggered-via-api/`](../../findings/cloud-config/19-gpi-events-cannot-be-triggered-via-api/).

### 7. Requested metadata names ≠ delivered field names

Nothing in the spec states the mapping:

| Requested | Delivered |
|---|---|
| `ANTENNA` | `antenna` |
| `RSSI` | **`peakRssi`** |
| `SEEN_COUNT` | **`reads`** |
| `CHANNEL` | `channel` |
| `PHASE` | `phase` |
| `HOSTNAME` | **`hostName`** |
| `PC`, `CRC`, `EPC`, `TID`, `USER`, `MAC` | same, uppercase |
| `XPC` | **absent** — accepted but never appears |

The output casing is itself inconsistent: some fields uppercase (`PC`, `CRC`,
`EPC`, `TID`, `USER`, `MAC`), others camelCase (`antenna`, `peakRssi`, `channel`,
`phase`, `reads`, `hostName`). A client must know both conventions.

`XPC` was accepted and silently never delivered — presumably these tags carry no
XPC word, but absence is unsignalled.

### 8. `USER` memory returns an English error message in the data field

```json
"USER": "Error: tag returned error code 0x03 = Memory overrun"
```

The tags in this field have no USER bank. Rather than omitting the field or
signalling a per-tag failure, the reader places a 52-character human-readable
sentence where hex data is expected — and its type (string) is indistinguishable
from a successful read. A client parsing `USER` as hex gets prose.

### 9. `accesses` works, but cannot be throttled

With `wordCount` corrected, the Gen2 READ executes per tag and returns:

```json
"accessResults": ["e28011c12000112dbc930317"]
```

6 words = 12 bytes = 24 hex chars. Correct.

But note the volume: **173 total reads from 22 unique tags**, reference tags read
11 and 9 times — the highest rate of any test here, because no `reportFilter` or
interval applies.

The natural way to throttle that is `reportFilter` — which is **exactly the
combination the API prohibits** (`reportFilter` and `accesses` cannot both be
set, enforced in test 17). So high event volume is unavoidable when using access
operations in `CUSTOM` mode.

### 10. ✅ All four tested cross-field constraints are enforced

This is the good-news section. Unlike the field-level problems above, the
constraint documentation is **accurate** and the validator matches it:

| Documented constraint | Result |
|---|---|
| `accesses` not allowed in `INVENTORY` | ✅ 422, names the constraint |
| `radioStopConditions` not allowed in `PORTAL` | ✅ 422 |
| `reportFilter` and `accesses` cannot both be set | ✅ 422 |
| `transmitPower` length must match `antennas` | ✅ 422 |

Each rejection names the specific violation rather than returning a generic
schema error. That matters — the mode object is large and these interactions are
not obvious, so clear enforcement is what makes the endpoint usable.

Four further documented constraints were not exercised (query+prefix-filter
conflict, `accesses` with EPC/TID/USER metadata, `reportFilter` with
EPC/TID/USER, and the `antennaStopCondition`/`query` array lengths). Given the
four tested all passed, the rest are likely enforced too — but that is an
inference, not a result.

### 11. `PUT /cloud/mode` replaces the whole mode object

The reader's original mode carried eight `tagMetaData` fields. Test 10 sets only
`type`, `antennas`, `transmitPower` and `filter` — and its tag events came back
with just `eventNum`, `format`, `idHex`. All eight metadata fields were
**discarded, not merged**.

Same pattern in tests 02, 12 and 13. And in reverse: test 09, which does request
13 fields, receives all 13.

**Every PUT must carry the complete desired configuration.** The safe pattern is
read-modify-write:

```
GET /cloud/mode   → current object
(modify one field)
PUT /cloud/mode   → the full modified object
```

Verified: PUTting the captured baseline object back produced a `GET` that
compared **byte-identical** to the pre-test capture.

**This API now has four different update semantics, none documented:**

| Endpoint | Partial update |
|---|---|
| `PUT /cloud/mode` | **replaces** wholesale |
| `PUT /cloud/config` → `GPIO-LED` | **replaces** wholesale |
| `PUT /cloud/displayConfig` | **merges** every field |
| `PUT /cloud/logs` | **mixed** — `components` merge, `radioPacketLog` resets |

---

## What was not verified

Being explicit, since several tests are "accepted" rather than "proven working":

| Test | Verified | Not verified |
|---|---|---|
| 05, 06 (PORTAL) | Config accepted; reading correctly suppressed until triggered | **The trigger path itself** — needs physical GPI access |
| 13 (`radioStopConditions`) | Accepted and stored | The 60 s auto-stop — the read window was shorter than the duration |
| 16 (`selects`) | Accepted; tags discriminated on TID | Whether the *specific* tags matched were the correct ones — the mask was not computed bit-by-bit |
| 07 (CONVEYOR) | Accepted; tags read with metadata | Whether any conveyor-specific behaviour differs from INVENTORY — the schema defines no conveyor `modeSpecificSettings` |

Antennas 2, 3 and 4 report `disconnected` on this reader, so every test used
antenna 1 only. Multi-antenna behaviour — `antennaStopCondition` cycling,
per-antenna power, `PER_ANTENNA` report filtering across antennas — is untested.

---

## Questions for Zebra

1. **Three broken examples (highest priority).** `simple_basic`
   (`transmitPower: 31.5` > 30.0 max), `with_tag_metadata` (`READER_LOCATION`
   not recognized), `with_accesses` (`wordCounter` should be `wordCount`). All
   three work once corrected. Please fix the examples and, for `wordCounter`, the
   schema too.

2. **`transmitPower` units.** `/cloud/region` reports `maxTxPowerSupported: 300`
   (deci-dBm) while `/cloud/mode` takes 0–30 (dBm). Is that intended? Copying one
   into the other produces a 422.

3. **`READER_LOCATION`.** Rejected as `tagMetaData`, though
   `GET /cloud/readerLocation` exists. Should it be implemented, or removed from
   the enum?

4. **`SIMPLE` mode metadata.** Is the three-field payload intended? There is no
   `tagMetaData` key for this mode, so RSSI and antenna are unobtainable. Worth
   documenting as a mode-selection criterion.

5. **`radioActivity` in `PORTAL` mode.** It reports `active` while the reader is
   armed but reading nothing. Could it distinguish "waiting for trigger" from
   "reading"? As it stands the field cannot be used to health-check a portal.

6. **GPI triggering for test.** Is there any way to drive a GPI transition
   through the API? Without one, `PORTAL` mode's trigger path cannot be validated
   before deployment.

7. **Metadata field naming.** `RSSI`→`peakRssi`, `SEEN_COUNT`→`reads`,
   `HOSTNAME`→`hostName`, and mixed casing in the output. Please document the
   mapping.

8. **`XPC`.** Accepted but never delivered. Silently absent, or not supported?

9. **`USER` read failure.** Returning
   `"Error: tag returned error code 0x03 = Memory overrun"` in the data field is
   indistinguishable by type from real data. Could a failed access be signalled
   structurally?

10. **Throttling `accesses`.** `reportFilter` + `accesses` is prohibited, but
    `reportFilter` is the natural way to limit an access-heavy configuration's
    event rate. What is the recommended approach?

11. **`CONVEYOR` mode settings.** The `modeSpecificSettings` `oneOf` offers only
    `inventorySettings` and `portalSettings`. Is there nothing conveyor-specific
    to configure?

12. **Update semantics.** `PUT /cloud/mode` replaces wholesale. Please state it —
    and note this API has four different behaviours across four endpoints.

---

## Reader state after testing

| | Pre-test | Post-test | |
|---|---|---|---|
| Mode | `CUSTOM`, antenna 1, 17 dBm, 8 metadata fields | **byte-identical** | ✅ |
| Data endpoint | `DATA_AWS_CLOUD_EVENTS` connected | `DATA_AWS_CLOUD_EVENTS` connected | ✅ |
| Radio | inactive | inactive | ✅ |

The baseline mode object was captured before any change and PUT back verbatim at
the end; `GET /cloud/mode` then compared byte-for-byte identical.

The data endpoint was temporarily pointed at the local MQTT broker so tag reads
could be observed, then restored to AWS.

---

## Folder contents

```
01-SIMPLE-spec-example-power-out-of-bounds-REJECTED/
02-SIMPLE-power-30-SUCCESS/
03-INVENTORY-interval-60s-SUCCESS/
04-INVENTORY-interval-5s-SUCCESS/
05-PORTAL-gpi-trigger-ACCEPTED-no-reads/
06-PORTAL-signal-LOW-ACCEPTED-no-reads/
07-CONVEYOR-SUCCESS/
08-CUSTOM-all-14-metadata-REJECTED/
09-CUSTOM-13-metadata-SUCCESS/
10-CUSTOM-filter-prefix-include-SUCCESS/
11-CUSTOM-filter-prefix-exclude-SUCCESS/
12-CUSTOM-reportFilter-SUCCESS/
13-CUSTOM-radioStopConditions-SUCCESS/
14-CUSTOM-accesses-wordCounter-REJECTED/
15-CUSTOM-accesses-READ-TID-SUCCESS/
16-CUSTOM-selects-SUCCESS/
17-cross-field-constraints-enforced/
18-mode-put-replaces-wholesale/
```

Each contains:

| Path | Contents |
|---|---|
| `request body/request.json` | The real request — method, URL, reader, headers, body |
| `response body/response.json` or `.txt` | The response verbatim (0-byte `.txt` = empty 200) |
| `response body/http_status.txt` | HTTP status |
| `response body/verification.txt` | How the result was confirmed and what it revealed |
| `response body/mode_after_GET.json` | What the reader actually stored, read back |
| `response body/tag-evidence/tag_report.json` | Unique tags, total reads, per-reference-tag detail, sample event |
| `response body/tag-evidence/tags_raw.ndjson` | Every tag message captured, verbatim from MQTT |

Bearer tokens are not stored; each `request.json` records the command that mints
one.

The test runner is [`../../mode_test.sh`](../../mode_test.sh) — it stops any
inventory, applies a payload, reads back the stored mode, runs a timed inventory,
and reports what the reference tags did.

---

## Related

| File | Contents |
|---|---|
| [`../SETTINGS_ENDPOINTS_TEST_REPORT.md`](../SETTINGS_ENDPOINTS_TEST_REPORT.md) | The six settings endpoints |
| [`../cloud-config-PUT/CONFIG_TEST_REPORT.md`](../cloud-config-PUT/CONFIG_TEST_REPORT.md) | `PUT /cloud/config` — GPIO-LED and READER-GATEWAY |
| [`../cloud-cloudConfig-PUT/CLOUDCONFIG_TEST_REPORT.md`](../cloud-cloudConfig-PUT/CLOUDCONFIG_TEST_REPORT.md) | Endpoint connection types |
| [`../../findings/`](../../findings/) | Every finding as its own folder with evidence |
