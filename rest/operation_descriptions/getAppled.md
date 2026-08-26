## 1. Description

The `GET /cloud/app-led` REST endpoint retrieves the current state of the application LED on the reader.

This endpoint returns:

- The application LED status (`DEFAULT` or `NON_DEFAULT`)

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_appled` |
| REST Endpoint | `GET /cloud/app-led` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |

## 3. When to Use This Endpoint

Use `GET /cloud/app-led` to:

- Confirm whether the application LED is showing default reader state or has been overridden
- Verify the effect of a prior `PUT /cloud/app-led` call
- Audit LED state as part of a device health or provisioning check

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `status` | Is it `DEFAULT` or `NON_DEFAULT`? | `NON_DEFAULT` indicates the LED has been overridden by the application; `DEFAULT` means it reflects normal reader status. |
