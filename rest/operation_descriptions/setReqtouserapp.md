## 1. Description

The `PUT /cloud/apps/{appname}/pass-through` REST endpoint sends a request to a running user application.

This endpoint requires:

- `{appname}` — installed name in the URL

Optional:

- `command` — object the application accepts
- `userapp` — same installed name in the JSON body. Not required for local REST; the `{appname}` path parameter identifies the application. The MQTT API requires it, because it has no path parameter.

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
| Required Request Fields | None |

## 3. Before You Begin

Confirm the application is running. Use the JSON field names below.

| Field | What to set |
|---|---|
| `appname` | Installed name from `GET /cloud/apps`. URL path. |
| `userapp` | Optional for local REST. Same installed name. Required by the MQTT API. |
| `command` | Optional. Object the application accepts, for example `command.message`. |
