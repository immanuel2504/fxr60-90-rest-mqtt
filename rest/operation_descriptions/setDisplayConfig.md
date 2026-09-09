## 1. Description

> **FXR60 only.** Display APIs are not available on FXR90.

The `PUT /cloud/displayConfig` REST endpoint sets the display configuration.

This endpoint sends:

- `enable` — `true` turns the display on, `false` turns it off
- `enableOnscreenKeyboard` — on-screen keyboard
- `startUrl` — URL opened when the display is enabled
- `resolution` — `WidthxHeight`
- `screenTimeoutSec` — idle timeout in seconds (`0` keeps the screen on; maximum `3600`)
- `orientation` — `landscape`, `portrait`, `landscape-flipped`, or `portrait-flipped`
- `keyboardLayout` — `English-US`, `English-UK`, `German`, `Spanish`, `Italian`, `French`, `Brazilian`, `Swedish`, or `Japanese`

Omitted fields keep their current values.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_displayConfig` |
| Pattern Name | Display Configuration |
| REST Endpoint | `PUT /cloud/displayConfig` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |

## 3. Before You Begin

Decide the display settings to send. Use the JSON field names below.

| Field | What to set |
|---|---|
| `enable` | `true` to turn the display on, `false` to turn it off. |
| `enableOnscreenKeyboard` | `true` to show the on-screen keyboard, `false` to hide it. |
| `startUrl` | Page the display opens, for example `https://localhost/`. |
| `resolution` | Size as `WidthxHeight`, for example `1920x1080`. Use `GET /cloud/inputOutputDevices` to see supported modes. |
| `screenTimeoutSec` | Idle time in seconds before the screen sleeps. `0` keeps it on. Maximum `3600`. |
| `orientation` | `landscape`, `portrait`, `landscape-flipped`, or `portrait-flipped`. |
| `keyboardLayout` | `English-US`, `English-UK`, `German`, `Spanish`, `Italian`, `French`, `Brazilian`, `Swedish`, or `Japanese`. |

