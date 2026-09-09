## 1. Description

The `PUT /cloud/revertbackOS` REST endpoint reverts the reader to the previous OS.

Send `{}`.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_revertbackOS` |
| Pattern Name | Firmware Rollback |
| REST Endpoint | `PUT /cloud/revertbackOS` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |

## 3. When to Use This Endpoint

Use `PUT /cloud/revertbackOS` to:

- Revert after `PUT /cloud/os`
