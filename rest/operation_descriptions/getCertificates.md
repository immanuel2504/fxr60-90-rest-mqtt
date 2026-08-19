## 1. Description

The `GET /cloud/certificates` REST endpoint retrieves the list of certificates installed on the reader.

This endpoint returns:

- An array of installed certificates, each with name, type, serial number, and validity dates

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Certificate Inventory Query |
| REST Endpoint | `GET /cloud/certificates` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the list of installed certificates |

## 3. When to Use This Endpoint

Use `GET /cloud/certificates` to:

- Audit which certificates are installed and their current validity windows
- Confirm a certificate was successfully installed or removed
- Retrieve serial numbers for certificate rotation audits
- Check expiry dates before a scheduled certificate renewal

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `name` | Is the expected certificate present? | Confirms the correct certificate is installed for TLS or authentication. |
| `type` | What type of certificate is it (`server`, `client`, or `app`)? | Differentiates server, client, and app certificates used for different purposes. |
| `validityEnd` | When does it expire? | Expired certificates will cause TLS handshake failures and connectivity loss. |
| `serial` | Does the serial match the expected certificate? | Verifies the exact certificate instance, useful for rotation audits. |
