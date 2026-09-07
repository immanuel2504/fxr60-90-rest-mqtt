# FXR60 BLE — `PUT /cloud/bleConfig` Test Report

Every BLE example from the latest spec, tested against a live reader, with real
beacons in range.

## Scope

| | |
|---|---|
| Spec | `openAPISpec 11.yaml` — **IoT Connector REST API v3.0.0** |
| Endpoints | `PUT /cloud/bleConfig` (`setBleConfig`), `GET /cloud/bleConfig` |
| Reader | `10.233.48.36`, reader app 5.0.7 |
| Date | 2026-09-06 |
| Spec examples | **5** |
| Extra tests | 2 — the corrected example, and the bisection that found the defect |
| Beacons in range | 4 unique addresses — iBeacon and altBeacon both decoded |

BLE start/stop is covered separately in
[`START_STOP_TEST_REPORT.md`](../cloud-start-PUT/START_STOP_TEST_REPORT.md).

---

## Results

**4 of 5 spec examples work. One is rejected — and it's the most detailed one.**

| # | Example | Result |
|---|---|---|
| 1 | `enable_ble` | ✅ 200, stored |
| 2 | `enable_with_interval` | ✅ 200, `interval=5` stored |
| 3 | `enable_with_rssi_filter` | ✅ 200 — **filter proven to work** |
| 4 | `enable_with_protocols` | ❌ **422 — spec casing bug** |
| 4b | `enable_with_protocols` **corrected** | ✅ 200, all filters stored |
| 5 | `disable_ble` | ✅ 200, `enable=false` |

Example 4 fails only because of **field-name casing in the `generic` filter**. A
one-line documentation fix makes it work — test 4b proves it.

---

## Findings

### 1. 🐛 The `enable_with_protocols` example is rejected — capitalised `generic` filter fields

The spec's most detailed example, sent verbatim:

```json
→ 422 {"code":3,"message":"CS:'setBleConfig' failed, Reason: Invalid BLE configuration: unknown or unexpected field in request payload, refer to API documentation for supported fields"}
```

**Isolated by bisection.** First, each protocol block alone with its filters:

| Block | Result |
|---|---|
| `iBeacon` + filters | ✅ 200 |
| `altBeacon` + filters | ✅ 200 |
| `eddystone` URL frame | ✅ 200 |
| **`generic` + filters** | ❌ **422** |
| `additionalFilters` (all three) | ✅ 200 |

Then each `generic` field, capitalised vs lowercase:

| Spec's example | | Firmware wants | |
|---|---|---|---|
| `"Address"` | ❌ 422 | `"address"` | ✅ 200 |
| `"AddressType"` | ❌ 422 | `"addressType"` | ✅ 200 |
| `"Name"` | ❌ 422 | `"name"` | ✅ 200 |
| `"Alias"` | ❌ 422 | `"alias"` | ✅ 200 |

All four capitalised names rejected, all four lowercase accepted — a naming
convention, not a per-field quirk. Each lowercase field was then confirmed to
**persist** by read-back.

**Why the spec probably has it wrong.** The reader's BLE *output* uses
capitalised names. A real captured `BLE_DATA` event:

```json
{"data": {"Address": "F7:17:BB:3A:7B:A1", "AddressType": "random",
          "Alias": "F7-17-BB-3A-7B-A1", "RSSI": -65,
          "beaconType": "IBEACON",
          "iBeacon": {"major": 10001, "minor": 20002, "txPower": -59,
                      "uuid": "FDA50693-A4E2-4FB1-AFCF-C6EB07647825"}}}
```

The example looks like **output field names pasted into an input filter**. The
schema sets `additionalProperties: false` on this object, so the wrong casing is
a hard 422 rather than being silently ignored — correct strict behaviour, applied
to an example that doesn't match it.

**Fix:** lowercase the four field names in the example. Test 4b is that payload,
accepted with 200 and everything stored.

### 2. ✅ The RSSI filter genuinely filters — measured A/B

Two 20-second scans, identical but for the filter, with data captured off the
local MQTT broker:

| | `additionalFilters` | BLE events | Unique | RSSI range |
|---|---|---|---|---|
| **A** | `{}` | **78** | 4 | −86 … −63 |
| **B** | `{"rssi": -60}` | **0** | 0 | — |

Every beacon in range was weaker than −60 dBm (strongest −63), so a −60 threshold
correctly excluded all of them. Scan A proves the beacons were present and
decoding; scan B proves the filter suppressed them.

Beacon types decoded in scan A: `IBEACON` 39, `ALTBEACON` 39. The reader's own
`GET /cloud/status → ble.beaconCounts` gives a second independent view
(altBeacon 73, eddystone 131, generic 265, iBeacon 86 across the session).

This is the strongest evidence in the BLE set — a real radio measurement rather
than a stored flag.

### 3. `protocols` merges — it does not replace

`enable_ble` names **only** `iBeacon`:

```json
{"ble": {"enable": true, "scanIntervalSec": 0,
         "protocols": {"iBeacon": {"enabled": true}}, "additionalFilters": {}}}
```

Read back:

```
protocols enabled: altBeacon=true  eddystone=true  generic=true  iBeacon=true
```

The three protocols absent from the request kept their previous state. **Sending
one protocol does not disable the others.**

That's the opposite of `GPIO-LED` in `PUT /cloud/config`, which replaces
wholesale. Neither is documented — see
[finding 13](../../findings/cloud-config/13-gpio-led-replaces-wholesale/finding.md).

Meanwhile the four **top-level** keys (`enable`, `scanIntervalSec`,
`additionalFilters`, `protocols`) *are* all required, as the schema states.

> **Correction to an earlier note.** During `/cloud/start` testing I recorded
> that bleConfig "requires the full object — a minimal `{"ble":{"enable":true}}`
> is rejected." The first half was wrong. `{"ble":{"enable":true}}` fails for
> **missing top-level keys**, not because every protocol must be listed —
> `protocols` needs only one protocol inside it, exactly as `enable_ble` shows.

### 4. ⚠️ `ble.enable: false` blocks BLE scanning with a misleading error

After `disable_ble`:

```json
PUT /cloud/start {"scanType":["ble"]}
→ 422 {"code":3,"message":"CS:'startBleScan' failed, Reason: Invalid BLE configuration: unknown or unexpected field in request payload, refer to API documentation for supported fields"}
```

The start payload has **one field**, it matches the schema, and nothing about it
is unknown or unexpected. The real cause is this config setting, which the
message never mentions.

**The same message, from two endpoints, for two different causes:**

| Endpoint | Cause | Message accuracy |
|---|---|---|
| `PUT /cloud/bleConfig` | capitalised `generic` fields | ✅ accurate (finding 1) |
| `PUT /cloud/start` | `ble.enable: false` | ❌ **misleading** |

**Ask:** make the start error name the real cause, e.g. *"BLE scanning is
disabled; set `ble.enable: true` via `PUT /cloud/bleConfig` first"*.

### 5. ✅ Per-protocol flags are independent of the master switch

After `disable_ble`, the protocols stay `enabled: true` while `ble.enable` is
`false`. Sensible — the protocol selection is preserved for the next time BLE is
turned on, rather than being reset.

### 6. `scanIntervalSec: 0` is accepted but undocumented

The schema allows `0–300`, and `enable_ble` uses `0`. Accepted and stored, but
the description says only *"integer"* — is `0` continuous scanning, or scan-once?
Worth clarifying, since it's the value the first example uses.

Values `0`, `1`, `5` and `10` were all stored verbatim, so the field is honoured
rather than clamped.

**Not verified:** the timing *effect* of the interval. Measuring that needs
beacon arrival timestamps compared across intervals, which wasn't run.

### 7. ✅ Filter coverage confirmed by test 4b

The corrected example exercises every documented filter type in one request, all
stored and read back:

| Protocol | Fields confirmed |
|---|---|
| `iBeacon` | `uuid`, `major`, `minor`, `txPower` |
| `altBeacon` | `mfgId`, `beaconId`, `major`, `minor`, `refRssi` |
| `eddystone` | all three frame types — `URL`, `UID` (`namespace`+`instance`), `EID` (`ephemeralId`) |
| `generic` | `address`, `addressType`, `name`, `alias` (lowercase) |
| `additionalFilters` | `rssi`, `serviceUuids16`, `serviceUuids128` |

---

## Questions for Zebra

1. **`enable_with_protocols` casing (highest priority).** The `generic` filter in
   the spec's example uses `Address`, `AddressType`, `Name`, `Alias`; the firmware
   requires `address`, `addressType`, `name`, `alias` and hard-rejects the
   capitalised forms via `additionalProperties: false`. Please lowercase them in
   the example. Related: should input and output use the same casing? Output is
   capitalised (`Address`, `RSSI`), which is where the confusion originates.

2. **The `startBleScan` error message.** `PUT /cloud/start {"scanType":["ble"]}`
   with BLE disabled returns *"unknown or unexpected field in request payload"*.
   The payload has one valid field. Please name the real cause.

3. **`protocols` merge semantics.** Sending one protocol leaves the others
   untouched. Intended? Please document it — `GPIO-LED` in `PUT /cloud/config`
   does the opposite, so a client cannot infer either.

4. **`scanIntervalSec: 0`.** What does 0 mean — continuous, or scan-once? It's
   the value in the first example.

5. **`generic` filter matching semantics.** With `address`, `name` and `alias`
   all set, is the match AND or OR? The schema says `minProperties: 1` but not how
   multiple fields combine.

---

## Reader state after testing

| | Pre-test | Post-test | |
|---|---|---|---|
| `bleConfig` | full object, `enable: false`, `interval: 1`, all 4 protocols enabled, no filters | **byte-identical** | ✅ |
| `ble.scanState` | `stopped` | `stopped` | ✅ |
| Data endpoint | `DATA_AWS_CLOUD_EVENTS` connected | same | ✅ |

Confirmed byte-identical by comparing the full `GET /cloud/bleConfig` JSON before
and after. The data endpoint was temporarily routed to the local MQTT broker to
capture the finding-2 measurement, then restored to AWS.

---

## Folder contents

This report lives beside the tests it describes:

```
cloud-bleConfig-PUT/
├── BLE_TEST_REPORT.md          ← this file
├── 01-enable_ble-SUCCESS/
├── 02-enable_with_interval-SUCCESS/
├── 03-enable_with_rssi_filter-SUCCESS-filter-proven/
│   └── response body/beacon-scan-evidence.txt   ← the A/B measurement
├── 04-enable_with_protocols-REJECTED-spec-casing-bug/
├── 04b-enable_with_protocols-CORRECTED-SUCCESS/
├── 05-disable_ble-SUCCESS/
└── 06-generic-filter-casing-bisect/
```

Each holds `request body/request.json` (with the spec example name in
`specExampleName`), `response body/` with the verbatim response,
`http_status.txt`, and `verification.txt`.

Successful calls return HTTP 200 with an **empty body** — stored as a 0-byte
`response.txt`.

The runner is [`../ble_test.sh`](../../ble_test.sh): it applies a payload, reads the
config back, and optionally runs a timed BLE scan reporting beacon counts.

> **Method note.** One observation in test 4b initially looked like a defect —
> only `addressType` appeared stored out of four fields sent. Re-testing each
> field individually, then all four together with a longer settle, showed all
> four persist. The first read was simply too soon and returned the previous
> test's state. It is **not** reported as a finding; recorded here because the
> same trap applies to any read-back on this endpoint.

---

## Related

| File | Contents |
|---|---|
| [`START_STOP_TEST_REPORT.md`](../cloud-start-PUT/START_STOP_TEST_REPORT.md) | `start`/`stop` incl. BLE scan control — all 10 examples |
| [`cloud-mode-PUT/MODE_TEST_REPORT.md`](../cloud-mode-PUT/MODE_TEST_REPORT.md) | `PUT /cloud/mode` — all five RFID modes |
| [`../findings/`](../../findings/) | Every finding as its own folder with evidence |
