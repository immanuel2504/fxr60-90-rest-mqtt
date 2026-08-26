## 1. Description

The `DELETE /cloud/certificates/{certname}` REST endpoint removes an installed certificate from the reader. When you call this endpoint, the certificate identified by the `{certname}` path parameter and its `type` is deleted from the reader's certificate store.

> **The server certificate cannot be deleted through this API.** Only `client` and `app` certificates can be removed — the `type` parameter accepts `client` or `app` only. The reader's server certificate is required for TLS and has no delete operation.

Use this endpoint to:

- Remove expired or revoked client TLS certificates before installing a replacement
- Clean up the certificate store after a certificate rotation
- Delete client or app certificates that are no longer needed for MQTT or HTTPS authentication

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `del_certificate` |
| Pattern Name | Certificate Deletion |
| REST Endpoint | `DELETE /cloud/certificates/{certname}` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Path Parameter | `certname` (the certificate name to delete) |
| Required Request Fields | `type` in the JSON request body |
| Supported Certificate Types | `client`, `app` (the `server` certificate cannot be deleted) |

Send:

```http
DELETE /cloud/certificates/{certname}
Content-Type: application/json

{ "type": "client" }
```

Do not put `type` in the URL query string.

## 3. Before You Begin

Confirm the certificate is no longer in use before sending this request. Cross-reference the certificate name and type with your active endpoint configuration and the list returned by `GET /cloud/certificates`.

| What You Need | Details |
|---|---|
| Certificate name | The exact name of the certificate to delete, supplied as the `{certname}` path parameter, as returned by `GET /cloud/certificates`. The name is case-sensitive. |
| Certificate type | The `type` of the certificate: `client` or `app`, sent in the request body. The type must match the installed certificate. The `server` certificate cannot be deleted. |
| Active use check | Confirm the certificate is not currently used for an active MQTT TLS or HTTPS endpoint connection. Deleting an in-use certificate will cause TLS handshake failures on the next reconnect. |
