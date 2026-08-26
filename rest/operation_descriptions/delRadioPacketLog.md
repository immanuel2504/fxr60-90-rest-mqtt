## 1. Description

The `DELETE /cloud/logs/radioPacketLog` REST endpoint purges radio packet log files stored on the reader. When you call this endpoint, all accumulated radio packet log data is permanently deleted from the reader's storage.

Use this endpoint to:

- Clear radio packet log archives after downloading them with `GET /cloud/logs/radioPacketLog`
- Free flash storage consumed by high-volume RF packet trace data
- Reset the packet log before starting a new diagnostic capture session

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

Download the log files with `GET /cloud/logs/radioPacketLog` before sending this request if you need to retain the data for RF analysis or support cases.

| What You Need | Details |
|---|---|
| Log retrieval | Confirm you have downloaded the radio packet logs using `GET /cloud/logs/radioPacketLog` before purging. Deletion is permanent and cannot be undone. |
| Logging state | If radio packet logging (`radioPacketLog`) is currently enabled, the reader will start writing new log data immediately after purge. Disable logging first (via `PUT /cloud/logs`) if you want to start a clean session with no logging active. |
