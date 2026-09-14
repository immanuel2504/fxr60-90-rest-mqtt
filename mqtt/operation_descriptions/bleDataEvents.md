## Description

The `ble_data_events` event is a `BLE_DATA` payload published on the configured data endpoint.

BLE data uses the same data-event channel as RFID tag reads, but the payload structure is different. Use the `type` field to separate BLE events from RFID tag-data events.

BLE `data` field names are capitalized, such as `Address`, `RSSI`, and `Alias`.

This event includes:

- The `BLE_DATA` event type.
- The event `timestamp`.
- The top-level `eventNum`.
- A `data` object that contains BLE device or beacon information.

This event is useful when BLE advertisements must be collected from the reader and sent to the same backend data channel.

## Event Details

| Property | Value |
|---|---|
| Event name | `ble_data_events` |
| Envelope `type` | `BLE_DATA` |
| Delivery destination | `endpointConfig.data.event` |
| Communication type | Device to Cloud |
| Trigger condition | Published while BLE scanning is running |
| Applies to | FXR60 / FXR90 |

## How BLE Data Events Work

The reader publishes `BLE_DATA` events when BLE scanning is enabled and the `start` command includes BLE.

Consumers on the data endpoint must check the `type` field. When `type` is `BLE_DATA`, parse the payload as BLE data.

Unlike RFID tag-data events, BLE events carry `eventNum` at the top level.

The `beaconType` field identifies the BLE beacon format.

| `beaconType` | Protocol object |
|---|---|
| `IBEACON` | `iBeacon` |
| `ALTBEACON` | `altBeacon` |
| `EDDYSTONE_URL` | `eddystone` |
| `EDDYSTONE_UID` | `eddystone` |
| `EDDYSTONE_EID` | `eddystone` |
| `EDDYSTONE_TLM` | `eddystone` |
| `GENERIC_BLE` | No protocol-specific object. Base BLE fields only. |

## Configure BLE Data Events

Set the data-event destination before starting BLE scanning.

Configure the destination under:

```text
endpointConfig.data.event
```

After the data endpoint is configured:

1. Configure BLE scanning by using `set_bleConfig`.
2. Set `ble.enable` to `true`.
3. Configure the required BLE protocols and filters.
4. Start BLE scanning by using `start` with `scanType: ["ble"]`.

Example start payload:

```json
{
  "scanType": [
    "ble"
  ]
}
```

To start both RFID inventory and BLE scanning, use:

```json
{
  "scanType": [
    "ble",
    "rfid"
  ]
}
```

See [set_bleConfig](set_bleConfig.md) for BLE scan configuration and [start](start.md) for scan start options.

## Fields

| Field | Description |
|---|---|
| `type` | Always `BLE_DATA` for BLE data events. |
| `timestamp` | Event timestamp. |
| `eventNum` | BLE event sequence number. This field is at the top level. |
| `data` | BLE payload object. |
| `data.Adapter` | BLE adapter path. |
| `data.Address` | BLE device address. |
| `data.AddressType` | BLE address type, such as `public` or `random`. |
| `data.Alias` | BLE device alias. |
| `data.RSSI` | Received signal strength indicator. |
| `data.UUIDs` | List of advertised UUIDs. |
| `data.Connected` | Indicates whether the BLE device is connected. |
| `data.Paired` | Indicates whether the BLE device is paired. |
| `data.Trusted` | Indicates whether the BLE device is trusted. |
| `data.Blocked` | Indicates whether the BLE device is blocked. |
| `data.ServicesResolved` | Indicates whether BLE services are resolved. |
| `data.ManufacturerData` | Manufacturer-specific advertisement data, when present. |
| `data.beaconType` | BLE beacon type. |
| `data.iBeacon` | iBeacon protocol details, when `beaconType` is `IBEACON`. |
| `data.altBeacon` | AltBeacon protocol details, when `beaconType` is `ALTBEACON`. |
| `data.eddystone` | Eddystone protocol details, when `beaconType` is an Eddystone type. |

## Response Schema

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `BLE_DATA`. |
| `timestamp` | string | Event timestamp. |
| `eventNum` | number | BLE event sequence number. |
| `data` | object | BLE device or beacon payload. |
| `data.Adapter` | string | BLE adapter path. |
| `data.Address` | string | BLE device address. |
| `data.AddressType` | string | BLE address type. |
| `data.Alias` | string | BLE device alias. |
| `data.RSSI` | number | Received signal strength indicator. |
| `data.UUIDs` | array | Advertised UUIDs. |
| `data.beaconType` | string | BLE beacon type. |
| `data.iBeacon` | object | iBeacon details, when present. |
| `data.altBeacon` | object | AltBeacon details, when present. |
| `data.eddystone` | object | Eddystone details, when present. |
