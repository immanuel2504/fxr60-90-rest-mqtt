## 1. Description

The `PUT /cloud/eSimConfig` REST endpoint updates an eSIM profile.

This endpoint requires:

- `operation` — `add`, `delete`, `enable`, or `disable`
- `profileNickName`

Also send `activationID` when `operation` is `add`. Omit it for `enable`, `disable`, and `delete`.

Supported on FXR90 only.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_eSimConfig` |
| Pattern Name | eSIM Configuration |
| REST Endpoint | `PUT /cloud/eSimConfig` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `operation`, `profileNickName` |

## 3. Before You Begin

Decide the operation and profile. Use the JSON field names below.

| Field | What to set |
|---|---|
| `operation` | `add`, `delete`, `enable`, or `disable`. |
| `profileNickName` | Profile nickname from `GET /cloud/eSimConfig`. |
| `activationID` | Required for `add`. Omit for `enable`, `disable`, and `delete`. |
