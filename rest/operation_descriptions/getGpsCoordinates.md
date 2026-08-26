## 1. Description

**Product note:** `readerLocation` is supported on **FXR90 only**. It is not available on FXR60 (no GNSS / GPS receiver).

The `GET /cloud/readerLocation` REST endpoint retrieves the reader's last reported GPS coordinates.

This endpoint returns:

- Latitude and longitude values
- The number of satellites used for the last fix
- The time the location was last reported (`lastReportedTime`)

No request body is required. The returned values represent the most recent location data known to the reader.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_gpsCoordinates` |
| Pattern Name | GPS Coordinates Query |
| REST Endpoint | `GET /cloud/readerLocation` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | **FXR90 only** (GNSS / GPS; not on FXR60) |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the reader's last known GPS coordinates |

## 3. When to Use This Endpoint

Use `GET /cloud/readerLocation` to:

- Record reader location for asset tracking or fleet management
- Confirm GPS or location availability on a deployed reader
- Feed location data into site, inventory, or logistics systems

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `latitude` | Is a valid latitude value returned? | A null or zero value may indicate the reader does not have a GPS fix yet. |
| `longitude` | Is a valid longitude value returned? | Combined with latitude, this identifies the reader's physical position. |
| `satellitesUsed` | How many satellites produced the fix? | A low satellite count indicates a weak fix and less reliable coordinates. |
| `lastReportedTime` | When was the location last reported? | Indicates how recent the coordinates are; a stale timestamp means the position may be outdated. |
