## 1. Description

The `PUT /cloud/apps/{appname}/pass-through` REST endpoint sends a custom request or data payload to a user application running on the reader. The application is identified by the `{appname}` path parameter.

This endpoint allows you to configure:

- The command or data payload to deliver through `command`

Use this endpoint to:

- Invoke custom logic in an installed user application
- Pass structured data or control commands to the application layer
- Integrate third-party processing running directly on the reader

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | User Application Request |
| REST Endpoint | `PUT /cloud/apps/{appname}/pass-through` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Path Parameter | `appname` (the target application) |
| Required Request Fields | `command` |

## 3. Before You Begin

Confirm the target user application is installed and running before sending this request. A request to a stopped or missing application will fail.

| What You Need | Details |
|---|---|
| Application name | The exact `appname`, supplied as the `{appname}` path parameter, as returned by `GET /cloud/apps`. |
| Command or data | The `command` object to pass to the user application (for example, `command.message`). The expected structure is defined by the user application, not by the reader API. |
| Application state | Use `GET /cloud/apps` to confirm the target application is running (`runningStatus: true`) before sending. A stopped application may not be able to process the request. |
