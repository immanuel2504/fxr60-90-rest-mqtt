## 1. Description

The `PUT /cloud/mode` REST endpoint configures the reader's operating mode. The request body is an `operatingMode.v1` object.

This call **replaces the entire mode configuration**. Fields you omit are not kept from the previous mode — send the full object you want the reader to use.

This endpoint allows you to configure:

- The operating mode type through `type`
- Antenna port selection and transmit power through `antennas` and `transmitPower`
- The RF environment profile through `environment`
- Inventory stop behavior through `antennaStopCondition`
- Gen2 query, select, and access settings
- Report filtering, RSSI filtering, and metadata options

Use this endpoint to:

- Switch between `SIMPLE`, `INVENTORY`, `PORTAL`, `CONVEYOR`, or `CUSTOM`
- Tune antenna ports and transmit power for the deployment environment
- Configure portal triggers or inventory intervals for the chosen mode type
- Apply tag filtering and reporting behavior before starting inventory

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_mode` |
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

Decide on your mode configuration before sending this request. Changing mode while inventory is active can disrupt reads — call `PUT /cloud/stop` first if the reader is currently reading.

| What You Need | Details |
|---|---|
| Mode type | One of `SIMPLE`, `INVENTORY`, `PORTAL`, `CONVEYOR`, or `CUSTOM`. |
| Antenna ports and power | Which antenna ports to enable, and transmit power in **dBm** (0.0–30.0). |
| Environment profile | Optional. Set to match the RF environment. Use `AUTO_DETECT` if unsure. Default is `HIGH_INTERFERENCE`. |
| Mode-specific settings | Inventory interval for `INVENTORY`; GPI trigger (`port` 1–4) and stop interval for `PORTAL`. Include only the sub-object for the chosen type. |
| Gen2 and reporting | Query, selects, optional accesses (`wordCount`, not `wordCounter`), metadata (`READERLOCATION`, not `READER_LOCATION`), report filter, RSSI filter, and radio start/stop conditions. |

## 4. Mode and field rules

These rules match `operatingMode.v1`:

| Rule | Detail |
|---|---|
| Wholesale replace | The new body replaces the previous mode. Omitted fields are not merged. |
| `SIMPLE` | Do not send `tagMetaData`. Tag events include only `eventNum`, `format`, and `idHex`. |
| `INVENTORY` | `accesses` is not allowed. Use `modeSpecificSettings.interval` to control how often each tag is reported. |
| `PORTAL` | `radioStartConditions` and `radioStopConditions` are not allowed. GPI `port` is 1–4. |
| Prefix `filter` | Cannot be set together with `query` or `selects`. |
| `reportFilter` and `accesses` | Cannot both be set. |
| Memory-bank metadata | `accesses` cannot be combined with `tagMetaData` values `RESERVED`, `EPC`, `TID`, or `USER`. |
| Array lengths | When `transmitPower`, `antennaStopCondition`, or `query` is an array, its length must match `antennas`. |
