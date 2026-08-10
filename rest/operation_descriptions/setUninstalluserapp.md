## 1. Description

The `PUT /cloud/apps/{appname}/uninstall` REST endpoint removes a user application from the reader. The application is identified by the `{appname}` path parameter.

Use this endpoint to:

- Remove a decommissioned user application
- Free storage before installing a replacement
- Clean up test or development packages

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | User Application Removal |
| REST Endpoint | `PUT /cloud/apps/{appname}/uninstall` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Path Parameter | `appname` (the application to uninstall) |
| Request Body | None (the app name is supplied as the `{appname}` path parameter) |

## 3. Before You Begin

Stop the app with `PUT /cloud/apps/{appname}/stop` before uninstalling if it is currently running.

| What You Need | Details |
|---|---|
| Application name | The exact `appname` from `GET /cloud/apps`, supplied as the `{appname}` path parameter. |
