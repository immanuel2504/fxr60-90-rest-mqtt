## 1. Description

The `GET /cloud/logs/RgWarningLog` REST endpoint retrieves the Reader Gateway warning log from the reader as a downloadable archive.

This endpoint returns:

- The archive filename
- The Base64-encoded `.tar.gz` reader-gateway warning log content

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Reader-Gateway Warning Log Retrieval |
| REST Endpoint | `GET /cloud/logs/RgWarningLog` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the reader-gateway warning log archive |

## 3. When to Use This Endpoint

Use `GET /cloud/logs/RgWarningLog` to:

- Review Reader Gateway warning events that may indicate non-critical but notable operational issues
- Investigate intermittent connectivity or data delivery problems that did not produce errors
- Capture warning logs as part of routine reader health monitoring

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `filename` | Is a filename returned (for example, `rgWarningLog.tar.gz`)? | Confirms the archive was generated and is ready for download. |
| `binary` | Is the Base64 string non-empty? | Repeated warnings often precede errors; an empty value means no warnings have been logged since the last purge. |
