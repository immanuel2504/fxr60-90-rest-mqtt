## 1. Description

The `DELETE /cloud/certificates/{certname}` REST endpoint removes an installed certificate.

This endpoint requires:

- `{certname}` — certificate `name` in the URL
- `type` — `client` or `app` in the JSON body

`server` cannot be deleted.

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
| Path Parameter | `certname` |
| Required Request Fields | `type` |

## 3. Before You Begin

Confirm the certificate name and type. Use the JSON field name below.

| Field | What to set |
|---|---|
| `certname` | Certificate `name` in the URL path. |
| `type` | `client` or `app`. Send in the JSON body. |
