## Description

The `userapp_event` event allows an installed user application to publish a custom asynchronous message on the management channel.

The envelope `type` is `userapp`, and the envelope `component` contains the user application name.

This event includes:

- The application name in `component`.
- The application-defined message in `data.event`.

This event is useful when an installed user application must publish its own management notification without polling.

This event is not the `userapps` array inside a heartbeat. The `userapps` heartbeat section reports application health and statistics, but `userapp_event` reports a custom message published by the application.

## Event Details

| Property | Value |
|---|---|
| MQTT event | `userapp_event` |
| Envelope `type` | `userapp` |
| Configuration path | `READER-GATEWAY.managementEventConfig.userappEvents` |
| Configure using MQTT | `set_config` |
| Configure using REST | `PUT /cloud/config` |
| Delivery destination | `endpointConfig.management.event` |
| Communication type | Device to Cloud |
| Applies to | FXR60 / FXR90 |

## Configure User App Events

Set the management-event destination on the common management-event configuration page.

To enable or disable custom events from installed user applications, use `set_config` and set:

```text
READER-GATEWAY.managementEventConfig.userappEvents
```

Set `userappEvents` to:

- `true` to publish custom user application events.
- `false` to stop publishing custom user application events.

Choose **MQTT — set_config** or **REST — PUT /cloud/config** from the **Example** dropdown in **Configuration Examples** below.

## Fields

| Field | Description | Default |
|---|---|---|
| `userappEvents` | Set to `true` to enable custom user application events, or `false` to disable them. | `true` |
| `component` | Name of the user application that published the event. | — |
| `event` | Application-defined event message. | — |

## Response Schema

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `userapp`. |
| `timestamp` | string | Event timestamp. |
| `component` | string | Name of the user application that published the event. |
| `eventNum` | number | Management event sequence number. |
| `data.event` | string | Application-defined event message. |
