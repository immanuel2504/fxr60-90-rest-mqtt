## 1. Description

> **Product applicability: FXR60 only.** Display APIs are not available on FXR90.

The `PUT /cloud/displayConfig` REST endpoint sets display configuration on the device.

This endpoint allows you to configure:

- `enable` — enable or disable the display
- `enableOnscreenKeyboard` — enable or disable the virtual touch on-screen keyboard
- `startUrl` — URL opened when the display is enabled
- `resolution` — configured display resolution (`WidthxHeight`)
- `screenTimeoutSec` — screen timeout in seconds (`0`–`3600`; `0` keeps the display always on)
- `orientation` — rotation of the screen content (`landscape`, `portrait`, `landscape-flipped`, `portrait-flipped`)
- `keyboardLayout` — physical keyboard layout

`resolution` and `screenTimeoutSec` are optional. If omitted, the reader uses the preferred resolution and a timeout of **300 seconds**.

All other request fields are also optional. Send only the settings you want to change.

## 2. Endpoint Details

| Property | Value |
|---|---|
| REST Endpoint | `PUT /cloud/displayConfig` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 only — not FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Related Endpoint | `GET /cloud/displayConfig` |
| MQTT Command | `set_displayConfig` |

## 3. Before You Begin

| What You Need | Details |
|---|---|
| Enable | `true` turns the display on; `false` turns it off. |
| Start URL | URL opened when the display is enabled, for example `https://localhost/`. |
| Resolution | Optional. `WidthxHeight`, for example `1920x1080`. If omitted, the preferred resolution is used. Confirm supported modes with `GET /cloud/inputOutputDevices`. |
| Idle timeout | Optional. `screenTimeoutSec`: `0` for always on, maximum `3600` (1 hour). If omitted, the default is `300`. |
| Orientation | `landscape`, `portrait`, `landscape-flipped`, or `portrait-flipped`. |
| Keyboard layout | One of `English-US`, `English-UK`, `German`, `Spanish`, `Italian`, `French`, `Brazilian`, `Swedish`, `Japanese`. |

A successful REST response is an empty JSON object `{}`.

Use `GET /cloud/inputOutputDevices` to confirm a monitor is connected and which resolutions it supports before setting `resolution`.
