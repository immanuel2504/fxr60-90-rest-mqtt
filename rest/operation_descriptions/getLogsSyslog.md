## 1. Description

The `GET /cloud/logs/syslog` REST endpoint retrieves the reader's operating-system system log as a downloadable archive.

This endpoint returns:

- The archive filename
- The Base64-encoded `.tar.gz` syslog content

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_logs_syslog` |
| Pattern Name | Syslog Retrieval |
| REST Endpoint | `GET /cloud/logs/syslog` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the system log archive |

## 3. When to Use This Endpoint

Use `GET /cloud/logs/syslog` to:

- Retrieve OS-level events for troubleshooting system startup, network changes, or service crashes
- Investigate unexpected reboots or hardware-related events
- Capture system logs before a reader restart resets the log buffer

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `filename` | Is a filename returned? | Confirms the archive was generated and identifies the log file for record keeping. |
| `binary` | Is the Base64 string non-empty? | Syslog captures low-level OS events that application logs may not surface; an empty value indicates no syslog data was available. |
