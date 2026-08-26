## 1. Description

> **Product applicability: FXR60 only.** Display APIs are not available on FXR90.

The `GET /cloud/inputOutputDevices` REST endpoint retrieves the connection status and capabilities of input/output devices attached to the reader.

This endpoint returns:

- Keyboard status and active layout
- Mouse and touch connection status
- Monitor status, including hardware details and capabilities

`monitor` shows the connected monitor's detailed capabilities and hardware information.

`screenActive` indicates whether the display screen is currently awake, or blanked because of screen timeout.

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| REST Endpoint | `GET /cloud/inputOutputDevices` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 only — not FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Related Endpoint | `GET /cloud/displayConfig` |
| MQTT Command | `get_inputOutputDevices` |

## 3. When to Use This Endpoint

Use `GET /cloud/inputOutputDevices` to:

- Confirm a keyboard, mouse, touch screen, or monitor is connected
- Read supported monitor resolutions before calling `PUT /cloud/displayConfig`
- Check whether the monitor is awake (`screenActive: true`) or blanked by screen timeout

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `keyboard.status` / `mouse.status` / `touch.status` / `monitor.status` | `connected` or `disconnected` | Tells you which peripherals are present. |
| `keyboard.keyboardLayout` | Active layout such as `Japanese` | Should match `displayConfig.keyboardLayout` when a keyboard is attached. |
| `monitor.details[].currentResolution` | Active `WidthxHeight` | Compare with `GET /cloud/displayConfig` `resolution`. |
| `monitor.details[].supportedResolutions` | List of modes the hardware allows | Use a value from this list in `PUT /cloud/displayConfig`. |
| `monitor.details[].screenActive` | Awake vs blanked | `false` means the panel is blanked because of screen timeout. |
