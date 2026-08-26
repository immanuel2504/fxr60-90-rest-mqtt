## 1. Description

The `GET /cloud/timeZone` REST endpoint retrieves the time zone currently configured on the reader.

This endpoint returns:

- The configured time zone value (a reader-supported time zone name in `(GMT±hh:mm) Region` format)

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_timeZone` |
| Pattern Name | Time Zone Query |
| REST Endpoint | `GET /cloud/timeZone` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the configured time zone |

## 3. When to Use This Endpoint

Use `GET /cloud/timeZone` to:

- Confirm the reader's time zone before relying on event timestamps
- Verify the result of a prior `PUT /cloud/timeZone` call
- Audit time zone consistency across a fleet of readers

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `timeZone` | Is this the correct time zone for the deployment location? | An incorrect time zone causes local event timestamps to be offset from actual local time. |
