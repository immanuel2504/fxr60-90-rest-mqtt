## 1. Description

The `PUT /cloud/certificates` REST endpoint installs or updates a certificate on the reader by downloading a PFX file from a URL.

This endpoint allows you to configure:

- The certificate name assigned on the reader through `name`
- The certificate type through `type`
- The download source URL through `url`
- The authentication method for the download server through `authenticationType`
- BASIC credentials through `authenticationOptions`
- The PFX file password through `pfxPassword`
- Optional HTTPS download retry through `retry` and timeouts through `timeouts`
- Optional download `headers.Authorization` (Bearer JWT)

Use this endpoint to:

- Install a new TLS client or server certificate for MQTT or HTTPS endpoints
- Rotate an existing certificate before expiry
- Provision application certificates as part of initial reader setup

**Synchronous vs asynchronous**

- Omit `retry` — download and install finish during this call. The HTTP 200 body is the final result. HTTPS, FTPS, and SFTP.
- Include `retry` with an `https://` URL — the reader acknowledges immediately and finishes in the background. The final success or failure is published on the management events channel. `retry.type` must be `randomWait`. Wait is a random duration between `retry.policy.wait.min` and `retry.policy.wait.max`.
- Do not send `retry` or `timeouts` for `ftps://` or `sftp://`. Those protocols are synchronous only.

`retry` and `timeouts` are HTTPS only.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_updateCertificate (set_update_cert)` |
| Pattern Name | Certificate Installation |
| REST Endpoint | `PUT /cloud/certificates` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `name`, `type`, `url` |
| Supported Certificate Types | `client`, `server`, `app` |
| Supported Transfer Protocols | `HTTPS`, `FTPS`, `SFTP` |
| Supported Authentication Types | `NONE`, `BASIC` |

## 3. Before You Begin

Gather all certificate source details before sending this request. An invalid URL, wrong certificate type, missing download credentials, or an incorrect PFX password will cause installation to fail.

| What You Need | Details |
|---|---|
| Certificate name | A unique name to assign to this certificate on the reader. If a certificate with this name already exists, it will be replaced. |
| Certificate type | `client` for mutual TLS authentication, `server` for CA/server trust, or `app` for application-specific certificates. |
| Source URL | An `HTTPS`, `FTPS`, or `SFTP` URL where the reader can download the PFX certificate file. The reader must have network connectivity to reach this URL. |
| Authentication type | `NONE` if the download server requires no credentials, or `BASIC` if username and password authentication is required. |
| Download credentials | Required only when `authenticationType` is `BASIC`. Provide `authenticationOptions.username` and `authenticationOptions.password`. |
| PFX password | The password protecting the PFX file (`pfxPassword`). Required if the PFX was exported with password protection. |
| HTTPS retry | Optional. `retry.type` is `randomWait`. `retry.policy.retries` is 1–50. Wait seconds: `min` 0–3600, `max` 1–3600. Sending `retry` makes the install asynchronous. |
| HTTPS timeouts | Optional. `timeouts.connection` and `timeouts.read` in seconds (1–3600). |
| Download header | Optional. `headers.Authorization` for a Bearer JWT on the file-server request. |
