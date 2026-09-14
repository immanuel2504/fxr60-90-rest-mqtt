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

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `essid` | Which network is this? | The broadcast SSID name shown to users when choosing a network. |
| `signalStrength` | Is the signal strong enough to connect? | Reported as a percentage; low values mean an unreliable connection. |
| `capabilities` | What security modes does the access point advertise? | Array of strings such as `WPA2`, `WPA2-802.1X`, `WPA3`, `WPA3-802.1X`. Confirms which authentication methods the reader can use to join. |
| `configuration.autoConnect` | Is the reader set to join this network automatically? | `true` means the reader connects to this network without manual action. |
| `configuration.security` | What credentials are configured for this network? | Present only when security settings have been saved for this `essid`. Includes `type` (security mode) and, for enterprise modes, `details` (`auth`, `innerAuth`, `username`, `password`, `cert`). |
