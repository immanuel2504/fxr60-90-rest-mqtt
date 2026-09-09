## 1. Description

The `PUT /cloud/certificates` REST endpoint installs a certificate from a download URL.

This endpoint requires:

- `name` — name stored on the reader
- `type` — `server`, `client`, or `app`
- `url` — `https://`, `ftps://`, or `sftp://` to a PFX file

Also send:

- `authenticationType` — `BASIC`
- `authenticationOptions` — `username` and `password`. If `authenticationOptions` is not accepted, send `options`.
- `pfxPassword` — PFX password, at least 15 characters

Optional:

- `verifyPeer`, `verifyHost`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_updateCertificate` |
| Pattern Name | Certificate Installation |
| REST Endpoint | `PUT /cloud/certificates` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `name`, `type`, `url` |

## 3. Before You Begin

Decide the name, type, and download source. Use the JSON field names below.

| Field | What to set |
|---|---|
| `name` | Name stored on the reader. |
| `type` | `server`, `client`, or `app`. |
| `url` | `https://`, `ftps://`, or `sftp://` URL of the PFX file. |
| `authenticationType` | `BASIC`. |
| `authenticationOptions` | `username` and `password` for the file server. If `authenticationOptions` is not accepted, send `options`. |
| `pfxPassword` | PFX password. Must be at least 15 characters. |
| `verifyPeer` | Optional. `true` to check the file server certificate. |
| `verifyHost` | Optional. `true` to check the file server hostname. |
