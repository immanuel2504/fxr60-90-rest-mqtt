## 1. Description

The `GET /cloud/ntpServer` REST endpoint retrieves the NTP server currently configured for time synchronization on the reader.

This endpoint returns:

- The NTP server hostname or IP address

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | NTP Server Query |
| REST Endpoint | `GET /cloud/ntpServer` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the configured NTP server |

## 3. When to Use This Endpoint

Use `GET /cloud/ntpServer` to:

- Confirm the reader is pointed at the correct time source for the deployment
- Verify the result of a prior `PUT /cloud/ntpServer` call
- Troubleshoot clock drift that is affecting event timestamps

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `server` | Is this the correct NTP server address? | An incorrect or unreachable NTP server causes clock drift, making event timestamps unreliable. |
