## Description

The `notification` event is published on the management channel when the connection status of a display peripheral changes.

All display events are published as notification events.

This event includes the updated connection status for one or more display peripherals:

- Monitor
- Keyboard
- Mouse
- Touch panel

This event is useful when the backend must react to peripheral connect or disconnect without polling `get_inputOutputDevices`.

## Event Details

| Property | Value |
|---|---|
| MQTT event | `notification_event` |
| Envelope `type` | `notification` |
| Configuration path | Not configurable in `managementEventConfig` |
| Trigger | Display peripheral connect or disconnect |
| Delivery destination | `endpointConfig.management.event` |
| Communication type | Device to Cloud |
| Applies to | FXR60 |

## How Notification Events Work

This event does not have a `managementEventConfig` enable or disable flag.

Set the management-event destination on the common management-event configuration page. When a display peripheral connects or disconnects, the reader automatically publishes a `notification` event on the management-event destination.

Use `get_inputOutputDevices` to query the current status of all display peripherals.

## Fields

| Field | Description |
|---|---|
| `data.monitor.status` | Monitor connection status. Values are `connected` and `disconnected`. |
| `data.keyboard.status` | Keyboard connection status. Values are `connected` and `disconnected`. |
| `data.mouse.status` | Mouse connection status. Values are `connected` and `disconnected`. |
| `data.touch.status` | Touch panel connection status. Values are `connected` and `disconnected`. |

Each event includes only the peripheral or peripherals whose status changed. Multiple peripherals can appear in the same event.

## Response Schema

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `notification`. |
| `timestamp` | string | Event timestamp. |
| `component` | string | Component that published the event. Typically `RG`. |
| `eventNum` | number | Management event sequence number. |
| `data.monitor.status` | string | Monitor connection status when the monitor changed. |
| `data.keyboard.status` | string | Keyboard connection status when the keyboard changed. |
| `data.mouse.status` | string | Mouse connection status when the mouse changed. |
| `data.touch.status` | string | Touch panel connection status when the touch panel changed. |
