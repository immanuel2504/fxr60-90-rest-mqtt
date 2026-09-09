## 1. Description

The `PUT /cloud/apps/install` REST endpoint installs a user application from a download URL.

This endpoint requires:

- `url` — URL of the `.deb` package
- `filename` — `.deb` filename on the server
- `authenticationType` — `NONE` or `BASIC`

When `authenticationType` is `BASIC`, also send `options` — `username` and `password`.

Optional:

- `verifyPeer`, `verifyHost`
- `headers` — for example `Authorization`
- `retry` — `count` and `delayInSec`
- `installedCertificateName`, `installedCertificateType`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_installUserapp` |
| Pattern Name | User Application Installation |
| REST Endpoint | `PUT /cloud/apps/install` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `url`, `filename`, `authenticationType` |

## 3. Before You Begin

Decide the download URL and authentication. Use the JSON field names below.

| Field | What to set |
|---|---|
| `url` | URL of the `.deb` package. |
| `filename` | `.deb` filename on the server. |
| `authenticationType` | `NONE` or `BASIC`. |
| `options` | `username` and `password` when `authenticationType` is `BASIC`. |
| `verifyPeer` | Optional. `true` to check the file server certificate. |
| `verifyHost` | Optional. `true` to check the file server hostname. |
| `headers` | Optional. Extra download headers, for example `Authorization`. |
| `retry` | Optional. `count` and `delayInSec`. |
| `installedCertificateName` | Optional. Installed certificate name for the download. |
| `installedCertificateType` | Optional. Installed certificate type for the download. |
