## 1. Description

> **FXR60 Premium only.** The stack LED is not on other FXR60 variants. The FXR90 has no stack light.

The `GET /cloud/stack-led` REST endpoint retrieves the current stack LED state.

## 2. Status values

The response always includes `status`. Additional fields appear only when the LED is under an active override.

| `status` | Meaning | When returned | Response body |
|---|---|---|---|
| `DEFAULT` | The stack LED reflects the reader's normal operating state (reader-controlled). No custom color, flash, or timer is active. | No prior `PUT /cloud/stack-led` override is in effect, or a timed override has expired and the LED returned to reader control. | `{ "status": "DEFAULT" }` only |
| `NON_DEFAULT` | An active custom LED pattern is in effect from a prior `PUT /cloud/stack-led`. | A `PUT /cloud/stack-led` set an explicit color, flash, brightness, and/or duration that is still active. | `status`, `color`, `brightness`, `flash`, `seconds`, and `seconds_remaining` |

When `status` is `NON_DEFAULT`:

- `color`, `brightness`, and `flash` describe the active override
- `seconds` is the configured duration (`0` means until the next `PUT /cloud/stack-led`)
- `seconds_remaining` counts down on timed overrides

## 3. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_stackled` |
| Pattern Name | Stack LED Query |
| REST Endpoint | `GET /cloud/stack-led` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 Premium |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve stack LED state |

## 4. When to Use This Endpoint

Use `GET /cloud/stack-led` to:

- Check whether the LED is `DEFAULT` or `NON_DEFAULT`
- Read color, brightness, and flash on an active override
- Check `seconds_remaining` on a timed override
- Confirm a prior `PUT /cloud/stack-led` call
