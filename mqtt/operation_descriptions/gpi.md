## Description

The `gpi` event is published on the management channel when a GPI pin changes state between `HIGH` and `LOW`.

This event includes:

- The GPI pin that changed.
- The new state of the pin.

This event is useful when an external input changes state and the backend must react without polling the reader.

## Event Details

| Property | Value |
|---|---|
| MQTT event | `gpi` |
| Envelope `type` | `gpi` |
| Configuration path | `READER-GATEWAY.managementEventConfig.gpiEvents` |
| Configure using MQTT | `set_config` |
| Configure using REST | `PUT /cloud/config` |
| Delivery destination | `endpointConfig.management.event` |
| Communication type | Device to Cloud |
| Applies to | FXR60 / FXR90 |

## Configure GPI Events

Set the management-event destination on the common management-event configuration page.

To enable or disable GPI transition events, use `set_config` and set:

```text
READER-GATEWAY.managementEventConfig.gpiEvents
```

Set `gpiEvents` to:

- `true` to publish GPI events.
- `false` to stop publishing GPI events.

Choose **MQTT — set_config** or **REST — PUT /cloud/config** from the **Example** dropdown in **Configuration Examples** below.

## Fields

| Field | Description | Default |
|---|---|---|
| `gpiEvents` | Set to `true` to enable GPI transition events, or `false` to disable them. | `true` |
| `pin` | GPI pin number. Valid values are `1` through `4`. | — |
| `state` | New GPI pin state. Valid values are `HIGH` and `LOW`. | — |

## Response Schema

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `gpi`. |
| `timestamp` | string | Event timestamp. |
| `component` | string | Component that published the event. |
| `eventNum` | number | Management event sequence number. |
| `data.pin` | number | GPI pin number. Valid values are `1` through `4`. |
| `data.state` | string | New GPI pin state. Valid values are `HIGH` and `LOW`. |
