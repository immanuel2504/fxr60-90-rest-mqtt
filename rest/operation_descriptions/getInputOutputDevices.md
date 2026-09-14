## 1. Description

> **FXR60 only.** Display APIs are not available on FXR90.

The `GET /cloud/inputOutputDevices` REST endpoint retrieves the connection status and capabilities of devices attached to the reader.

This endpoint returns:

- Connection status for the attached keyboard, mouse, touch panel, and monitor
- The active keyboard layout
- Monitor hardware details, current and supported resolutions, orientation, and whether the panel is awake

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
