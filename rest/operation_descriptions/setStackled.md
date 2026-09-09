## 1. Description

> **FXR60 Premium only.** The stack LED is not on other FXR60 variants. The FXR90 has no stack light.

The `PUT /cloud/stack-led` REST endpoint sets the stack LED color, flash, and duration.

This endpoint requires:

- `color` — `red`, `amber`, `green`, `blue`, or `off`
- `flash` — `true` to blink, `false` for solid
- `seconds` — how long to keep this state. `0` means until the next `PUT /cloud/stack-led`

`brightness` is optional: `low`, `med`, or `high`. If omitted, the reader uses `low`.

`blue` is valid on the stack LED. It is not valid on `PUT /cloud/app-led`.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_stackled` |
| Pattern Name | Stack LED Control |
| REST Endpoint | `PUT /cloud/stack-led` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 Premium |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Supported Colors | `red`, `amber`, `green`, `blue`, `off` |
| Supported Brightness | `low`, `med`, `high` (default `low`) |
| Required Request Fields | `color`, `flash`, `seconds` |

## 3. Before You Begin

| What You Need | Details |
|---|---|
| Color | `red`, `amber`, `green`, `blue`, or `off`. |
| Flash | `true` blinks. `false` is solid. |
| Duration | Seconds to keep this state. Use `0` until the next `PUT /cloud/stack-led`. |
| Brightness | Optional. `low`, `med`, or `high`. |
