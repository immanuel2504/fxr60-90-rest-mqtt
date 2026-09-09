## 1. Description

The `DELETE /cloud/caCertificates` REST endpoint removes an installed CA certificate.

This endpoint requires:

- `name` — the name you sent at install, without `.crt`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `del_CACertificate` |
| Pattern Name | CA Certificate Deletion |
| REST Endpoint | `DELETE /cloud/caCertificates` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `name` |

## 3. Before You Begin

Use the JSON field name below.

| Field | What to set |
|---|---|
| `name` | Install name, without the `.crt` suffix that `GET /cloud/caCertificates` returns. |
