## 1. Description

The `PUT /cloud/apps/{appname}/start` REST endpoint starts an installed user application.

This endpoint requires:

- `{appname}` — installed name in the URL

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_startUserapp` |
| Pattern Name | User Application Control — Start |
| REST Endpoint | `PUT /cloud/apps/{appname}/start` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Path Parameter | `appname` |
| Request Body | None |

## 3. Before You Begin

Confirm the application is installed. Use the JSON field name below.

| Field | What to set |
|---|---|
| `appname` | Installed name from `GET /cloud/apps`. URL path. |
