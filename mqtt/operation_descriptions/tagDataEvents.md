## Description

The `tagDataEvents` event is the common data-event envelope used for RFID tag reads.

The `type` field identifies the operating mode that produced the event. The `data` payload changes based on the `type`.

This page focuses on RFID tag-read payloads for `SIMPLE`, `INVENTORY`, `PORTAL`, `CONVEYOR`, and `CUSTOM` modes.

> **Note:** `BLE_DATA` can also use the same data-event channel, but BLE payload details are covered separately in [BLE Data Events](ble_data_events.md).

This event includes:

- The operating mode `type` that produced the event.
- The event `timestamp`.
- A `data` object that contains the tag-read payload.

This event is useful when RFID tag reads from different operating modes are published through the same configured data endpoint.

## Event Details

| Property | Value |
|---|---|
| Event name | `tagDataEvents` |
| Envelope `type` | `SIMPLE`, `INVENTORY`, `PORTAL`, `CONVEYOR`, or `CUSTOM` |
| Delivery destination | `endpointConfig.data.event` |
| Communication type | Device to Cloud |
| Trigger condition | Published when the reader reports tag reads during an active operating mode |
| Applies to | FXR60 / FXR90 |

## How Tag Data Events Work

The reader publishes `tagDataEvents` automatically to the configured data endpoint while inventory is active.

No separate event command is required after inventory starts. Configure the operating mode, start inventory, and consume the tag data from the configured data endpoint.

The `type` field is not a constant. Use `type` to decide how to parse the `data` object.

| `type` | Default `data` payload | Description |
|---|---|---|
| `SIMPLE` | `eventNum`, `format`, `idHex` | Basic RFID tag-read payload. |
| `INVENTORY` | `antenna`, `eventNum`, `format`, `idHex`, `peakRssi`, `reads` | Richest default RFID payload. |
| `CONVEYOR` | `antenna`, `eventNum`, `format`, `idHex` | Conveyor-mode RFID payload. |
| `CUSTOM` | `eventNum`, `format`, `idHex` | Custom-mode payload. Additional fields depend on `tagMetaData` and access operations. |
| `PORTAL` | No tag data until the GPI start trigger is active | Portal mode publishes tag data only after the configured GPI trigger starts the read cycle. |

## Configure Tag Data Events

Set the data-event destination before starting inventory.

Configure the destination under:

```text
endpointConfig.data.event
```

After the destination is configured:

1. Configure the required operating mode by using `set_mode`.
2. Start inventory by using `start`.
3. Read the published tag data from the configured data endpoint.

### Choose which fields appear in `data`

The default `data` fields depend on the operating mode. To include additional fields, configure them in `set_mode`.

Use:

- `tagMetaData` to request optional tag-read fields such as antenna, RSSI, phase, channel, PC, CRC, TID, and USER.
- `accesses` to run access operations. Results appear in `data.accessResults`.

| `tagMetaData` value | Published field in `data` |
|---|---|
| `ANTENNA` | `antenna` |
| `RSSI` | `peakRssi` |
| `SEEN_COUNT` | `reads` |
| `CHANNEL` | `channel` |
| `PHASE` | `phase` |
| `PC` | `PC` |
| `CRC` | `CRC` |
| `TID` | `TID` |
| `USER` | `USER` |

Mode rules that affect the payload:

- `SIMPLE` — do not send `tagMetaData`. The payload stays `eventNum`, `format`, and `idHex`.
- `INVENTORY` — richest default payload. `accesses` is not allowed.
- `CUSTOM` — default payload matches `SIMPLE`. Use `tagMetaData` and `accesses` to add fields.
- `PORTAL` and `CONVEYOR` — default fields are mode-specific. Use `tagMetaData` to request additional fields where supported.

See [set_mode](set_mode.md) for the full operating-mode configuration.
## Fields

| Field | Description |
|---|---|
| `type` | Operating mode that produced the event. |
| `timestamp` | Event timestamp. |
| `data` | Tag-read payload. The structure depends on `type`. |
| `data.eventNum` | RFID tag-read event number. |
| `data.format` | Format of the tag identifier. Example: `epc`. |
| `data.idHex` | EPC value of the tag as a hexadecimal string. |
| `data.antenna` | Antenna port on which the tag was read. |
| `data.peakRssi` | Peak RSSI value for the tag read. |
| `data.reads` | Number of reads since the previous report. |
| `data.TID` | TID memory-bank value, when requested. |
| `data.USER` | USER memory-bank value, when requested. This can contain an error string when user memory is not available. |
| `data.PC` | PC bits of the inventoried tag, when requested. |
| `data.CRC` | CRC bits of the inventoried tag, when requested. |
| `data.channel` | RF channel used for the read. Included only when individual tag reads are reported. |
| `data.phase` | Phase angle for the read. Included only when individual tag reads are reported. |
| `data.accessResults` | Results of configured access operations. |

## Response Schema

| Field | Type | Description |
|---|---|---|
| `type` | string | Operating mode that produced the event. Valid values covered on this page are `SIMPLE`, `INVENTORY`, `PORTAL`, `CONVEYOR`, and `CUSTOM`. |
| `timestamp` | string | Event timestamp. |
| `data` | object | Tag-read payload. The structure depends on `type`. |
| `data.eventNum` | number | RFID tag-read event number. |
| `data.format` | string | Format of the tag identifier. |
| `data.idHex` | string | EPC value of the tag as a hexadecimal string. |
| `data.antenna` | number | Antenna port on which the tag was read. |
| `data.peakRssi` | number | Peak RSSI value. |
| `data.reads` | number | Number of reads since the previous report. |
| `data.accessResults` | array | Results of configured access operations. |
