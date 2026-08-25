## 1. Description

The `PUT /cloud/displayConfig` REST endpoint updates display configuration on the device.

This endpoint allows you to configure:

- Display engine on or off through `enable`
- On-screen keyboard through `enableOnscreenKeyboard`
- Start URL, resolution, idle timeout, orientation, and keyboard layout

All request fields are optional. Send only the settings you want to change.

## 2. Endpoint Details

| Property | Value |
|---|---|
| REST Endpoint | `PUT /cloud/displayConfig` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Related Endpoint | `GET /cloud/displayConfig` |
| MQTT Command | `set_displayConfig` |

## 3. Before You Begin

Decide which display settings to change before sending this request.

| What You Need | Details |
|---|---|
| Enable | `true` turns the display rendering engine on; `false` turns it off. |
| Start URL | URL opened when the display is enabled, for example `https://localhost/`. |
| Resolution | Preferred monitor mode as `WidthxHeight`, for example `1920x1080`. |
| Idle timeout | `screenTimeoutSec`: `0` for always on, maximum `3600` (1 hour). |
| Orientation | `landscape`, `portrait`, `landscape-flipped`, or `portrait-flipped`. |
| Keyboard layout | One of `English-US`, `English-UK`, `German`, `Spanish`, `Italian`, `French`, `Brazilian`, `Swedish`, `Japanese`. |

A successful response is an empty JSON object `{}`.

Use `GET /cloud/inputOutputDevices` to confirm a monitor is connected and which resolutions it supports before setting `resolution`.
