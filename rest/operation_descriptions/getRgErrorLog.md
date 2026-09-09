## 1. Description

The `GET /cloud/logs/RgErrorLog` REST endpoint retrieves the reader-gateway error log archive.

This endpoint returns:

- `filename` — archive name, for example `rgErrorLog.tar.gz`
- `binary` — Base64-encoded `.tar.gz`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_logs_rgErrorLog` |
| Pattern Name | Reader-Gateway Error Log Retrieval |
| REST Endpoint | `GET /cloud/logs/RgErrorLog` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the reader-gateway error log archive |

## 3. When to Use This Endpoint

Use `GET /cloud/logs/RgErrorLog` to:

- Download reader-gateway errors as `filename` + `binary`
