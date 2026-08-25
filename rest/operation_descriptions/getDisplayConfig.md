## 1. Description

The `GET /cloud/displayConfig` REST endpoint retrieves the currently active display configuration from the device.

This endpoint returns:

- Whether the display rendering engine is enabled
- On-screen keyboard, start URL, resolution, idle timeout, orientation, and keyboard layout

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| REST Endpoint | `GET /cloud/displayConfig` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Related Endpoint | `PUT /cloud/displayConfig` |
| MQTT Command | `get_displayConfig` |

## 3. When to Use This Endpoint

Use `GET /cloud/displayConfig` to:

- Confirm the display is on and showing the expected URL
- Read the active resolution, orientation, and keyboard layout
- Verify the effect of a prior `PUT /cloud/displayConfig` call

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `enable` | Is the display engine on? | `false` means the panel is not rendering. |
| `startUrl` | Which URL is loaded? | Confirms the kiosk or local UI target. |
| `resolution` | Is it `WidthxHeight` as expected? | Must match a resolution the monitor supports. |
| `screenTimeoutSec` | Idle timeout, or `0` for always on | `0` keeps the screen awake; maximum is 3600 seconds. |
| `orientation` | `landscape`, `portrait`, or a flipped variant | Controls how content is rotated. |
| `keyboardLayout` | Physical layout such as `English-US` | Must match the attached keyboard. |
