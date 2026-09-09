## 1. Description

The `GET /cloud/region` REST endpoint retrieves the active RF region and regulatory settings.

This endpoint returns:

- `country` — country name
- `region` — region code
- `regulatoryStandard` — active standard
- `lbtEnabled` — Listen-Before-Talk
- `FrequencyHopping` — frequency hopping
- `channelData` — channel frequencies in kHz
- `minTxPowerSupported`, `maxTxPowerSupported` — transmit power range

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_region` |
| Pattern Name | Region Configuration Query |
| REST Endpoint | `GET /cloud/region` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve active RF region and regulatory settings |

## 3. When to Use This Endpoint

Use `GET /cloud/region` to:

- Read `country` and `regulatoryStandard` after `PUT /cloud/region`
- Confirm LBT, hopping, channels, and power limits
