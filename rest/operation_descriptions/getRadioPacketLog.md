## 1. Description

The `GET /cloud/logs/radioPacketLog` REST endpoint retrieves the radio packet log archive.

Enable capture first with `PUT /cloud/logs` `radioPacketLog` `true`.

This endpoint returns:

- `filename` — archive name, for example `radioPktLog.tar.gz`
- `binary` — Base64-encoded `.tar.gz`

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

- Download RF packet data as `filename` + `binary`
