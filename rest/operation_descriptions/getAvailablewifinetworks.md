## 1. Description

The `GET /cloud/wifiNetworks` REST endpoint retrieves visible Wi-Fi networks.

This endpoint returns `availableWifiNetworks`. Each item has:

- `essid`
- `signalStrength`
- `capabilities`
- `configuration` — `autoConnect` and optional `security`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_availableWifiNetworks` |
| Pattern Name | Wi-Fi Site Survey |
| REST Endpoint | `GET /cloud/wifiNetworks` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve visible Wi-Fi networks |

## 3. When to Use This Endpoint

Use `GET /cloud/wifiNetworks` to:

- Read `essid`, `signalStrength`, `capabilities`, and `configuration`
