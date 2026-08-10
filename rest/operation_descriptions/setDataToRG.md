## 1. Description

The `PUT /cloud/setdataToRG` REST endpoint triggers the reader gateway to process and deliver any buffered tag data.

This is a **trigger-only** call — you do not upload tag data in the request. The reader flushes data that is already buffered on the device. No request body is required.

Use this endpoint to:

- Manually trigger reader gateway data delivery when automatic forwarding is not active
- Flush buffered tag events through the reader gateway pipeline

## 2. Before You Begin

Confirm that the reader gateway is configured and active before calling this endpoint. If no data is buffered or the gateway is not configured, the call may succeed but have no effect.

| What You Need | Details |
|---|---|
| Reader gateway | Valid endpoint settings (see `GET /cloud/config`) |
| Buffered data | Tag events waiting for delivery |

## 3. Endpoint Details

| Property | Value |
|---|---|
| REST Endpoint | `PUT /cloud/setdataToRG` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Request body | None |
