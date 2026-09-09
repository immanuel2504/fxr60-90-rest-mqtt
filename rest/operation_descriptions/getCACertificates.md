## 1. Description

The `GET /cloud/caCertificates` REST endpoint retrieves the CA certificates installed on the reader.

This endpoint returns:

- an array of CA names

Listed names include a `.crt` suffix. Delete with the name you installed, without that suffix.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_CACertificates` |
| Pattern Name | CA Certificate Inventory Query |
| REST Endpoint | `GET /cloud/caCertificates` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve installed CA certificate names |

## 3. When to Use This Endpoint

Use `GET /cloud/caCertificates` to:

- Read CA names after `PUT /cloud/caCertificates` or `DELETE /cloud/caCertificates`
