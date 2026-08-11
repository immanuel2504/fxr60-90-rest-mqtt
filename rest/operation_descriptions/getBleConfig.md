## 1. Description

The `GET /cloud/bleConfig` REST endpoint retrieves the current Bluetooth Low Energy (BLE) scanner configuration from the reader.

This endpoint returns:

- Whether BLE scanning is enabled
- Scan interval and window settings
- RSSI filtering threshold
- iBeacon, AltBeacon, Eddystone, and generic BLE advertisement filter settings

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| REST Endpoint | `GET /cloud/bleConfig` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Firmware Requirement | BLE requires reader build **4.0.11** or later. On earlier builds this endpoint is not available. |

## 3. When to Use This Endpoint

Use `GET /cloud/bleConfig` to:

- Verify BLE scanning is enabled before starting a BLE inventory scan
- Review scan interval and RSSI filter settings before modifying them
- Confirm iBeacon, AltBeacon, Eddystone, or generic BLE filter configuration
- Verify the effect of a prior `PUT /cloud/bleConfig` call

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `ble.enable` | Is BLE scanning enabled? | BLE inventory will not start if scanning is disabled. |
| `ble.scanIntervalSec` | What is the configured scan interval? | Determines how frequently the reader actively listens for BLE advertisements. |
| `ble.additionalFilters.rssi` | What is the RSSI threshold? | Tags or beacons below this threshold are filtered out of scan results. |
| Beacon type filters | Which beacon types are included? | Only enabled beacon types will appear in BLE tag data events. |
