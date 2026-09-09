## 1. Description

The `GET /cloud/supportedStandardList` REST endpoint retrieves the regulatory standards for a country.

Send `region` — a country name from `GET /cloud/supportedRegionList`.

This endpoint returns:

- `StandardName` — standard identifier (in `SupportedStandards[]`)
- `channeldata` — channel frequencies in kHz
- `isChannelSelectable` — `"true"` or `"false"`
- `isHoppingConfigurable` — `"true"` or `"false"`
- `isLBTConfigurable` — `"true"` or `"false"`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_supportedStandardList` |
| Pattern Name | Supported Standard Query |
| REST Endpoint | `GET /cloud/supportedStandardList` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve standards and channel details for a country |

## 3. When to Use This Endpoint

Use `GET /cloud/supportedStandardList` to:

- Get the exact `standardname` string before `PUT /cloud/region`
- See whether LBT or channel selection can be set for that standard
