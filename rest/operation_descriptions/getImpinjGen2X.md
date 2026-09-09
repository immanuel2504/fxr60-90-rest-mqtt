## 1. Description

The `GET /cloud/impinjGen2X` REST endpoint retrieves the Impinj Gen2X configuration currently saved on the reader.

This endpoint returns the **last saved** Gen2X feature — exactly one of FastID, TagFocus, TagProtect, or TagQuieting — and that feature's fields.

PUT is wholesale, not a merge. A later PUT replaces the stored object. GET never returns two features at once, and it is not a full picture of radio Gen2X state. Use `GET /cloud/status` `impinjGen2X.isActive` to see whether a saved config is running on the current inventory session.

On a reader that has **never** had Gen2X configured, GET returns HTTP 200 with an empty body (not JSON `{}`). After any successful PUT, GET returns a JSON object. That saved config is sticky: `PUT /cloud/impinjGen2X` with `{}` is rejected (422). There is no documented way back to the empty body.

No request body is required.

Live-tested 8 September 2026 on FXR60 and FXR90, reader application 5.0.7: after a FastID PUT, both readers returned `{"fastID":{"enabled":false}}`.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_impinjGen2X` |
| Pattern Name | Impinj Gen2X Configuration Query |
| REST Endpoint | `GET /cloud/impinjGen2X` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve last saved Impinj Gen2X feature |

## 3. When to Use This Endpoint

Use `GET /cloud/impinjGen2X` to:

- See which one feature was last saved, and its fields (including `enabled`)
- Confirm the effect of a prior `PUT /cloud/impinjGen2X` call
- Review that saved object before applying it with `PUT /cloud/start` and `applyImpinjGen2X: true`

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `fastID` | Was FastID the last PUT? Is `enabled` true or false? | FastID embeds the TID in the singulation response. GET shows only this object if it was the last PUT. |
| `tagFocus` | Was TagFocus the last PUT? | TagFocus reduces re-reading of already-singulated tags. A later FastID PUT removes this object from GET. |
| `tagQuieting` | Was TagQuieting the last PUT? | TagQuieting suppresses listed or masked tags. GET shows only the last saved quieting object. |
| `tagProtect` | Was TagProtect the last PUT? | TagProtect applies Impinj tag locking. GET shows only this object if it was the last PUT. |
