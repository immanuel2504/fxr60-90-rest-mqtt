## 1. Description

The `GET /cloud/readerLocation` REST endpoint retrieves the last reported GPS coordinates.

This endpoint returns:

- `latitude`
- `longitude`
- `satellitesUsed`
- `lastReportedTime`

Supported on FXR90 only.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_gpsCoordinates` |
| Pattern Name | GPS Coordinates Query |
| REST Endpoint | `GET /cloud/readerLocation` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve GPS coordinates |

## 3. When to Use This Endpoint

Use `GET /cloud/readerLocation` to:

- Read `latitude`, `longitude`, `satellitesUsed`, and `lastReportedTime`
