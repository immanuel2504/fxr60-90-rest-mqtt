## 1. Description

The `GET /cloud/gpo` REST endpoint retrieves the current digital output state of all GPO (General Purpose Output) pins on the reader.

This endpoint returns:

- The current HIGH or LOW state of each GPO pin (pins 1–4)

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_gpoStatus` |
| REST Endpoint | `GET /cloud/gpo` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |

## 3. When to Use This Endpoint

Use `GET /cloud/gpo` to:

- Verify the current state of GPO outputs before issuing a GPO control command
- Troubleshoot whether an actuator or signaling device connected to a GPO pin is receiving the correct signal
- Confirm the effect of a prior GPO set command

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `1` | Is GPO pin 1 HIGH or LOW? | Confirms whether the device driven by port 1 (e.g., a light or gate) is active. |
| `2` | Is GPO pin 2 HIGH or LOW? | Confirms whether the device driven by port 2 is active. |
| `3` | Is GPO pin 3 HIGH or LOW? | Confirms whether the device driven by port 3 is active. |
| `4` | Is GPO pin 4 HIGH or LOW? | Confirms whether the device driven by port 4 is active. |
