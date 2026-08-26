## 1. Description

The `PUT /cloud/apps/{appname}/autostart` REST endpoint configures whether a user application starts automatically when the reader boots. The application is identified by the `{appname}` path parameter.

This endpoint allows you to configure:

- Whether the application starts automatically on boot through `autostart`

Use this endpoint to:

- Enable autostart for production user apps
- Disable autostart for test or manual-only apps
- Standardize boot behavior across a fleet

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
| Path Parameter | `appname` (the application to configure) |
| Required Request Fields | `autostart` |

## 3. Before You Begin

Decide the desired boot behavior before sending this request.

| What You Need | Details |
|---|---|
| Application name | The exact `appname`, supplied as the `{appname}` path parameter, as returned by `GET /cloud/apps`. |
| Autostart flag | `autostart` (boolean): `true` to start the app automatically on boot, or `false` to disable autostart. |
