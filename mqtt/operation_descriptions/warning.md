## Description

The `warning` event is published on the management channel when the reader detects a warning-level condition.

Warning events are used for conditions that need attention before they become errors. Each warning event includes a human-readable message in `data.message`. The envelope `component` identifies the source of the warning.

This event includes:

- The component that reported the warning.
- The warning message in `data.message`.

This event is useful when the backend must receive CPU, RAM, flash, NTP, temperature, Radio Control, Reader Gateway, database, or user application warnings from the management event stream.

Warning Events are configured separately from Error Events.

## Event Details

| Property | Value |
|---|---|
| MQTT event | `warning` |
| Envelope `type` | `warning` |
| Configuration path | `READER-GATEWAY.managementEventConfig.warnings` |
| Configure using MQTT | `set_config` |
| Configure using REST | `PUT /cloud/config` |
| Delivery destination | `endpointConfig.management.event` |
| Communication type | Device to Cloud |
| Applies to | FXR60 / FXR90 |

## Configure Warning Events

Set the management-event destination on the common management-event configuration page.

To configure warning reporting, use `set_config` and set the required monitors under:

```text
READER-GATEWAY.managementEventConfig.warnings
```

Boolean fields enable or disable that warning monitor.

Fields such as `cpu`, `ram`, `flash`, and `userApp` use:

- `threshold` to set the warning limit.
- `reportIntervalInSec` to set the minimum time between repeated reports.

The `temperature` field uses:

- `ambient` for the ambient temperature threshold.
- `pa` for the PA temperature threshold.

Choose **MQTT — set_config** or **REST — PUT /cloud/config** from the **Example** dropdown in **Configuration Examples** below.

## Fields

| Field | Description | Default |
|---|---|---|
| `cpu` | CPU warning threshold and report interval. | Enabled |
| `database` | Enable or disable database warning reporting. | Enabled |
| `flash` | Flash warning threshold and report interval. | Enabled |
| `ntp` | Enable or disable NTP synchronization warning reporting. | Enabled |
| `radio_api` | Enable or disable radio API warning reporting. | Enabled |
| `radio_control` | Enable or disable Radio Control warning reporting. | Enabled |
| `ram` | RAM warning threshold and report interval. | Enabled |
| `reader_gateway` | Enable or disable Reader Gateway warning reporting. | Enabled |
| `temperature` | Ambient and PA temperature warning thresholds. | Enabled |
| `userApp` | User application warning threshold and report interval. | Enabled |
| `threshold` | Limit above which the warning is reported. | — |
| `reportIntervalInSec` | Minimum interval, in seconds, between repeated warning reports. | — |
| `message` | Warning message published in `data.message`. | — |

## Response Schema

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `warning`. |
| `timestamp` | string | Event timestamp. |
| `component` | string | Component that published the warning. |
| `eventNum` | number | Management event sequence number. |
| `data.message` | string | Human-readable warning message. |
