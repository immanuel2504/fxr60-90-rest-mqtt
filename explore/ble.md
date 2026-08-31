# BLE scanner

BLE here is the **scanner**. The reader listens for Bluetooth Low Energy advertisements: badges, iBeacons, AltBeacon, Eddystone, and generic BLE devices.

It is **not** Bluetooth PAN (`bnep0`). That is “pair a laptop to reach the reader.” BLE is “see tags and beacons in the air.”

Applies to **FXR60 and FXR90**. Firmware **4.0.11** or later (`GET /cloud/version` → `readerApplication`). On older builds, `/cloud/bleConfig` and `scanType` are not available.

Path is **`/cloud/bleConfig`** (camelCase), not `ble-config`.

---

## Endpoints

| # | Method | Path | MQTT | What it does |
|---|---|---|---|---|
| 1 | `GET` | `/cloud/bleConfig` | `get_bleConfig` | Read scanner settings |
| 2 | `PUT` | `/cloud/bleConfig` | `set_bleConfig` | Change scanner settings. **`ble.enable` is required.** Does **not** start a scan. |
| 3 | `PUT` | `/cloud/start` | `start` | Start listening: `{ "scanType": ["ble"] }` |
| 4 | `PUT` | `/cloud/stop` | `stop` | Stop listening: `{ "scanType": ["ble"] }` |
| 5 | `GET` | `/cloud/status` | `get_status` | Is BLE `running`? Beacon counts |

Auth: Bearer token.

`GET /cloud/network` with `{ "interface": "blescan" }` is only the BLE **network interface** name. Config and start/stop are the calls above.

**Enable ≠ start.** `PUT /cloud/bleConfig` with `enable: true` only allows the scanner. `PUT /cloud/start` is what actually listens.

BLE **never auto-resumes** after reboot. Start it again with `/cloud/start`. RFID can persist; BLE does not.

---

## Scenario A — Warehouse door: hear BLE badges

A warehouse door has an FXR60. People wear a **BLE badge** (iBeacon). The site wants a count when someone walks through — not only when a carton with an RFID tag passes.

They do **not** pair a laptop (`bnep0`). They do **not** plug in a monitor (display). They only want the reader to **listen**.

| They need | BLE does this |
|---|---|
| Know a person/badge is at the door | Hear the badge’s iBeacon advertisements |
| Ignore far-away beacons | RSSI filter (only strong / nearby signals) |
| Hear only *their* beacons | Filter by UUID / protocol |
| Start listening at shift start | `PUT /cloud/start` `{ "scanType": ["ble"] }` |
| Stop at shift end | `PUT /cloud/stop` `{ "scanType": ["ble"] }` |

### Steps

**1. Configure** — allow the scanner (not listening yet):

```http
PUT /cloud/bleConfig
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "ble": {
    "enable": true
  }
}
```

**2. Start** — actually listen:

```http
PUT /cloud/start
```

```json
{
  "scanType": ["ble"]
}
```

**3. Someone with a badge walks past.** The reader sees BLE ads and reports them (status counts / data events).

**4. Check**

```http
GET /cloud/status
```

`ble.scanState` should be `running`. `ble.beaconCounts` go up if ads are seen.

**5. Stop**

```http
PUT /cloud/stop
```

```json
{
  "scanType": ["ble"]
}
```

If they skip step 2, config is saved but **nothing is scanning**.

---

## When they do **not** use BLE

| Situation | Use this instead |
|---|---|
| Laptop must talk to the reader with no Ethernet | `bnep0` (Bluetooth PAN) |
| Read cartons / RFID labels | RFID `PUT /cloud/start` (empty body or `scanType: ["rfid"]`) |
| Show a page on a monitor | Display (`/cloud/displayConfig`) |

---

## vs `bnep0`

| | BLE (`bleConfig` + start) | Bluetooth PAN (`bnep0`) |
|---|---|---|
| Job | Hear beacons / BLE ads | Pair a laptop to manage the reader |
| You pair a phone? | No | Yes |
| Start with | `PUT /cloud/start` `scanType: ["ble"]` | Pair in Bluetooth settings |

---

## `PUT /cloud/bleConfig` fields

Required: `ble` object and **`ble.enable`**.

| Field | Meaning |
|---|---|
| `ble.enable` | Required. `true` = scanner allowed, `false` = off |
| `ble.scanIntervalSec` | How often to collect results (`0`–`300` seconds) |
| `ble.additionalFilters.rssi` | Drop weak signals (`-127` to `0` dBm; e.g. `-70`) |
| `ble.additionalFilters.serviceUuids16` | 16-bit service UUID list |
| `ble.additionalFilters.serviceUuids128` | 128-bit service UUID list |
| `ble.protocols.iBeacon` | iBeacon on/off + UUID / major / minor / txPower filters |
| `ble.protocols.altBeacon` | AltBeacon filters (mfgId, beaconId, major, minor, refRssi) |
| `ble.protocols.eddystone` | Eddystone `URL` / `UID` / `EID` / `TLM` |
| `ble.protocols.generic` | Specific BLE MAC / name (`addressType`: `public` or `random`) |

### Minimal on

```json
{
  "ble": {
    "enable": true
  }
}
```

### Minimal off

```json
{
  "ble": {
    "enable": false
  }
}
```

### Enable + interval

```json
{
  "ble": {
    "enable": true,
    "scanIntervalSec": 5
  }
}
```

### Enable + RSSI filter (ignore weak / far ads)

```json
{
  "ble": {
    "enable": true,
    "scanIntervalSec": 10,
    "additionalFilters": {
      "rssi": -70
    }
  }
}
```

Shorter `scanIntervalSec` = more responsive, more data. RSSI closer to `0` = stronger signal only.

---

## Scenario B — Full protocol filters (hear only chosen beacons)

Use when the warehouse has mixed BLE noise and you only want known badges / frames.

```json
{
  "ble": {
    "enable": true,
    "scanIntervalSec": 5,
    "protocols": {
      "iBeacon": {
        "enabled": true,
        "filters": [
          {
            "uuid": "FDA50693-A4E2-4FB1-AFCF-C6EB07647825",
            "major": 10001,
            "minor": 20002,
            "txPower": -59
          }
        ]
      },
      "altBeacon": {
        "enabled": true,
        "filters": [
          {
            "mfgId": "0118",
            "beaconId": "2F234454-CF6D-4A0F-ADF2-F4911BA9FFA7",
            "major": 4,
            "minor": 4,
            "refRssi": -100
          }
        ]
      },
      "eddystone": {
        "enabled": true,
        "filters": [
          {
            "frameType": "URL",
            "txPower": -59,
            "url": "https://www.zebra.com"
          },
          {
            "frameType": "UID",
            "txPower": -18,
            "namespace": "0102030405060708090A",
            "instance": "000000000001"
          },
          {
            "frameType": "EID",
            "txPower": -18,
            "ephemeralId": "0102030405060708"
          }
        ]
      },
      "generic": {
        "enabled": true,
        "filters": [
          {
            "address": "7E:41:25:1E:D5:16",
            "addressType": "random",
            "name": "BLEPeripheralApp",
            "alias": "BLEPeripheralApp"
          }
        ]
      }
    },
    "additionalFilters": {
      "rssi": -80,
      "serviceUuids16": ["FEAA", "FE9B"],
      "serviceUuids128": ["FDA50693-A4E2-4FB1-AFCF-C6EB07647825"]
    }
  }
}
```

Then still `PUT /cloud/start` with `{ "scanType": ["ble"] }`.

Eddystone `frameType` values in the spec: `URL`, `UID`, `EID`, `TLM`.  
Generic `addressType`: `public` or `random`.

---

## Scenario C — Confirm config (GET)

```http
GET /cloud/bleConfig
```

No body. You get the same `ble` object you configured.

Example when disabled:

```json
{
  "ble": {
    "enable": false
  }
}
```

Use GET to verify `ble.enable` is `true` **before** start. If enable is `false`, BLE inventory will not start.

---

## Scenario D — Start and stop (RFID vs BLE)

**BLE only:**

```json
{ "scanType": ["ble"] }
```

**RFID only** (or empty body on older firmware): `scanType: ["rfid"]` or `{}`.

**Both:**

```json
{ "scanType": ["ble", "rfid"] }
```

Same `scanType` shape on **stop**. Stopping BLE does not stop RFID if both were running (stop only what you list).

`applyImpinjGen2X: true` cannot be combined with a BLE-only start (`scanType: ["ble"]`).

Firmware older than 4.0.11: omit `scanType`; start/stop is RFID only.

---

## Scenario E — What status provides while scanning

```http
GET /cloud/status
```

The `ble` section is present only when BLE is supported and status is available:

```json
"ble": {
  "scanState": "running",
  "scanStartTime": "2026-05-21T13:46:16.955Z",
  "beaconCounts": {
    "total": 108,
    "iBeacon": 75,
    "altBeacon": 33,
    "eddystone": 0,
    "generic": 0
  }
}
```

| Field | Meaning |
|---|---|
| `ble.scanState` | `running` or `stopped` |
| `ble.scanStartTime` | When this scan started (ISO 8601) |
| `ble.beaconCounts.total` | Ads seen in the current window |
| `ble.beaconCounts.iBeacon` / `altBeacon` / `eddystone` / `generic` | Counts by protocol |

`running` + `total` staying `0` usually means no beacons in range, or filters are too tight (RSSI / UUID).

---

## Related example files in this repo

| File | What it is |
|---|---|
| `rest/operation_examples/cloud-bleconfig/PUT/enable_ble.json` | Minimal enable |
| `rest/operation_examples/cloud-bleconfig/PUT/disable_ble.json` | Minimal disable |
| `rest/operation_examples/cloud-bleconfig/PUT/enable_with_interval.json` | Interval 5 s |
| `rest/operation_examples/cloud-bleconfig/PUT/enable_with_rssi_filter.json` | RSSI −70 |
| `rest/operation_examples/cloud-bleconfig/PUT/enable_with_protocols.json` | Protocol filters |
| `rest/operation_examples/cloud-bleconfig/GET/disabled.json` | GET when off |
| `rest/operation_examples/cloud-bleconfig/GET/inline.json` | GET with full filters |
| `rest/operation_examples/cloud-start/PUT/start_Global_BLE_only.json` | Start BLE |
| `rest/operation_examples/cloud-stop/PUT/stop_Global_BLE_only.json` | Stop BLE |
