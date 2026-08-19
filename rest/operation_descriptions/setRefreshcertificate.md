## 1. Description

The `PUT /cloud/certificates/{certname}` REST endpoint refreshes an already-installed certificate on the reader by re-fetching or re-applying it from its configured source.

Use this endpoint to:

- Renew a certificate before expiry without a full reinstall
- Re-apply a certificate after upstream CA rotation
- Trigger certificate refresh as part of a credential rotation workflow

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Certificate Refresh |
| REST Endpoint | `PUT /cloud/certificates/{certname}` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Path Parameter | `certname` (the installed certificate name to refresh) |
| Required Request Fields | `type` |
| Supported Certificate Types | `client`, `server`, `app` |

## 3. Before You Begin

The certificate must already be installed. Use `GET /cloud/certificates` to confirm the certificate name and `type`.

| What You Need | Details |
|---|---|
| Certificate name | The exact name of the installed certificate, supplied as the `{certname}` path parameter. |
| Certificate type | The `type` of the certificate: `client`, `server`, or `app`, sent in the request body. |
