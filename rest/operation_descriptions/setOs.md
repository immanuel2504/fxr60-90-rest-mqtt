## 1. Description

The `PUT /cloud/os` REST endpoint updates the reader OS from a download URL.

This endpoint requires:

- `url` — `https://`, `scp://`, `sftp://`, or `ftps://`
- `authenticationType` — `NONE` or `BASIC`

When `authenticationType` is `BASIC`, also send `authenticationOptions` — `username` and `password`. If `authenticationOptions` is not accepted, send `options`.

Optional:

- `verifyPeer`, `verifyHost`
- `retry`, `timeouts` — HTTPS only

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_os` |
| Pattern Name | OS Firmware Update |
| REST Endpoint | `PUT /cloud/os` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `url`, `authenticationType` |

## 3. Before You Begin

Decide the download URL and authentication. Use the JSON field names below.

| Field | What to set |
|---|---|
| `url` | `https://`, `scp://`, `sftp://`, or `ftps://` URL of the OS image. |
| `authenticationType` | `NONE` or `BASIC`. |
| `authenticationOptions` | `username` and `password` when `authenticationType` is `BASIC`. If `authenticationOptions` is not accepted, send `options`. |
| `verifyPeer` | Optional. `true` to check the file server certificate. |
| `verifyHost` | Optional. `true` to check the file server hostname. |
| `retry` | Optional. HTTPS only. `type` `randomWait` with `policy.retries` and `wait.min` / `wait.max`. |
| `timeouts` | Optional. HTTPS only. `connection` and `read` in seconds. |
