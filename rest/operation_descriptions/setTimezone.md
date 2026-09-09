## 1. Description

The `PUT /cloud/timeZone` REST endpoint sets the time zone.

This endpoint requires:

- `timeZone` — a reader-supported name, for example `UTC` or `Kolkata`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_timeZone` |
| Pattern Name | Time Zone Configuration |
| REST Endpoint | `PUT /cloud/timeZone` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `timeZone` |

## 3. Before You Begin

Decide the zone to send. Use the JSON field name below.

| Field | What to set |
|---|---|
| `timeZone` | A supported name, for example `UTC` or `Kolkata`. Matching is case-sensitive. |
