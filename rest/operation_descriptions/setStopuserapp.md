## 1. Description

The `PUT /cloud/apps/{appname}/stop` REST endpoint stops a running user application on the reader. The application is identified by the `{appname}` path parameter.

Use this endpoint to:

- Halt a user app before uninstalling or updating
- Free CPU/memory resources on the reader
- Pause application logic during maintenance

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_stopUserapp` |
| Pattern Name | User Application Control — Stop |
| REST Endpoint | `PUT /cloud/apps/{appname}/stop` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Path Parameter | `appname` (the running application to stop) |
| Request Body | None (the app name is supplied as the `{appname}` path parameter) |

## 3. Before You Begin

Confirm the application is running before stopping it. Use `GET /cloud/apps` to verify the exact `appname` and its current running status.

| What You Need | Details |
|---|---|
| Application name | The exact name of the running application, supplied as the `{appname}` path parameter, as returned by `GET /cloud/apps`. |
