## 1. Description

The `GET /cloud/logs` REST endpoint retrieves the current log configuration.

This endpoint returns:

- `radioPacketLog` — `true` or `false`
- `components` — `componentName` and `level` for `radio_control` and `reader_gateway`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_logs` |
| Pattern Name | Log Configuration Query |
| REST Endpoint | `GET /cloud/logs` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve log configuration |

## 3. When to Use This Endpoint

Use `GET /cloud/logs` to:

- Read `radioPacketLog` and component levels after `PUT /cloud/logs`
