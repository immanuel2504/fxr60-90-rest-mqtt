## 1. Description

The `GET /cloud/impinjGen2X` REST endpoint retrieves the Impinj Gen2X configuration currently saved on the reader.

This endpoint returns the **last saved** Gen2X feature — one of FastID, TagFocus, TagProtect, or TagQuieting — and that feature's fields.

The reader stores only one feature at a time. The response is not a list of all four. If no Gen2X configuration has been saved, the payload is an empty object.

No request body is required. Use this GET to see `enabled` on FastID or TagFocus. `GET /cloud/status` `impinjGen2X.isActive` only means a Gen2X config is running, not that the feature is switched on.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_impinjGen2X` |
| Pattern Name | Impinj Gen2X Configuration Query |
| REST Endpoint | `GET /cloud/impinjGen2X` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve saved Impinj Gen2X configuration |

## 3. When to Use This Endpoint

Use `GET /cloud/impinjGen2X` to:

- See which one feature was last saved, and its fields (including `enabled`)
- Review Gen2X settings before applying them with `PUT /cloud/start` and `applyImpinjGen2X: true`
- Confirm the effect of a prior `PUT /cloud/impinjGen2X` call

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `fastID` | Is FastID enabled? | FastID embeds the TID in the singulation response, enabling faster tag identification without a separate read. |
| `tagFocus` | Is TagFocus configured? | TagFocus reduces re-reading of already-singulated tags in dense tag populations. |
| `tagQuieting` | Is TagQuieting set? | TagQuieting suppresses repeated reads of the same tag EPC within a session. |
| `tagProtect` | Is TagProtect active? | TagProtect applies Impinj proprietary tag locking features for secure deployments. |
