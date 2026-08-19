## 1. Description

The `GET /cloud/status` REST endpoint retrieves operational statistics and health information from the reader at the moment of the request.

This endpoint returns:

- Uptime and current system time
- Radio connection and activity state
- Reader temperature
- CPU and RAM usage
- Flash storage usage by partition
- Antenna port connection states
- NTP synchronization status
- Cloud interface connection status
- Power source and power-negotiation state
- Active Impinj Gen2X feature status (when a Gen2X feature is running)
- BLE scanner runtime status (scan state, scan start time, and beacon counts by protocol)

The `ble` section is present only when BLE is supported and its status is available. No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Reader Status Query |
| REST Endpoint | `GET /cloud/status` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve live operational statistics and health |

## 3. When to Use This Endpoint

Use `GET /cloud/status` to:

- Confirm the reader is powered, healthy, and reachable
- Verify the radio is connected before starting inventory
- Monitor reader temperature for thermal issues
- Synchronize against the reader's current system time
- Check CPU, RAM, and flash usage during high-load scenarios
- Confirm BLE scanning is active and review beacon counts by protocol

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `uptime` | How long has the reader been running? | Long uptimes confirm stability; short uptimes indicate an unexpected restart. |
| `radioConnection` | Is the value `connected`? | Inventory cannot run if the radio is disconnected. |
| `radioActivity` | Is it `active` or `inactive`? | Confirms whether an inventory session is currently in progress. |
| `temperature` | Is the value within safe operating range? | Excessive temperature can cause throttling or hardware faults. |
| `antennas` | Are expected ports `connected`? Only ports present on this reader are listed — not every reader has 8 antennas. | A `disconnected` antenna port means tags on that port will not be read. |
| `ntp.offset` | Is the offset near zero? | A large NTP offset means event timestamps may be inaccurate. |
| `ble.scanState` | Is the value `running`? | Confirms whether the BLE scanner is currently active (`running`) or `stopped`. |
| `ble.scanStartTime` | When did the current scan start? | ISO 8601 timestamp marking when BLE scanning last started. |
| `ble.beaconCounts` | Are advertisements being seen? | Per-protocol counts (`iBeacon`, `altBeacon`, `eddystone`, `generic`, `total`) confirm beacons are being detected in the current scan window. |

## 4. BLE Status Fields

When BLE is supported and active, the response includes a `ble` object:

| Field | Type | Description |
|---|---|---|
| `ble.scanState` | string | Current BLE scanner state — `running` or `stopped`. |
| `ble.scanStartTime` | string (date-time) | ISO 8601 timestamp of when the BLE scan was last started. |
| `ble.beaconCounts.total` | integer | Total BLE advertisements observed in the current scan window. |
| `ble.beaconCounts.iBeacon` | integer | Number of iBeacon advertisements observed. |
| `ble.beaconCounts.altBeacon` | integer | Number of AltBeacon advertisements observed. |
| `ble.beaconCounts.eddystone` | integer | Number of Eddystone advertisements observed. |
| `ble.beaconCounts.generic` | integer | Number of generic BLE advertisements observed. |

Example `ble` section:

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
