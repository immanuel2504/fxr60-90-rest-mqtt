## 1. Description

The `GET /cloud/network` REST endpoint retrieves the reader's network configuration.

This endpoint returns:

- `hostName`
- `networkInterface` — `eth0`, `mlan0`, `bnep0`, `wan0`, `uap0`

Optional request field:

- `interface` — `eth0`, `mlan0`, `bnep0`, `wan0`, `uap0`, or `all`

Omit the body, or send `{}`, to return every interface. `wan0` is FXR90 only.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_network` |
| Pattern Name | Network Configuration Query |
| REST Endpoint | `GET /cloud/network` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve network configuration |

## 3. When to Use This Endpoint

Use `GET /cloud/network` to:

- Read `hostName` and `networkInterface` after `PUT /cloud/network`
