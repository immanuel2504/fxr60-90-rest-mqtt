## 1. Description

The `PUT /cloud/start` REST endpoint starts RFID inventory, BLE scanning, or both on the reader.

By default, an empty request body starts RFID inventory only. Use the flags below to start BLE, apply Gen2X, or control reboot persistence.

Use this endpoint to:

- Start RFID inventory using the currently configured operating mode
- Start BLE scanning using the currently configured BLE settings
- Start RFID and BLE scanning together in a single inventory session
- Apply a previously saved Impinj Gen2X configuration when starting RFID inventory
- Control whether the reader automatically resumes scanning after reboot

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
| Supported Scan Types | `rfid`, `ble`, or both combined |
| Firmware Requirement | BLE requires reader build **4.0.11** or later. On earlier builds the `scanType` field is not available. |

## 3. Before You Begin

Make sure the relevant scanners are configured before sending this request.

| What You Need | Details |
|---|---|
| HTTPS connectivity | The reader's HTTPS endpoint must be reachable and a valid bearer token must be included in the `Authorization` header of every request. |
| RFID configuration | Operating mode must be configured via `PUT /cloud/mode` (or default) before starting RFID inventory. |
| BLE configuration | If starting BLE, the BLE scanner must be configured via `PUT /cloud/bleConfig` with `ble.enable: true`. |
| Gen2X configuration | If using `applyImpinjGen2X: true`, the Gen2X configuration must be saved via `PUT /cloud/impinjGen2X` beforehand. `applyImpinjGen2X` cannot be combined with a BLE-only scan (`scanType: ["ble"]`). |

## 4. Supported flags

The start body may include these flags. Each is explained below.

| Flag | What it does |
|---|---|
| `scanType` | Which scanners to start, and on which data endpoints. |
| `applyImpinjGen2X` | Apply the Gen2X configuration saved with `PUT /cloud/impinjGen2X`. |
| `doNotPersistState` | Do not resume RFID inventory after reboot. |

### `scanType`

`scanType` is either:

- An **array** — **global start**. The same scan types apply to **every** data endpoint.
- An **object** — **targeted start**. Keys are data endpoint names; values are the scan types for that endpoint.

**Global start** (array). Example — BLE on all endpoints:

```json
{ "scanType": ["ble"] }
```

| Scan Type | Behavior |
|---|---|
| omitted / `{}` | Starts RFID inventory only (default). |
| `["rfid"]` | Starts RFID inventory only, on every data endpoint. |
| `["ble"]` | Starts BLE scanning only, on every data endpoint. |
| `["ble", "rfid"]` | Starts both scanners, on every data endpoint. |

**Targeted start** (object with data-endpoint fields):

```json
{ "scanType": { "dataEndpoint1": ["ble", "rfid"], "dataEndpoint2": ["rfid"] } }
```

> Firmware requirement: BLE scanning — and with it the `scanType` field — is available from reader build **4.0.11** onward. On builds older than 4.0.11, `scanType` is not supported: omit it, and `PUT /cloud/start` starts RFID inventory only. Check the installed build with `GET /cloud/version` (`readerApplication`).

### `applyImpinjGen2X`

Send `applyImpinjGen2X: true` to apply the Gen2X features saved with `PUT /cloud/impinjGen2X` when RFID inventory starts.

| Value | Behavior |
|---|---|
| omitted / `false` | Start without applying Gen2X. |
| `true` | Apply saved Gen2X on this start. Save the config first with `PUT /cloud/impinjGen2X`. Cannot be combined with a BLE-only scan (`scanType: ["ble"]`). |

```json
{ "applyImpinjGen2X": true }
```

### Persistence across reboots (`doNotPersistState`)

The `doNotPersistState` field controls whether the reader resumes RFID inventory automatically after a reboot or reconnect. It applies to RFID only and has no effect on BLE scanning — a BLE scan never auto-resumes.

| `doNotPersistState` | Behavior on reboot or reconnect |
|---|---|
| `false` (default) | The reader **remembers the running RFID inventory state** and automatically resumes it. |
| `true` | The running state is **not saved**. The reader stays Idle until `PUT /cloud/start` is called again. |

> Tip: Use `doNotPersistState: true` for one-time or debugging sessions where automatic resume after reboot is not desired.
