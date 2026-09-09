## 1. Description

The `GET /cloud/gpi` REST endpoint retrieves the current input state of each GPI pin.

This endpoint returns:

- `1`, `2`, `3`, `4` — `HIGH` or `LOW`

GPI pins are inputs. This call does not change them.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_gpiStatus` |
| Pattern Name | GPI Status Query |
| REST Endpoint | `GET /cloud/gpi` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve GPI pin states |

## 3. When to Use This Endpoint

Use `GET /cloud/gpi` to:

- Read the state of sensors or triggers wired to GPI pins
