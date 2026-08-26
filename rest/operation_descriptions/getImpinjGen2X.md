## 1. Description

The `GET /cloud/impinjGen2X` REST endpoint retrieves the Impinj Gen2X configuration currently saved on the reader.

This endpoint returns:

- Whether FastID, TagFocus, TagProtect, or TagQuieting is configured
- The parameters for each enabled Gen2X feature

No request body is required. If no Gen2X configuration has been saved, the response payload will be an empty object.

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

- Check whether FastID, TagProtect, TagFocus, or TagQuieting has been configured
- Review Gen2X settings before applying them with a `PUT /cloud/start` call
- Confirm the effect of a prior `PUT /cloud/impinjGen2X` call

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `fastID` | Is FastID enabled? | FastID embeds the TID in the singulation response, enabling faster tag identification without a separate read. |
| `tagFocus` | Is TagFocus configured? | TagFocus reduces re-reading of already-singulated tags in dense tag populations. |
| `tagQuieting` | Is TagQuieting set? | TagQuieting suppresses repeated reads of the same tag EPC within a session. |
| `tagProtect` | Is TagProtect active? | TagProtect applies Impinj proprietary tag locking features for secure deployments. |
