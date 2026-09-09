## 1. Description

The `GET /cloud/certificates` REST endpoint retrieves the certificates installed on the reader.

This endpoint returns an array. Each item has:

- `name`
- `type` — `server`, `client`, or `app`
- `serial`
- `validityStart`, `validityEnd`
- `installTime`
- `issuerName`, `subjectName`
- `publickey`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_certificates` |
| Pattern Name | Certificate Inventory Query |
| REST Endpoint | `GET /cloud/certificates` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve installed certificates |

## 3. When to Use This Endpoint

Use `GET /cloud/certificates` to:

- Read installed certificates after `PUT /cloud/certificates` or `DELETE /cloud/certificates/{certname}`
