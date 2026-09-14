## Description

The `system` section gives reader system heartbeat information, such as CPU usage, RAM usage, flash status, system time, temperature, uptime, GPI/GPO state, power source, MAC address, and host name.

This section includes:

- CPU, RAM, flash, and uptime for the reader.
- Reader system time and NTP status.
- Ambient and PA temperature.
- Current GPI and GPO pin states.
- Power source and power negotiation status.
- Reader MAC address and host name.

Use this section to:

- Monitor reader health and resource usage.
- Check reader temperature and memory usage.
- Read current GPI and GPO states from the heartbeat payload.
- Identify the reader using `hostName` and `macAddress`.
- Compare the envelope `timestamp` with the reader clock in `systemtime`.

## Event Details

| Property | Value |
|---|---|
| MQTT event | `heartbeat` |
| Heartbeat section | `data.system` |
| Envelope `type` | `heartbeat` |
| Configuration path | `READER-GATEWAY.managementEventConfig.heartbeat.fields.system` |
| Configure using MQTT | `set_config` |
| Configure using REST | `PUT /cloud/config` |
| Delivery destination | `endpointConfig.management.event` |
| Applies to | FXR60 / FXR90 |

## Configure System Fields

Set the management-event destination and heartbeat interval on the **Heartbeat** page.

To include System fields in the heartbeat payload, use `set_config` and add the required field names under:

```text
READER-GATEWAY.managementEventConfig.heartbeat.fields.system
```

Fields not listed in the `system` array are omitted from the published heartbeat payload.

Choose **MQTT — set_config** or **REST — PUT /cloud/config** from the **Example** dropdown in **Configuration Examples** below.

## Parameters

| Field | Description | Default |
|---|---|---|
| `CPU` | Reader CPU utilisation. | Enabled |
| `FLASH` | Flash storage information. This value can be `null`. | Enabled |
| `NTP` | NTP synchronisation status. | Enabled |
| `RAM` | Reader RAM information. | Enabled |
| `SYSTEMTIME` | Reader system time. This is separate from the envelope `timestamp`. | Enabled |
| `TEMPERATURE` | Reader temperature readings, such as ambient and PA temperature. | Enabled |
| `UPTIME` | Reader uptime. | Enabled |
| `GPO` | Current GPO pin states. | Enabled |
| `GPI` | Current GPI pin states. | Enabled |
| `POWER_NEGOTIATION` | Current power negotiation status. | Enabled |
| `POWER_SOURCE` | Current reader power source. | Enabled |
| `MAC_ADDRESS` | Reader MAC address. | Enabled |
| `HOSTNAME` | Reader host name. | Enabled |
