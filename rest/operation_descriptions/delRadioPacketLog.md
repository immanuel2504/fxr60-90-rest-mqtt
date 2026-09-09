## 1. Description

The `DELETE /cloud/logs/radioPacketLog` REST endpoint deletes stored radio packet log files.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `del_logs_radioPacketLog` |
| Pattern Name | Radio Packet Log Purge |
| REST Endpoint | `DELETE /cloud/logs/radioPacketLog` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Request Body | None |

## 3. Before You Begin

Download first with `GET /cloud/logs/radioPacketLog` if you need to keep the files.
