## 1. Description

The `PUT /cloud/apps/{appname}/autostart` REST endpoint sets whether a user application starts when the reader boots.

This endpoint requires:

- `{appname}` — installed name in the URL
- `autostart` — `true` or `false`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_autostartUserapp` |
| Pattern Name | User Application Autostart Configuration |
| REST Endpoint | `PUT /cloud/apps/{appname}/autostart` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Path Parameter | `appname` |
| Required Request Fields | `autostart` |

## 3. Before You Begin

Decide the boot behavior. Use the JSON field names below.

| Field | What to set |
|---|---|
| `appname` | Installed name from `GET /cloud/apps`. URL path. |
| `autostart` | `true` to start on boot, or `false` to not. |
