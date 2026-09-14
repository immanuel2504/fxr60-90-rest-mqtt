## Description

The `heartbeat` event gives periodic management status from the reader. The reader publishes one heartbeat payload at the configured interval.

This event is useful when the backend must confirm that the reader is online and monitor reader health over time.

## Event Details

| Property | Value |
|---|---|
| MQTT event | `heartbeat` |
| Envelope `type` | `heartbeat` |
| Configuration path | `READER-GATEWAY.managementEventConfig.heartbeat` |
| Configure using MQTT | `set_config` |
| Configure using REST | `PUT /cloud/config` |
| Delivery destination | `endpointConfig.management.event` |
| Communication type | Device to Cloud |
| Applies to | FXR60 / FXR90 |

## How Heartbeat Works

The reader publishes a single management event with `type` `heartbeat`. The `data` object contains only the sections configured in `heartbeat.fields`:

- `radio_control` — Radio Control process health, antenna and radio status, and tag-read statistics. See [Radio Control](heartbeat_radio_control.md) for more details.
- `reader_gateway` — Reader Gateway process health, connection status, and management-event and data-path counts. See [Reader Gateway](heartbeat_reader_gateway.md) for more details.
- `system` — Reader system health, including CPU, RAM, flash, temperature, time, GPIO state, and host identity. See [System](heartbeat_system.md) for more details.
- `userapps` — Status and resource usage for each installed user application. Empty when no user applications are installed. See [User Apps](heartbeat_userapps.md) for more details.

## Configure the Heartbeat Event

Set the management-event destination on the common management-event configuration page.

To set the heartbeat interval and select heartbeat fields, use `set_config` and configure:

```text
READER-GATEWAY.managementEventConfig.heartbeat
```

Use:

- `interval` to set how often the reader publishes heartbeat events.
- `fields` to select which heartbeat sections and fields are published.

Choose **MQTT — set_config** or **REST — PUT /cloud/config** from the **Example** dropdown in **Configuration Examples** below.

## Parameters

| Field | Description | Default |
|---|---|---|
| `interval` | Heartbeat publish interval, in seconds. Set to `0` to disable heartbeat events. | `60` |
| `fields.radio_control` | Radio Control heartbeat fields to publish. | Enabled |
| `fields.reader_gateway` | Reader Gateway heartbeat fields to publish. | Enabled |
| `fields.system` | System heartbeat fields to publish. | Enabled |
| `fields.userapps` | User Apps heartbeat fields to publish. | Enabled |
| `fields.userDefined` | Optional static key-value pairs copied into each heartbeat payload. | Omitted |

## Response Schema

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `heartbeat`. |
| `timestamp` | string | Event timestamp. |
| `component` | string | Component that published the event. |
| `eventNum` | number | Management event sequence number. |
| `data.radio_control` | object | Radio Control heartbeat section. |
| `data.reader_gateway` | object | Reader Gateway heartbeat section. |
| `data.system` | object | System heartbeat section. |
| `data.userapps` | array | User application heartbeat section. Empty when no user applications are installed. |
