## 1. Description

> **FXR60 only.** Display APIs are not available on FXR90.

The `GET /cloud/inputOutputDevices` REST endpoint retrieves the connection status and capabilities of devices attached to the reader.

Peripheral and monitor details are documented in the response schema and in the key fields table below.

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

- Confirm which peripherals are connected before changing display settings
- Read supported monitor resolutions before `PUT /cloud/displayConfig`

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `monitor.connected` | Is a monitor attached? | Display APIs apply only when a monitor is present. |
| `monitor.supportedResolutions` | Which resolutions are supported? | List of resolutions supported by the monitor hardware. Use these values in `PUT /cloud/displayConfig`. |
| `monitor.currentResolution` | What resolution is active? | Confirms the current `<width>x<height>` string. |
| `monitor.screenActive` | Is the panel awake? | `true` when the display is on; `false` when sleeping. |
