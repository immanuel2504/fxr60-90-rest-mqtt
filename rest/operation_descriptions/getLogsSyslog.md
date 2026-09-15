## 1. Description

The `GET /cloud/logs/syslog` REST endpoint retrieves the reader's current active system log.

This endpoint returns:

- `filename` — log archive name, for example `syslog.tar.gz`
- `binary` — a standard Base64-encoded string representing the raw `.tar.gz` byte stream

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_logs_syslog` |
| Pattern Name | Syslog Retrieval |
| REST Endpoint | `GET /cloud/logs/syslog` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the current active system log |

## 3. When to Use This Endpoint

Use `GET /cloud/logs/syslog` to:

- Download the current system log as `filename` and `binary`
- Collect diagnostics while the reader is running
