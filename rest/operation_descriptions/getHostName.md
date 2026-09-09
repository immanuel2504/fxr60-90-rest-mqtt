## 1. Description

The `GET /cloud/hostName` REST endpoint retrieves the reader's network hostname.

This endpoint returns:

- `hostName` — the hostname currently assigned to the reader

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_hostName` |
| Pattern Name | Hostname Query |
| REST Endpoint | `GET /cloud/hostName` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the configured reader hostname |
| Response field | `hostName` |

## 3. When to Use This Endpoint

Use `GET /cloud/hostName` to:

- Read the hostname before changing it with `PUT /cloud/hostName`
- Confirm the hostname after a prior `PUT /cloud/hostName` call
