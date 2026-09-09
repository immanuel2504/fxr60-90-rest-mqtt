## 1. Description

The `PUT /cloud/certificates/{certname}` REST endpoint refreshes an installed certificate.

This endpoint requires:

- `{certname}` — certificate `name` in the URL
- `type` — `server`, `client`, or `app` in the JSON body

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_refreshCertificate` |
| Pattern Name | Certificate Refresh |
| REST Endpoint | `PUT /cloud/certificates/{certname}` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Path Parameter | `certname` |
| Required Request Fields | `type` |

## 3. Before You Begin

Confirm the certificate is already installed. Use the JSON field name below.

| Field | What to set |
|---|---|
| `certname` | Certificate `name` in the URL path. |
| `type` | `server`, `client`, or `app`. Send in the JSON body. |
