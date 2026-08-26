## 1. Description

The `PUT /cloud/apps/install` REST endpoint installs a user application (`.deb` package) on the reader by downloading it from a file server.

This endpoint allows you to configure:

- The download source URL through `url`
- The package filename through `filename`
- The authentication method for the download server through `authenticationType`
- BASIC credentials through `options`
- Optional HTTPS download retry through `retry` and timeouts through `timeouts`
- Optional download `headers.Authorization` (Bearer JWT)

Use this endpoint to:

- Deploy custom on-reader applications
- Update user-app packages from a central repository
- Extend reader functionality with Zebra-approved `.deb` packages

**Synchronous vs asynchronous**

- Omit `retry` — download and install finish during this call. The HTTP 200 body is the final result. HTTPS, FTPS, and SFTP.
- Include `retry` with an `https://` URL — the reader acknowledges immediately and finishes in the background. The final success or failure is published on the management events channel. `retry.type` must be `randomWait`. Wait is a random duration between `retry.policy.wait.min` and `retry.policy.wait.max`.
- Do not send `retry` or `timeouts` for `ftps://` or `sftp://`. Those protocols are synchronous only.

`retry` and `timeouts` are HTTPS only.

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
| Supported Authentication Types | `NONE`, `BASIC` |

## 3. Before You Begin

Gather download server details before sending this request. The reader must be able to reach the URL from its network.

| What You Need | Details |
|---|---|
| File server URL | The base URL hosting the `.deb` package (HTTPS, FTPS, or SFTP), supplied through `url`. |
| Filename | The exact `.deb` filename on the server, supplied through `filename`. |
| Authentication type | `NONE` if the download server requires no credentials, or `BASIC` for username/password (`options.username`, `options.password`). |
| HTTPS retry | Optional. `retry.type` is `randomWait`. `retry.policy.retries` is 1–50. Wait seconds: `min` 0–3600, `max` 1–3600. Sending `retry` makes the install asynchronous. |
| HTTPS timeouts | Optional. `timeouts.connection` and `timeouts.read` in seconds (1–3600). |
| Download header | Optional. `headers.Authorization` for a Bearer JWT on the file-server request. |
| TLS verification | Optional `verifyPeer` and `verifyHost` flags, plus an optional CA certificate path or inline content for HTTPS servers. |
