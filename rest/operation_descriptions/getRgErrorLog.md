## 1. Description

The `GET /cloud/logs/RgErrorLog` REST endpoint retrieves the Reader Gateway error log from the reader as a downloadable archive.

This endpoint returns:

- The archive filename
- The Base64-encoded `.tar.gz` reader-gateway error log content

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Reader-Gateway Error Log Retrieval |
| REST Endpoint | `GET /cloud/logs/RgErrorLog` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the reader-gateway error log archive |

## 3. When to Use This Endpoint

Use `GET /cloud/logs/RgErrorLog` to:

- Retrieve Reader Gateway error events for troubleshooting connectivity or data delivery failures
- Investigate errors that occurred during tag data forwarding or cloud endpoint communication
- Capture error logs before a reader restart clears in-memory data

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `filename` | Is a filename returned (for example, `rgErrorLog.tar.gz`)? | Confirms the archive was generated and is ready for download. |
| `binary` | Is the Base64 string non-empty? | The Base64-encoded `.tar.gz` content reveals the specific failures affecting Reader Gateway operation; an empty value means no errors have been logged since the last purge. |
