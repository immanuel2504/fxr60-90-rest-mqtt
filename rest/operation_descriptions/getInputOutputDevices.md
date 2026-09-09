## 1. Description

> **FXR60 only.** Display APIs are not available on FXR90.

The `GET /cloud/inputOutputDevices` REST endpoint retrieves the connection status and capabilities of devices attached to the reader.

This endpoint returns:

- `keyboard.status` — `connected` or `disconnected`
- `keyboard.keyboardLayout` — `English-US`, `English-UK`, `German`, `Spanish`, `Italian`, `French`, `Brazilian`, `Swedish`, or `Japanese`
- `mouse.status` — `connected` or `disconnected`
- `touch.status` — `connected` or `disconnected`
- `monitor.status` — `connected` or `disconnected`
- `manufacturer`, `model` — monitor hardware (in `monitor.details[]`)
- `currentResolution` — active `WidthxHeight`
- `supportedResolutions` — modes the hardware allows
- `orientation` — `landscape`, `portrait`, `landscape-flipped`, or `portrait-flipped`
- `screenActive` — `true` if the panel is awake, `false` if blanked by screen timeout

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_inputOutputDevices` |
| Pattern Name | Input/Output Devices Query |
| REST Endpoint | `GET /cloud/inputOutputDevices` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve attached keyboard, mouse, touch, and monitor status |

## 3. When to Use This Endpoint

Use `GET /cloud/inputOutputDevices` to:

- Confirm which peripherals are connected
- Read `supportedResolutions` before `PUT /cloud/displayConfig`
- Check whether the panel is awake (`screenActive`)
