## 1. Description

The `GET /cloud/eSimConfig` REST endpoint retrieves eSIM identity and profiles.

This endpoint returns:

- `eid`
- `imei`
- `profiles` — `profileNickName`, `provider`, `iccid`, `enabled`

Supported on FXR90 only.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_eSimConfig` |
| Pattern Name | eSIM Configuration Query |
| REST Endpoint | `GET /cloud/eSimConfig` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve eSIM identity and profiles |

## 3. When to Use This Endpoint

Use `GET /cloud/eSimConfig` to:

- Read `eid`, `imei`, and `profiles` after `PUT /cloud/eSimConfig`
