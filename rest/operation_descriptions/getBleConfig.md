## 1. Description

The `GET /cloud/bleConfig` REST endpoint retrieves the BLE scanner configuration currently saved on the reader.

The response always includes all four fields. The reader stores a full BLE object, even when scanning is disabled:

- `ble.enable`
- `ble.scanIntervalSec`
- `ble.protocols`
- `ble.additionalFilters`

`PUT /cloud/bleConfig` must send those same four fields on every request. Use this GET to confirm what was saved before `PUT /cloud/start` with `scanType: ["ble"]`.

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_bleConfig` |
| REST Endpoint | `GET /cloud/bleConfig` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Always-present fields | `ble.enable`, `ble.scanIntervalSec`, `ble.protocols`, `ble.additionalFilters` |
| Firmware Requirement | BLE requires reader build **4.0.11** or later. On earlier builds this endpoint is not available. |

## 3. When to Use This Endpoint

Use `GET /cloud/bleConfig` to:

- Confirm all four saved fields, not only `enable`
- Check `scanIntervalSec`, `protocols`, and `additionalFilters` before starting a BLE scan
- Verify generic filter names are lowercase (`address`, `addressType`, `name`, `alias`)
- Verify the effect of a prior `PUT /cloud/bleConfig` call

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `ble.enable` | Is scanning turned on? | BLE start will not scan if this is `false`. |
| `ble.scanIntervalSec` | What is the scan interval? | Always present. Range `0`–`300`. |
| `ble.protocols` | Which beacon types are enabled, and which filters? | Always present. Includes iBeacon, altBeacon, eddystone, and generic. |
| `ble.additionalFilters` | RSSI and service UUID filters | Always present. May be `{}` when no extra filters are set. |
