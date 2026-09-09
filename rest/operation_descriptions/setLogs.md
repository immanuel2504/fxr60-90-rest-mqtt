## 1. Description

The `PUT /cloud/logs` REST endpoint sets log configuration.

This endpoint sends:

- `radioPacketLog` — `true` or `false`
- `components` — optional array of `componentName` and `level`

To change a component level, send `reader_gateway` (or `RG`).

`level` is `OFF`, `FATAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`, `TRACE`, or `EXTRA`.

Omitted `radioPacketLog` returns to `false`.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_logs` |
| Pattern Name | Log Configuration |
| REST Endpoint | `PUT /cloud/logs` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |

## 3. Before You Begin

Decide `radioPacketLog` and any component level. Use the JSON field names below.

| Field | What to set |
|---|---|
| `radioPacketLog` | `true` to capture radio packets, `false` to stop. Send this on every `PUT /cloud/logs`. |
| `componentName` | `reader_gateway` or `RG`. |
| `level` | `OFF`, `FATAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`, `TRACE`, or `EXTRA`. |
