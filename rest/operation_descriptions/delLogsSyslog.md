## 1. Description

The `DELETE /cloud/logs/syslog` REST endpoint deletes stored system log files.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `del_logs_syslog` |
| Pattern Name | Syslog Purge |
| REST Endpoint | `DELETE /cloud/logs/syslog` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Request Body | None |

## 3. Before You Begin

Download first with `GET /cloud/logs/syslog` if you need to keep the files.
