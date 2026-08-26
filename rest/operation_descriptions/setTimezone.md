## 1. Description

The `PUT /cloud/timeZone` REST endpoint sets the time zone on the reader.

This endpoint allows you to configure:

- The reader's local time zone through `timeZone`

Use this endpoint to:

- Align the reader's clock with the deployment site's local time zone
- Correct event timestamps and log timestamps for local time reporting
- Standardize time zone configuration across a fleet of readers
- Update the time zone after a reader is relocated to a different region

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_timeZone` |
| Pattern Name | Time Zone Configuration |
| REST Endpoint | `PUT /cloud/timeZone` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `timeZone` |

## 3. Before You Begin

Have the exact time zone string ready before sending this request. An unrecognized time zone string will be rejected.

| What You Need | Details |
|---|---|
| Time zone string | A reader-supported time zone name (e.g., `"International Date Line West"`, `"Pacific Time (US & Canada)"`). Use `GET /cloud/timeZone` to check the currently configured value. |
| Site location | Confirm the physical deployment location of the reader to select the correct time zone. |
