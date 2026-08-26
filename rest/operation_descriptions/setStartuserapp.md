## 1. Description

The `PUT /cloud/apps/{appname}/start` REST endpoint starts a user application installed on the reader. The application is identified by the `{appname}` path parameter.

Use this endpoint to:

- Launch an installed user app on demand
- Restart an app after configuration changes
- Bring application logic online after installing it with `PUT /cloud/apps/install`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_startUserapp` |
| Pattern Name | User Application Control — Start |
| REST Endpoint | `PUT /cloud/apps/{appname}/start` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Path Parameter | `appname` (the installed application to start) |
| Request Body | None (the app name is supplied as the `{appname}` path parameter) |

## 3. Before You Begin

Confirm the application is installed before starting it. Use `GET /cloud/apps` to verify the exact `appname` and its current running status.

| What You Need | Details |
|---|---|
| Application name | The exact name of the installed application, supplied as the `{appname}` path parameter, as returned by `GET /cloud/apps`. |
| Installation check | The application must already be installed via `PUT /cloud/apps/install` before it can be started. |
