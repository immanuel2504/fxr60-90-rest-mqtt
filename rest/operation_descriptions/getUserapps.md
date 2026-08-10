## 1. Description

The `GET /cloud/apps` REST endpoint retrieves the list of user applications installed on the reader.

This endpoint returns:

- An array of installed user apps, each with `appname`, `autostart`, `runningStatus`, and `metadata`

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | User Application Inventory Query |
| REST Endpoint | `GET /cloud/apps` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the list of installed user applications |

## 3. When to Use This Endpoint

Use `GET /cloud/apps` to:

- Confirm which user apps are installed before issuing start, stop, or uninstall requests
- Check whether a user app is currently running
- Verify autostart configuration per installed app
- Audit deployed applications across a fleet of readers

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `appname` | Is the expected app present? | Confirms successful installation before attempting to start or configure the app. |
| `runningStatus` | Is the app currently running? | Required before sending a stop request; also confirms a successful start. |
| `autostart` | Is autostart enabled? | Determines whether the app will resume automatically after a reboot. |
