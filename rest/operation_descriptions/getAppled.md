## 1. Description

The `GET /cloud/app-led` REST endpoint retrieves whether the application LED is under reader control or has been set by an application.

This endpoint returns:

- `status` — `DEFAULT` or `NON_DEFAULT`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_appled` |
| Pattern Name | Application LED Query |
| REST Endpoint | `GET /cloud/app-led` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve application LED status |
| Response field | `status`: `DEFAULT` \| `NON_DEFAULT` |

## 3. When to Use This Endpoint

Use `GET /cloud/app-led` to:

- Check whether the LED is `DEFAULT` or `NON_DEFAULT`
- Confirm that a prior `PUT /cloud/app-led` moved the LED out of `DEFAULT`
