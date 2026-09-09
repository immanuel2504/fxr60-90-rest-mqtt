## 1. Description

The `GET /cloud/logs/RgWarningLog` REST endpoint retrieves the reader-gateway warning log archive.

This endpoint returns:

- `filename` — archive name, for example `rgWarningLog.tar.gz`
- `binary` — Base64-encoded `.tar.gz`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_logs_rgWarningLog` |
| Pattern Name | Reader-Gateway Warning Log Retrieval |
| REST Endpoint | `GET /cloud/logs/RgWarningLog` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the reader-gateway warning log archive |

## 3. When to Use This Endpoint

Use `GET /cloud/logs/RgWarningLog` to:

- Download reader-gateway warnings as `filename` + `binary`
