## 1. Description

The `GET /cloud/logs/RcLog` REST endpoint retrieves the Radio Control (RC) information log from the reader as a downloadable archive.

This endpoint returns:

- The archive filename
- The Base64-encoded `.tar.gz` radio-control log content

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_logs_rcLog` |
| Pattern Name | Radio-Control Log Retrieval |
| REST Endpoint | `GET /cloud/logs/RcLog` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the radio-control information log archive |

## 3. When to Use This Endpoint

Use `GET /cloud/logs/RcLog` to:

- Retrieve radio control events and diagnostic messages for troubleshooting inventory issues
- Capture RC log data before a reader restart wipes in-memory logs
- Investigate radio connection failures or inventory start/stop events

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `filename` | Is a filename returned (for example, `rcLog.tar.gz`)? | Confirms the archive was successfully generated on the reader. |
| `binary` | Is the Base64 string non-empty? | The Base64-encoded `.tar.gz` content holds radio control state changes, errors, and diagnostics; an empty value means no data was recorded. |
