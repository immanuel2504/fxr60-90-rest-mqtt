## 1. Description

The `GET /cloud/networkInterfaces` REST endpoint retrieves the network interface names on the reader.

This endpoint returns:

- `availableNetworkInterfaces` — names such as `eth0`, `mlan0`, `bnep0`, `uap0`

`wan0` is present on FXR90 only.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_networkInterfaces` |
| Pattern Name | Network Interface Query |
| REST Endpoint | `GET /cloud/networkInterfaces` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve network interface names |

## 3. When to Use This Endpoint

Use `GET /cloud/networkInterfaces` to:

- Read `availableNetworkInterfaces`
