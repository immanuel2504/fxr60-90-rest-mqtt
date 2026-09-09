## 1. Description

The `GET /cloud/gpo` REST endpoint retrieves the current output state of each GPO pin.

This endpoint returns:

- `1`, `2`, `3`, `4` — `HIGH` or `LOW`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_gpoStatus` |
| Pattern Name | GPO Status Query |
| REST Endpoint | `GET /cloud/gpo` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve GPO pin states |

## 3. When to Use This Endpoint

Use `GET /cloud/gpo` to:

- Read pin states before or after `PUT /cloud/gpo`
