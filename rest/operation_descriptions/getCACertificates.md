## 1. Description

The `GET /cloud/caCertificates` REST endpoint retrieves the CA certificates installed on the reader.

This endpoint returns an array of installed CA certificate names.

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

- List CA names currently installed on the reader
- Verify a `PUT /cloud/caCertificates` request succeeded
