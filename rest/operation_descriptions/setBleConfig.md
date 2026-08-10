## 1. Description

The `PUT /cloud/ble-config` REST endpoint configures the Bluetooth Low Energy (BLE) scanner on the reader.

This endpoint allows you to configure:

- BLE scanner enable or disable through `ble.enable`
- Scan interval through `ble.scanIntervalSec`
- Cross-protocol RSSI and service UUID filters through `ble.additionalFilters`
- iBeacon filters through `ble.protocols.iBeacon`
- AltBeacon filters through `ble.protocols.altBeacon`
- Eddystone filters through `ble.protocols.eddystone`
- Generic BLE device filters through `ble.protocols.generic`

Use this endpoint to:

- Activate or deactivate BLE scanning
- Tune how frequently the reader collects BLE scan results
- Filter out weak or irrelevant BLE advertisements using RSSI or service UUID
- Capture only specific beacon types or devices from the BLE environment
- Prepare BLE configuration before starting a combined RFID and BLE inventory

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | BLE Configuration Update |
| REST Endpoint | `PUT /cloud/ble-config` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `ble.enable` |
| Supported BLE Protocols | iBeacon, AltBeacon, Eddystone (`URL`, `UID`, `EID`, `TLM`), Generic |
| Firmware Requirement | BLE requires reader build **4.0.11** or later. On earlier builds this endpoint is not available. |
| Supported Address Types | `public`, `random` |
| RSSI Filter Range | `-127` to `0` dBm |
| Scan Interval Minimum | 1 second |

## 3. Before You Begin

Decide which BLE behavior you need to configure before sending this request. A minimal request only needs `ble.enable`; additional fields refine which beacons are captured.

| What You Need | Details |
|---|---|
| Enable decision | `ble.enable` is required in every request. Set to `true` to activate scanning, or `false` to disable it. |
| Scan interval | How often the reader collects BLE scan results (`scanIntervalSec`). Minimum value is `1` second. Shorter intervals increase responsiveness; longer intervals reduce data volume. |
| RSSI threshold | Set `additionalFilters.rssi` to drop weak advertisements. Range is `-127` to `0` dBm; values closer to zero indicate stronger signals. |
| Service UUID filters | Prepare 16-bit (`serviceUuids16`) or 128-bit (`serviceUuids128`) UUID lists to filter by advertised services. |
| iBeacon details | UUID, major, minor, and txPower values for each iBeacon filter entry. |
| AltBeacon details | Manufacturer ID, beacon ID, major, minor, and refRssi for each AltBeacon filter entry. |
| Eddystone frame type | Choose `URL`, `UID`, `EID`, or `TLM` and supply the corresponding fields (`url`, `namespace`/`instance`, `ephemeralId`). |
| Generic BLE device | Bluetooth MAC address, address type (`public`/`random`), device name, or alias for each generic filter entry. |
| Activation | Saving this configuration does not start BLE scanning. Send `PUT /cloud/start` with `scanType: ["ble"]` to begin scanning. |
