## 1. Description

The `GET /cloud/readPoints` REST endpoint retrieves the read points on the reader.

This endpoint returns:

- an array of read-point identifiers, for example `"1"` through `"6"`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_readPoints` |
| Pattern Name | Read Point Query |
| REST Endpoint | `GET /cloud/readPoints` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve read-point identifiers |

## 3. When to Use This Endpoint

Use `GET /cloud/readPoints` to:

- Read the identifiers
