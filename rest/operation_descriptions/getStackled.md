## 1. Description

> **Product applicability: FXR60 only — not applicable to the FXR90.** The stack LED (stack light) is an FXR60 feature; the FXR90 has no stack light. This endpoint and its schema are documented here because the stack-light definition is shared across the Zebra fixed-reader family. On an FXR90, use `GET /cloud/app-led` for the application LED instead.

The `GET /cloud/stack-led` REST endpoint retrieves the current state of the stack LED on the reader.

This endpoint returns status, color, brightness, flash state, configured duration, and remaining time.

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| REST Endpoint | `GET /cloud/stack-led` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | **FXR60** — the FXR90 has no stack light |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |

## 3. When to Use This Endpoint

Use `GET /cloud/stack-led` to:

- Confirm the current stack LED color, brightness, and flash state
- Verify the effect of a prior `PUT /cloud/stack-led` call
- Check how many seconds remain on a timed LED override
