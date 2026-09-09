## 1. Description

> **FXR60 Premium only.** The stack LED is not on other FXR60 variants. The FXR90 has no stack light.

The `GET /cloud/stack-led` REST endpoint retrieves the current stack LED state.

This endpoint returns:

- `status` — `DEFAULT` or `NON_DEFAULT`
- `color`, `brightness`, `flash`, `seconds`, and `seconds_remaining` when the LED is `NON_DEFAULT`

When `status` is `DEFAULT`, the body is `{ "status": "DEFAULT" }`.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_stackled` |
| Pattern Name | Stack LED Query |
| REST Endpoint | `GET /cloud/stack-led` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 Premium |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve stack LED state |

## 3. When to Use This Endpoint

Use `GET /cloud/stack-led` to:

- Read `status`, color, brightness, and flash
- Check `seconds_remaining` on a timed override
- Confirm a prior `PUT /cloud/stack-led` call
