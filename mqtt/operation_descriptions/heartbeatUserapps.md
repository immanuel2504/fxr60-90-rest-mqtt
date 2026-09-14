## Description

The `userapps` section gives heartbeat information for installed user applications, such as running status, CPU usage, RAM usage, uptime, data-message counts, and buffer levels.

`data.userapps` is an array. Each installed user application is reported as one object in the array. If no user applications are installed, `userapps` is an empty array.

This section includes:

- Running status, CPU usage, RAM usage, and uptime for each installed user application.
- Number of data messages received and sent by each application.
- Incoming and outgoing data-buffer capacity remaining.

Use this section to:

- Check which user applications are installed and running.
- Monitor CPU and RAM usage for each user application.
- Track data-message flow between the application and Reader Gateway.
- Watch buffer levels before data is dropped.

This heartbeat section is not the same as a **User App Event**. A User App Event is a custom management event published by the application.

## Event Details

| Property | Value |
|---|---|
| MQTT event | `heartbeat` |
| Heartbeat section | `data.userapps` |
| Envelope `type` | `heartbeat` |
| Configuration path | `READER-GATEWAY.managementEventConfig.heartbeat.fields.userapps` |
| Configure using MQTT | `set_config` |
| Configure using REST | `PUT /cloud/config` |
| Delivery destination | `endpointConfig.management.event` |
| Applies to | FXR60 / FXR90 |

## Configure User App Fields

Set the management-event destination and heartbeat interval on the **Heartbeat** page.

To include User App fields in the heartbeat payload, use `set_config` and add the required field names under:

```text
READER-GATEWAY.managementEventConfig.heartbeat.fields.userapps
```

Fields not listed in the `userapps` array are omitted from the published heartbeat payload.

Choose **MQTT — set_config** or **REST — PUT /cloud/config** from the **Example** dropdown in **Configuration Examples** below.

## Parameters

| Field | Description | Default |
|---|---|---|
| `STATUS` | User application running status. | Enabled |
| `CPU` | User application CPU utilisation. | Enabled |
| `RAM` | User application RAM utilisation. | Enabled |
| `UPTIME` | User application uptime. | Enabled |
| `NUM_DATA_MESSAGES_RXED` | Number of data messages received by the application. | Enabled |
| `NUM_DATA_MESSAGES_TXED` | Number of data messages sent by the application to Reader Gateway. | Enabled |
| `INCOMING_DATA_BUFFER_PERCENTAGE_REMAINING` | Percentage of incoming buffer capacity remaining. | Enabled |
| `OUTGOING_DATA_BUFFER_PERCENTAGE_REMAINING` | Percentage of outgoing buffer capacity remaining. | Enabled |
