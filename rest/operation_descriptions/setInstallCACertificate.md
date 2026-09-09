## 1. Description

The `PUT /cloud/caCertificates` REST endpoint installs a CA certificate.

This endpoint requires:

- `name` — name stored on the reader
- `content` — PEM, including `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_InstallCACertificate` |
| Pattern Name | CA Certificate Installation |
| REST Endpoint | `PUT /cloud/caCertificates` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `name`, `content` |

## 3. Before You Begin

Decide the CA name and PEM. Use the JSON field names below.

| Field | What to set |
|---|---|
| `name` | Name to store. GET later lists this name with `.crt` appended. |
| `content` | Full PEM CA certificate. |
