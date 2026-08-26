## 1. Description

The `GET /cloud/supportedRegionList` REST endpoint retrieves the list of RF regions this reader is permitted to operate in.

This endpoint returns:

- The set of supported country or region names that can be applied via `PUT /cloud/region`

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_SupportedRegionList` |
| Pattern Name | Supported Region Query |
| REST Endpoint | `GET /cloud/supportedRegionList` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the list of permitted RF regions for this reader |

## 3. When to Use This Endpoint

Use `GET /cloud/supportedRegionList` to:

- Determine valid values before calling `PUT /cloud/region`
- Confirm that the target deployment region is supported by this hardware
- Build a region picker in a provisioning or configuration UI
- Audit region support across different reader hardware variants in the same fleet

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| Region list | Is the target deployment region present? | Attempting to set an unsupported region via `PUT /cloud/region` will result in an error. |
