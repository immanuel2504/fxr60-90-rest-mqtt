## Description

The `gpo` event is published on the management channel when a GPO pin changes state.

The change can come from a `set_gpo` request or from a mode-triggered output.

This event includes:

- The GPO pin that changed.
- The new state of the pin.

This event is useful when an external system must confirm output-state changes without polling the reader.

## Event Details

| Property | Value |
|---|---|
| MQTT event | `gpo` |
| Envelope `type` | `gpo` |
| Configuration path | `READER-GATEWAY.managementEventConfig.gpoEvents` |
| Configure using MQTT | `set_config` |
| Configure using REST | `PUT /cloud/config` |
| Delivery destination | `endpointConfig.management.event` |
| Communication type | Device to Cloud |
| Applies to | FXR60 / FXR90 |

## Configure GPO Events

Set the management-event destination on the common management-event configuration page.

To enable or disable GPO transition events, use `set_config` and set:

```text
READER-GATEWAY.managementEventConfig.gpoEvents
```

Set `gpoEvents` to:

- `true` to publish GPO events.
- `false` to stop publishing GPO events.

Choose **MQTT — set_config** or **REST — PUT /cloud/config** from the **Example** dropdown in **Configuration Examples** below.

## Fields

| Field | Description | Default |
|---|---|---|
| `gpoEvents` | Set to `true` to enable GPO transition events, or `false` to disable them. | `true` |
| `pin` | GPO pin number. Valid values are `1` through `4`. | — |
| `state` | New GPO pin state. Valid values are `HIGH` and `LOW`. | — |

## Response Schema

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `gpo`. |
| `timestamp` | string | Event timestamp. |
| `component` | string | Component that published the event. |
| `eventNum` | number | Management event sequence number. |
| `data.pin` | number | GPO pin number. Valid values are `1` through `4`. |
| `data.state` | string | New GPO pin state. Valid values are `HIGH` and `LOW`. |
