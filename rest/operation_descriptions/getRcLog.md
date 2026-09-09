## 1. Description

The `GET /cloud/logs/RcLog` REST endpoint retrieves the radio-control log archive.

This endpoint returns:

- `filename` — archive name, for example `rcLog.tar.gz`
- `binary` — Base64-encoded `.tar.gz`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_logs_rcLog` |
| Pattern Name | Radio-Control Log Retrieval |
| REST Endpoint | `GET /cloud/logs/RcLog` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the radio-control log archive |

## 3. When to Use This Endpoint

Use `GET /cloud/logs/RcLog` to:

- Download radio-control events as `filename` + `binary`
