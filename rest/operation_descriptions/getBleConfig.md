## 1. Description

The `GET /cloud/bleConfig` REST endpoint retrieves the BLE scanner configuration.

This endpoint returns:

- `ble.enable`
- `ble.scanIntervalSec`
- `ble.protocols`
- `ble.additionalFilters`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_bleConfig` |
| Pattern Name | BLE Configuration Query |
| REST Endpoint | `GET /cloud/bleConfig` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve BLE scanner configuration |

## 3. When to Use This Endpoint

Use `GET /cloud/bleConfig` to:

- Read the settings last applied with `PUT /cloud/bleConfig`
