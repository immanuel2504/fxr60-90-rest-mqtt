## 1. Description

The `PUT /cloud/start` REST endpoint starts RFID inventory, BLE scanning, or both on the reader.

By default, an empty request body starts RFID inventory only. Use the flags below to start BLE, apply Gen2X, or control reboot persistence.

Use this endpoint to:

- Start RFID inventory using the currently configured operating mode
- Start BLE scanning using the currently configured BLE settings
- Start RFID and BLE scanning together in a single session
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
| Request fields | `scanType` (array of `ble` / `rfid`), `applyImpinjGen2X`, `doNotPersistState` |
| Firmware Requirement | BLE requires reader build **4.0.11** or later. On earlier builds the `scanType` field is not available. |

## 3. Before You Begin

Make sure the relevant scanners are configured before sending this request.

| What You Need | Details |
|---|---|
| HTTPS connectivity | The reader's HTTPS endpoint must be reachable and a valid bearer token must be included in the `Authorization` header of every request. |
| RFID configuration | Operating mode must be configured via `PUT /cloud/mode` (or left at the default) before starting RFID inventory. |
| BLE configuration | If starting BLE, configure BLE first with `PUT /cloud/bleConfig` and `ble.enable: true`. The full `ble` object is required. |
| Gen2X configuration | If using `applyImpinjGen2X: true`, save the Gen2X configuration with `PUT /cloud/impinjGen2X` first. `applyImpinjGen2X` cannot be combined with a BLE-only scan (`scanType: ["ble"]`). |

## 4. Supported flags

| Flag | What it does |
|---|---|
| `scanType` | Which scanners to start. Array of `ble` and/or `rfid`. |
| `applyImpinjGen2X` | Apply the Gen2X configuration saved with `PUT /cloud/impinjGen2X`. |
| `doNotPersistState` | Do not resume RFID inventory after reboot. RFID only — BLE never auto-resumes. |

### `scanType`

`scanType` is an **array** of scan types. Omit it for RFID-only (default). The array must be non-empty and must not contain duplicates.

```json
{ "scanType": ["ble"] }
```

| Request body | Behavior |
|---|---|
| omitted / `{}` | Starts RFID inventory only (default). |
| `["rfid"]` | Starts RFID inventory only. |
| `["ble"]` | Starts BLE scanning only. Requires BLE to be enabled first. |
| `["ble", "rfid"]` | Starts both scanners. |

> Firmware requirement: BLE scanning — and with it the `scanType` field — is available from reader build **4.0.11** onward. On builds older than 4.0.11, omit `scanType`; `PUT /cloud/start` starts RFID inventory only. Check the installed build with `GET /cloud/version` (`readerApplication`).

### `applyImpinjGen2X`

Send `applyImpinjGen2X: true` to apply the Gen2X features saved with `PUT /cloud/impinjGen2X` when RFID inventory starts.

| Value | Behavior |
|---|---|
| omitted / `false` | Start without applying Gen2X. A saved Gen2X config is ignored until this flag is true. |
| `true` | Apply the saved Gen2X config on **this** start only. After `PUT /cloud/stop`, send `true` again — activation does not persist across inventory sessions. Cannot be combined with `scanType: ["ble"]`. |

```json
{ "applyImpinjGen2X": true }
```

### Persistence across reboots (`doNotPersistState`)

`doNotPersistState` applies to RFID only.

| `doNotPersistState` | Behavior on reboot or reconnect |
|---|---|
| `false` (default) | The reader **remembers the running RFID inventory state** and automatically resumes it. |
| `true` | The running state is **not saved**. The reader stays idle until `PUT /cloud/start` is called again. |

> Use `doNotPersistState: true` for one-time or debugging sessions where automatic resume after reboot is not desired.
