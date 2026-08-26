## 1. Description

The `GET /cloud/logs/radioPacketLog` REST endpoint retrieves the radio packet log from the reader as a downloadable archive.

This endpoint returns:

- The archive filename
- The Base64-encoded `.tar.gz` radio packet log content

No request body is required. Radio packet logging must be enabled via `PUT /cloud/logs` before this endpoint will return meaningful data.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_logs_radioPacketLog` |
| Pattern Name | Radio Packet Log Retrieval |
| REST Endpoint | `GET /cloud/logs/radioPacketLog` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the radio packet log archive |

## 3. When to Use This Endpoint

Use `GET /cloud/logs/radioPacketLog` to:

- Download RF-level packet data for deep diagnostics of inventory performance
- Analyze raw radio events to investigate tag read anomalies or read rate issues
- Retrieve packet logs after a troubleshooting session before clearing or restarting the reader

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `filename` | Is a filename returned? | Confirms the archive was generated and ready for download. |
| `binary` | Is the Base64 string non-empty? | The Base64-encoded `.tar.gz` content holds the RF packet data; an empty value means radio packet logging was not enabled when the events occurred. |
