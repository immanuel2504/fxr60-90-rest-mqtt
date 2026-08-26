## 1. Description

The `GET /cloud/hostName` REST endpoint retrieves the reader's currently configured network hostname.

This endpoint returns:

- The hostname string currently assigned to the reader

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_hostName` |
| Pattern Name | Hostname Query |
| REST Endpoint | `GET /cloud/hostName` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve the configured reader hostname |

## 3. When to Use This Endpoint

Use `GET /cloud/hostName` to:

- Verify the hostname assigned to a reader during provisioning
- Confirm the hostname matches the expected naming convention for the deployment
- Retrieve the current hostname before changing it with `PUT /cloud/hostName`
- Verify the result of a prior `PUT /cloud/hostName` call

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `hostName` | Does it match the expected naming convention? | The hostname identifies the reader on the local network and in management systems; a mismatch may indicate the wrong reader was configured. |
