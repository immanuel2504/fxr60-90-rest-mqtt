## 1. Description

The `PUT /cloud/bleConfig` REST endpoint sets the BLE scanner configuration.

This endpoint requires:

- `ble.enable`
- `ble.scanIntervalSec` — `0` to `300`
- `ble.protocols`
- `ble.additionalFilters`

Optional inside `ble.protocols`:

- `iBeacon`, `altBeacon`, `eddystone`, `generic` — each with `enabled`, and optional `filters`

Optional inside `ble.additionalFilters`:

- `rssi` — `-127` to `0`
- `serviceUuids16`
- `serviceUuids128`

When `generic.filters` is sent, use `address`, `addressType`, `name`, and `alias`.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_bleConfig` |
| Pattern Name | BLE Configuration Update |
| REST Endpoint | `PUT /cloud/bleConfig` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `ble.enable`, `ble.scanIntervalSec`, `ble.protocols`, `ble.additionalFilters` |

## 3. Before You Begin

Decide the scanner settings. Use the JSON field names below.

| Field | What to set |
|---|---|
| `ble.enable` | `true` to allow BLE scanning, `false` to not. |
| `ble.scanIntervalSec` | Scan interval in seconds. `0` to `300`. |
| `ble.protocols` | Protocol object. Include at least one of `iBeacon`, `altBeacon`, `eddystone`, or `generic`. |
| `ble.protocols.*.enabled` | `true` or `false` for that protocol. |
| `ble.protocols.iBeacon.filters` | Optional. `uuid`, `major`, `minor`, `txPower`. |
| `ble.protocols.altBeacon.filters` | Optional. `mfgId`, `beaconId`, `major`, `minor`, `refRssi`. |
| `ble.protocols.eddystone.filters` | Optional. `frameType` `URL`, `UID`, `EID`, or `TLM`, plus `url`, `namespace`/`instance`, or `ephemeralId`. |
| `ble.protocols.generic.filters` | Optional. `address`, `addressType` (`public` or `random`), `name`, `alias`. |
| `ble.additionalFilters` | Required object. Use `{}` when empty. |
| `ble.additionalFilters.rssi` | Optional. Drop weaker advertisements. `-127` to `0`. |
| `ble.additionalFilters.serviceUuids16` | Optional. 16-bit service UUIDs. |
| `ble.additionalFilters.serviceUuids128` | Optional. 128-bit service UUIDs. |
