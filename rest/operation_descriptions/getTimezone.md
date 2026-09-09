## 1. Description

The `GET /cloud/timeZone` REST endpoint retrieves the active time zone.

This endpoint returns:

- `timeZone` — the zone currently in effect

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_timeZone` |
| Pattern Name | Time Zone Query |
| REST Endpoint | `GET /cloud/timeZone` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the active time zone |

## 3. When to Use This Endpoint

Use `GET /cloud/timeZone` to:

- Read `timeZone` after `PUT /cloud/timeZone`
