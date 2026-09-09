## 1. Description

The `GET /cloud/ntpServer` REST endpoint retrieves the NTP server used for time synchronization.

This endpoint returns:

- `server` — hostname or IP of the primary NTP server

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_ntpServer` |
| Pattern Name | NTP Server Query |
| REST Endpoint | `GET /cloud/ntpServer` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the configured NTP server |

## 3. When to Use This Endpoint

Use `GET /cloud/ntpServer` to:

- Read `server` after `PUT /cloud/ntpServer`
