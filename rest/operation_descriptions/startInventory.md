## 1. Description

The `PUT /cloud/start` REST endpoint starts RFID inventory, BLE scanning, or both on the reader.

By default, an empty request body **starts RFID inventory only**. BLE does **not** autostart — you must include `scanType` with `"ble"` (and configure BLE first) to start BLE scanning.

Use this endpoint to:

- Start RFID inventory using the currently configured operating mode
- Start BLE scanning when explicitly requested in `scanType`
- Start RFID and BLE together in a single session
- Apply a previously saved Impinj Gen2X configuration when starting RFID inventory
- Control whether the reader automatically resumes RFID inventory after reboot

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `start` |
| Pattern Name | Scan Control - Start |
| REST Endpoint | `PUT /cloud/start` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Supported flags | `scanType`, `applyImpinjGen2X`, `doNotPersistState` |
| Firmware Requirement | BLE requires reader build **4.0.11** or later. On earlier builds the `scanType` field is not available. |

## 3. Supported flags (summary)

| Flag | Type | Purpose |
|---|---|---|
| `scanType` | array **or** object (MQTT targeted) | Choose which scan types to start — globally or per data endpoint |
| `applyImpinjGen2X` | boolean | Apply the Gen2X configuration saved with `PUT /cloud/impinjGen2X` when RFID inventory starts |
| `doNotPersistState` | boolean | Control RFID auto-resume after reboot (RFID only) |

## 4. Before You Begin

| What You Need | Details |
|---|---|
| Bearer token | Include a valid bearer token in the `Authorization` header (`Authorization: Bearer <token>`). |
| RFID mode | Configure the operating mode with `PUT /cloud/mode` before starting RFID, or use the reader default. |
| BLE (optional) | To start BLE, configure `PUT /cloud/bleConfig` first with `ble.enable: true`, then include `"ble"` in `scanType`. |
| Gen2X (optional) | To apply Gen2X on start, save the configuration with `PUT /cloud/impinjGen2X` and send `applyImpinjGen2X: true`. Cannot combine with BLE-only start. |

## 5. `scanType`

Controls which scan types start. Omit `scanType` for RFID-only (default).

### Global start (REST and MQTT)

`scanType` is an **array** of `"ble"` and/or `"rfid"`. The array must be non-empty and must not contain duplicates.

```json
{ "scanType": ["ble"] }
```

| Request body | Behavior |
|---|---|
| omitted / `{}` | Starts **RFID inventory only** (default). BLE is not started. |
| `["rfid"]` | Starts RFID inventory only. |
| `["ble"]` | Starts BLE scanning only. Requires BLE to be enabled in `PUT /cloud/bleConfig`. |
| `["ble", "rfid"]` | Starts both. |

**Firmware requirement:** BLE scanning — and with it the `scanType` field — is available from reader build **4.0.11** onward. On builds older than 4.0.11, omit `scanType`; `PUT /cloud/start` starts RFID inventory only. Check the installed build with `GET /cloud/version` (`readerApplication`).

### Targeted start (MQTT only)

When multiple data endpoints are configured, MQTT accepts `scanType` as an **object** that maps each data-endpoint connection name to the scan types to start on that endpoint:

```json
{
  "scanType": {
    "dataEndpoint1": ["ble", "rfid"],
    "dataEndpoint2": ["rfid"]
  }
}
```

Each key is a connection `name` from `endpointConfig.data.event.connections`. Each value is an array of `"ble"` and/or `"rfid"` for that endpoint only.

## 6. `applyImpinjGen2X`

Separate from `scanType`. Send `applyImpinjGen2X: true` to apply the Gen2X features saved with `PUT /cloud/impinjGen2X` when RFID inventory starts.

| Value | Behavior |
|---|---|
| omitted / `false` | Start without applying Gen2X. A saved Gen2X config is ignored until this flag is true. |
| `true` | Apply the saved Gen2X config on **this** start only. After `PUT /cloud/stop`, send `true` again — activation does not persist across inventory sessions. Cannot be combined with `scanType: ["ble"]`. |

```json
{ "applyImpinjGen2X": true }
```

## 7. Persistence across reboots (`doNotPersistState`)

`doNotPersistState` applies to **RFID only**. BLE never auto-resumes after reboot.

| `doNotPersistState` | Behavior on reboot or reconnect |
|---|---|
| `false` (default) | The reader remembers the running RFID inventory state and automatically resumes it. |
| `true` | The running state is not saved. The reader stays idle until `PUT /cloud/start` is called again. |

Use `doNotPersistState: true` for one-time or debugging sessions where automatic resume after reboot is not desired.
