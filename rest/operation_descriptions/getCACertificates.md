## 1. Description

The `GET /cloud/caCertificates` REST endpoint retrieves the list of CA (Certificate Authority) certificates installed on the reader.

This endpoint returns:

- An array of installed CA certificate names

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | CA Certificate Inventory Query |
| REST Endpoint | `GET /cloud/caCertificates` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the list of installed CA certificate names |

## 3. When to Use This Endpoint

Use `GET /cloud/caCertificates` to:

- Confirm which CA certificates are installed before configuring a TLS endpoint that must trust them
- Audit the reader's CA trust store across a fleet of readers
- Verify a CA certificate was installed after `PUT /cloud/caCertificates/{caname}`, or removed after `DELETE /cloud/caCertificates/{caname}`
- Reconcile the reader's trust anchors against your organization's PKI

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| CA certificate name | Is the expected CA certificate name present in the returned array? | Confirms the reader trusts the CA that issued your broker or endpoint TLS certificates. |
