## 1. Description

The `GET /cloud/logs/syslog` REST endpoint retrieves the system log archive.

This endpoint returns:

- `filename` — archive name, for example `syslog.tar.gz`
- `binary` — Base64-encoded `.tar.gz`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_logs_syslog` |
| Pattern Name | Syslog Retrieval |
| REST Endpoint | `GET /cloud/logs/syslog` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the system log archive |

## 3. When to Use This Endpoint

Use `GET /cloud/logs/syslog` to:

- Download OS events as `filename` + `binary`
