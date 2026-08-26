## 1. Description

> **Product applicability: FXR60 only.** Display APIs are not available on FXR90.

The `GET /cloud/displayConfig` REST endpoint retrieves the currently active display configuration from the device.

This endpoint returns:

- Whether the display is enabled
- On-screen keyboard, start URL, resolution, idle timeout, orientation, and keyboard layout

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| REST Endpoint | `GET /cloud/displayConfig` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 only — not FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Related Endpoint | `PUT /cloud/displayConfig` |
| MQTT Command | `get_displayConfig` |

## 3. When to Use This Endpoint

Use `GET /cloud/displayConfig` to read the display settings last applied with `PUT /cloud/displayConfig`.

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `enable` | Is the display on? | `false` means the display is disabled. |
| `enableOnscreenKeyboard` | Is the virtual touch keyboard on? | Needed when no physical keyboard is attached. |
| `startUrl` | Which URL is loaded? | Confirms the kiosk or local UI target. |
| `resolution` | Is it `WidthxHeight` as expected? | Must match a resolution the monitor supports. |
| `screenTimeoutSec` | Idle timeout, or `0` for always on | `0` keeps the screen awake; maximum is 3600 seconds. |
| `orientation` | `landscape`, `portrait`, or a flipped variant | Controls how content is rotated. |
| `keyboardLayout` | Layout such as `Japanese` or `English-US` | Should match the attached keyboard when one is present. |
