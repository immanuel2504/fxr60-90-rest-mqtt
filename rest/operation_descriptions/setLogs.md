## 1. Description

The `PUT /cloud/logs` REST endpoint sets log configuration.

This endpoint sends:

- `radioPacketLog` — `true` or `false`
- `components` — optional array of `componentName` and `level`

To set a component level, send `reader_gateway` or `radio_control` as the component name (`RG` is also accepted as an alias for `reader_gateway`). Send one of the valid levels — `OFF`, `FATAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`, `TRACE`, or `EXTRA`.

If `radioPacketLog` is omitted, the reader defaults it to `false`.

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
| `radioPacketLog` | `true` to capture radio packets, `false` to stop. Include this field on every `PUT /cloud/logs` request. |
| `componentName` | `reader_gateway`, `radio_control`, or `RG` (alias for `reader_gateway`). |
| `level` | `OFF`, `FATAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`, `TRACE`, or `EXTRA`. |
