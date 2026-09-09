## 1. Description

The `PUT /cloud/apps/{appname}/pass-through` REST endpoint sends a request to a running user application.

This endpoint requires:

- `{appname}` — installed name in the URL
- `userapp` — same installed name in the JSON body

Optional:

- `command` — object the application accepts

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_reqToUserapp` |
| Pattern Name | User Application Request |
| REST Endpoint | `PUT /cloud/apps/{appname}/pass-through` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Path Parameter | `appname` |
| Required Request Fields | `userapp` |

## 3. Before You Begin

Confirm the application is running. Use the JSON field names below.

| Field | What to set |
|---|---|
| `appname` | Installed name from `GET /cloud/apps`. URL path. |
| `userapp` | Same installed name. |
| `command` | Optional. Object the application accepts, for example `command.message`. |
