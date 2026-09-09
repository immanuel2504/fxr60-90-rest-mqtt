## 1. Description

> **FXR60 only.** Display APIs are not available on FXR90.

The `GET /cloud/displayConfig` REST endpoint retrieves the active display configuration.

This endpoint returns:

- `enable` — whether the display is on
- `enableOnscreenKeyboard` — whether the on-screen keyboard is on
- `startUrl` — URL loaded on the display
- `resolution` — active resolution (`WidthxHeight`)
- `screenTimeoutSec` — idle timeout in seconds
- `orientation` — `landscape`, `portrait`, `landscape-flipped`, or `portrait-flipped`
- `keyboardLayout` — `English-US`, `English-UK`, `German`, `Spanish`, `Italian`, `French`, `Brazilian`, `Swedish`, or `Japanese`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_displayConfig` |
| Pattern Name | Display Configuration Query |
| REST Endpoint | `GET /cloud/displayConfig` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve active display configuration |

## 3. When to Use This Endpoint

Use `GET /cloud/displayConfig` to:

- Read the settings last applied with `PUT /cloud/displayConfig`
- Confirm enable, URL, resolution, orientation, and keyboard layout
