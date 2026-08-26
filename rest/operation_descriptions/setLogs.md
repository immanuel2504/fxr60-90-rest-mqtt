## 1. Description

The `PUT /cloud/logs` REST endpoint configures logging behavior on the reader, including per-component log verbosity and radio packet log capture.

This endpoint allows you to configure:

- Whether radio packet logging is enabled through `radioPacketLog`
- The log level for each reader software component through `components`

Use this endpoint to:

- Enable radio packet logging before collecting RF diagnostic data
- Increase log verbosity for a specific component during troubleshooting
- Reduce log verbosity in production to limit storage consumption
- Reset component log levels to a known state before a support capture

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
| Supported Log Levels | `OFF`, `FATAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`, `TRACE`, `EXTRA` |
| Supported Components | `radio_control` (alias `RC`), `cloud_agent`, `reader_gateway` (alias `RG`) |

## 3. Before You Begin

Decide which logging areas you need to change before sending this request. Verbose log levels can fill storage quickly in production deployments.

| What You Need | Details |
|---|---|
| Radio packet log | Whether to enable or disable `radioPacketLog` (boolean). Enabling this is required before `GET /cloud/logs/radioPacketLog` will return useful data. |
| Component name | The component whose level to change: `radio_control` (alias `RC`), `cloud_agent`, or `reader_gateway` (alias `RG`). |
| Log level | The verbosity level to apply, one of `OFF`, `FATAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`, `TRACE`, or `EXTRA`. `OFF` disables logging for the component. |
| Storage impact | Verbose levels such as `DEBUG`, `TRACE`, and `EXTRA` generate the most data. Confirm available flash storage before enabling verbose logging for extended periods. |
