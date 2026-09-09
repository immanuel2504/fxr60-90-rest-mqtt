## 1. Description

The `GET /cloud/supportedRegionList` REST endpoint retrieves the country names this reader accepts.

This endpoint returns:

- `SupportedRegions` — country or region names for `PUT /cloud/region` `country`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_supportedRegionList` |
| Pattern Name | Supported Region Query |
| REST Endpoint | `GET /cloud/supportedRegionList` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve permitted country names |

## 3. When to Use This Endpoint

Use `GET /cloud/supportedRegionList` to:

- Get the exact `country` string before `PUT /cloud/region`
- Get the `region` value for `GET /cloud/supportedStandardList`
