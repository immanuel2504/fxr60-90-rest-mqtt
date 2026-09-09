## 1. Description

The `GET /cloud/apps` REST endpoint retrieves the user applications installed on the reader.

This endpoint returns an array. Each item has:

- `appname`
- `runningStatus`
- `autostart`
- `metadata`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_userapps` |
| Pattern Name | User Application Inventory Query |
| REST Endpoint | `GET /cloud/apps` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve installed user applications |

## 3. When to Use This Endpoint

Use `GET /cloud/apps` to:

- Read installed names before `PUT /cloud/apps/{appname}/start`, `PUT /cloud/apps/{appname}/stop`, or `PUT /cloud/apps/{appname}/uninstall`
