## 1. Description

The `GET /cloud/config` REST endpoint retrieves the reader's full configuration, including RF settings, GPIO and LED defaults, and reader-gateway endpoint settings.

This endpoint returns:

- GPIO and LED trigger configuration (`GPIO-LED`), including GPO and LED defaults; returned as an empty object `{}` when unset
- Reader-gateway settings including tag data retention, batching, and endpoint configuration

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Reader Configuration Query |
| REST Endpoint | `GET /cloud/config` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve active reader configuration |

## 3. When to Use This Endpoint

Use `GET /cloud/config` to:

- Review the active configuration before calling `PUT /cloud/config`
- Audit GPIO and LED default states across a fleet of readers
- Inspect tag-data retention and batching settings
- Confirm which data and management endpoints are configured

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `READER-GATEWAY` | Are endpoint URLs and credentials correct? | Determines where tag data is delivered and how the reader authenticates. |
| `GPIO-LED.GPODefaults` | What are the default GPO states? | Ensures GPO-triggered logic starts from the expected initial state. |
| `GPIO-LED.LEDDefaults` | What are the LED default states? | Confirms expected LED behavior on startup and after a reboot. |
