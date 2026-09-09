## 1. Description

The `PUT /cloud/gpo` REST endpoint sets one GPO pin.

This endpoint requires:

- `port` — pin number `1`, `2`, `3`, or `4`
- `state` — `true` for HIGH, `false` for LOW

One pin per request.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_gpo` |
| Pattern Name | GPO Control |
| REST Endpoint | `PUT /cloud/gpo` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `port`, `state` |

## 3. Before You Begin

Decide the pin and the state to send. Use the JSON field names below.

| Field | What to set |
|---|---|
| `port` | Pin to drive: `1`, `2`, `3`, or `4`. |
| `state` | `true` for HIGH, `false` for LOW. |
