## 1. Description

The `PUT /cloud/certificates` REST endpoint installs or updates a certificate on the reader by downloading a PFX file from a URL.

This endpoint allows you to configure:

- The certificate name assigned on the reader through `name`
- The certificate type through `type`
- The download source URL through `url`
- The authentication method for the download server through `authenticationType`
- The PFX file password through `pfxPassword`

Use this endpoint to:

- Install a new TLS client or server certificate for MQTT or HTTPS endpoints
- Rotate an existing certificate before expiry
- Provision application certificates as part of initial reader setup

## 2. Endpoint Details

| Property | Value |
|---|---|
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
| Download credentials | Required only when `authenticationType` is `BASIC`. Provide `options.username` and `options.password`. |
| PFX password | The password protecting the PFX file (`pfxPassword`). Required if the PFX was exported with password protection. |
