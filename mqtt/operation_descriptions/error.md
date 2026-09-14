## Description

The `error` event is published on the management channel when the reader detects an error-level condition.

Each error event includes a human-readable message in `data.message`. The envelope `component` identifies the source of the error.

This event includes:

- The component that reported the error.
- The error message in `data.message`.

This event is useful when the backend must receive reader, Radio Control, Reader Gateway, antenna, memory, CPU, RAM, flash, NTP, radio, database, or user application errors from the management event stream.

## Event Details

| Property | Value |
|---|---|
| MQTT event | `error` |
| Envelope `type` | `error` |
| Configuration path | `READER-GATEWAY.managementEventConfig.errors` |
| Configure using MQTT | `set_config` |
| Configure using REST | `PUT /cloud/config` |
| Delivery destination | `endpointConfig.management.event` |
| Communication type | Device to Cloud |
| Applies to | FXR60 / FXR90 |

## Configure Error Events

Set the management-event destination on the common management-event configuration page.

To configure error reporting, use `set_config` and set the required monitors under:

```text
READER-GATEWAY.managementEventConfig.errors
```

Boolean fields enable or disable that error monitor.

Fields such as `cpu`, `ram`, `flash`, and `userApp` use:

- `threshold` to set the error limit.
- `reportIntervalInSec` to set the minimum time between repeated reports.

Choose **MQTT — set_config** or **REST — PUT /cloud/config** from the **Example** dropdown in **Configuration Examples** below.

## Fields

| Field | Description | Default |
|---|---|---|
| `antenna` | Enable or disable antenna error reporting. | Enabled |
| `cpu` | CPU error threshold and report interval. | Enabled |
| `database` | Enable or disable database error reporting. | Enabled |
| `flash` | Flash error threshold and report interval. | Enabled |
| `ntp` | Enable or disable NTP synchronization error reporting. | Enabled |
| `radio` | Enable or disable radio error reporting. | Enabled |
| `radio_control` | Enable or disable Radio Control error reporting. | Enabled |
| `ram` | RAM error threshold and report interval. | Enabled |
| `reader_gateway` | Enable or disable Reader Gateway error reporting. | Enabled |
| `userApp` | User application error threshold and report interval. | Enabled |
| `threshold` | Limit above which the error is reported. | — |
| `reportIntervalInSec` | Minimum interval, in seconds, between repeated error reports. | — |
| `message` | Error message published in `data.message`. | — |

## Response Schema

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `error`. |
| `timestamp` | string | Event timestamp. |
| `component` | string | Component that published the error. |
| `eventNum` | number | Management event sequence number. |
| `data.message` | string | Human-readable error message. |
