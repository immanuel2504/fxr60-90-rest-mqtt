## 1. Description

The `GET /cloud/logs` REST endpoint retrieves the reader's current log configuration, including the radio packet log enable flag and per-component log levels.

This endpoint returns:

- Whether radio packet logging is enabled (`radioPacketLog`)
- The configured log level for each reader software component (`components`)

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_logs` |
| Pattern Name | Log Configuration Query |
| REST Endpoint | `GET /cloud/logs` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve current logging configuration |

## 3. When to Use This Endpoint

Use `GET /cloud/logs` to:

- Review which components are set to verbose or debug logging before a troubleshooting session
- Confirm radio packet log capture is enabled before downloading log files
- Audit per-component verbosity during troubleshooting or before a support handoff
- Verify the effect of a prior `PUT /cloud/logs` call

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `radioPacketLog` | Is packet logging enabled? | Must be enabled before log files (`GET /cloud/logs/radioPacketLog`) will contain meaningful data. |
| `components` | Are component levels set to the appropriate verbosity? | Higher verbosity generates more log data but may affect performance in production deployments. |
