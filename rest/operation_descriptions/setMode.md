## 1. Description

The `PUT /cloud/mode` REST endpoint configures the reader's operating mode and all RF settings associated with that mode.

This endpoint allows you to configure:

- The operating mode type through `type`
- Antenna port selection and transmit power through `antennas`
- The RF environment profile through `environment`
- Inventory stop behavior through `antennaStopCondition`
- Gen2 query, select, and access settings
- Report filtering, RSSI filtering, and metadata options

Use this endpoint to:

- Switch between `SIMPLE`, `INVENTORY`, `PORTAL`, `CONVEYOR`, or `CUSTOM` modes
- Tune antenna ports and transmit power for the deployment environment
- Configure portal triggers or inventory intervals for the chosen mode type
- Apply tag filtering and reporting behavior before starting inventory

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Operating Mode Configuration |
| REST Endpoint | `PUT /cloud/mode` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Request Schema | `operatingMode.v1` |
| Supported Mode Types | `SIMPLE`, `INVENTORY`, `PORTAL`, `CONVEYOR`, `CUSTOM` |
| Supported Environment Profiles | `LOW_INTERFERENCE`, `HIGH_INTERFERENCE`, `VERY_HIGH_INTERFERENCE`, `AUTO_DETECT`, `DEMO` |

## 3. Before You Begin

Decide on your mode configuration before sending this request. Changing mode while inventory is active can disrupt reads - call `PUT /cloud/stop` first if the reader is currently reading.

| What You Need | Details |
|---|---|
| Mode type | One of `SIMPLE`, `INVENTORY`, `PORTAL`, `CONVEYOR`, or `CUSTOM`. |
| Antenna ports and power | Which antenna ports (or ATR beams) to enable and the transmit power in dBm for each. |
| Environment profile | Optional - set to match the RF environment at the deployment site. Use `AUTO_DETECT` if unsure. |
| Mode-specific settings | Inventory interval for `INVENTORY`; GPI triggers and stop interval for `PORTAL`. Only include the sub-object relevant to the chosen mode type. |
| Gen2 and reporting settings | Query settings, select operations, and optional access operations, plus metadata fields, report filter, RSSI filter, and radio start/stop conditions. |
| Active inventory | If the reader is currently reading tags, send `PUT /cloud/stop` before changing the mode to avoid disrupting ongoing inventory. |
