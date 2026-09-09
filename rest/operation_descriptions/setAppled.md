## 1. Description

The `PUT /cloud/app-led` REST endpoint sets the application LED color, flash, and duration.

This endpoint requires:

- `color` — `red`, `amber`, `green`, or `off`
- `flash` — `true` to blink, `false` for solid
- `seconds` — how long to keep this state. `0` means until the next `PUT /cloud/app-led`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_appled` |
| Pattern Name | Application LED Control |
| REST Endpoint | `PUT /cloud/app-led` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Supported Colors | `red`, `amber`, `green`, `off` |
| Required Request Fields | `color`, `flash`, `seconds` |

## 3. Before You Begin

| What You Need | Details |
|---|---|
| Color | `red`, `amber`, `green`, or `off`. |
| Flash | `true` blinks. `false` is solid. |
| Duration | Seconds to keep this state. Use `0` until the next `PUT /cloud/app-led`. |
