## 1. Description

The `DELETE /cloud/caCertificates/{caname}` REST endpoint removes an installed CA (Certificate Authority) root certificate from the reader. When you call this endpoint, the CA certificate identified by the `{caname}` path parameter is permanently deleted from the reader's CA certificate store.

Use this endpoint to:

- Remove a CA certificate that is no longer trusted or has been compromised
- Clean up the CA store before installing a replacement with `PUT /cloud/caCertificates/{caname}`
- Rotate PKI trust anchors on the reader as part of a certificate lifecycle policy

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | CA Certificate Deletion |
| REST Endpoint | `DELETE /cloud/caCertificates/{caname}` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Path Parameter | `caname` (the CA certificate name to delete) |
| Supported Operations | Delete an installed CA certificate |

## 3. Before You Begin

Confirm the CA certificate is safe to remove before sending this request. Deleting a CA that is actively used for TLS verification will cause all TLS connections that depend on it to fail.

| What You Need | Details |
|---|---|
| CA certificate name | The exact name of the CA certificate to delete, supplied as the `{caname}` path parameter, as returned by `GET /cloud/caCertificates`. The name is case-sensitive. |
| Active use check | Identify all MQTT or HTTPS endpoints whose server or client certificates are issued by this CA. Remove those dependencies or install a replacement CA before deleting. |
| Irreversible action | Deletion is permanent. If the CA is still needed, reinstall it with `PUT /cloud/caCertificates/{caname}` and its original PEM content. |
