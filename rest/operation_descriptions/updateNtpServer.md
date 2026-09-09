## 1. Description

The `PUT /cloud/ntpServer` REST endpoint sets the NTP server used for time synchronization.

This endpoint requires one primary:

- `server` — hostname or IP
- or `server1` — same meaning (legacy key)

Optional:

- `server2` — backup hostname or IP

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_ntpServer` |
| Pattern Name | NTP Server Configuration |
| REST Endpoint | `PUT /cloud/ntpServer` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `server` or `server1` |

## 3. Before You Begin

Decide the NTP host to send. Use the JSON field names below.

| Field | What to set |
|---|---|
| `server` | Primary NTP hostname or IP. |
| `server1` | Same as `server` (legacy key). Send `server` or `server1`, not both. |
| `server2` | Optional backup hostname or IP. |
