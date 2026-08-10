## 1. Description

The `GET /cloud/gpi` REST endpoint retrieves the current digital input state of all GPI (General Purpose Input) pins on the reader.

This endpoint returns:

- The current HIGH or LOW state of each GPI pin (pins 1-4)

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| REST Endpoint | `GET /cloud/gpi` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |

## 3. When to Use This Endpoint

Use `GET /cloud/gpi` to:

- Check the current digital state of trigger or sensor inputs connected to GPI pins
- Verify GPI pin state before applying a GPI-triggered workflow
- Troubleshoot whether an external trigger signal is being received at the reader

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `1` | Is GPI pin 1 HIGH or LOW? | Confirms whether the wired sensor or trigger on port 1 is currently active. |
| `2` | Is GPI pin 2 HIGH or LOW? | Confirms whether the wired sensor or trigger on port 2 is currently active. |
| `3` | Is GPI pin 3 HIGH or LOW? | Confirms whether the wired sensor or trigger on port 3 is currently active. |
| `4` | Is GPI pin 4 HIGH or LOW? | Confirms whether the wired sensor or trigger on port 4 is currently active. |
