## 1. Description

The `PUT /cloud/apps/install` REST endpoint installs a user application (`.deb` package) on the reader by downloading it from a file server.

This endpoint allows you to configure:

- The download source URL through `url`
- The package filename through `filename`
- The authentication method for the download server through `authenticationType`

Use this endpoint to:

- Deploy custom on-reader applications
- Update user-app packages from a central repository
- Extend reader functionality with Zebra-approved `.deb` packages

## 2. Endpoint Details

| Property | Value |
|---|---|
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
| File server URL | The base URL hosting the `.deb` package (for example, HTTP, HTTPS, or SFTP), supplied through `url`. |
| Filename | The exact `.deb` filename on the server, supplied through `filename`. |
| Authentication type | `NONE` if the download server requires no credentials, or `BASIC` for username/password authentication (`options.username`, `options.password`). |
| TLS verification | Optional `verifyPeer` and `verifyHost` flags, plus an optional CA certificate path or inline content for HTTPS servers. |
