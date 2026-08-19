## 1. Description

The `PUT /cloud/start` REST endpoint starts RFID inventory, BLE scanning, or both on the reader.

By default, an empty request body starts RFID inventory only. Use the `scanType` field to start BLE, RFID, or both.

`scanType` can be:

- An **array** — global start on every data endpoint
- An **object** — targeted start per data endpoint (`dataEndpoint1`, `dataEndpoint2`)

If `scanType` is omitted or empty, the reader starts RFID only.

Use this endpoint to:

- Start RFID inventory using the currently configured operating mode
- Start BLE scanning using the currently configured BLE settings
- Start RFID and BLE scanning together in a single inventory session
- Apply a previously saved Impinj Gen2X configuration when starting RFID inventory
- Control whether the reader automatically resumes scanning after reboot

## 2. Endpoint Details

| Property | Value |
|---|---|
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

## 4. What Happens After Start

Once the `PUT /cloud/start` request succeeds, the reader transitions from **Idle** to **Running**. Two important behaviors govern the running session.

### Scan Type

The `scanType` field determines which scanners run and where the data is published.

**Global start** — send an array. The same scan types apply to every data endpoint.

| Scan Type | Behavior |
|---|---|
| omitted / `{}` | Starts RFID inventory only (default). |
| `["rfid"]` | Starts RFID inventory only. |
| `["ble"]` | Starts BLE scanning only. |
| `["ble", "rfid"]` | Starts both scanners. |

**Targeted start** — send an object. Keys are data endpoints; values are the scan types for that endpoint.

| `scanType` | Behavior |
|---|---|
| `{ "dataEndpoint1": ["rfid"], "dataEndpoint2": ["rfid"] }` | RFID on both endpoints. |
| `{ "dataEndpoint1": ["ble"], "dataEndpoint2": ["ble"] }` | BLE on both endpoints. |
| `{ "dataEndpoint1": ["ble", "rfid"], "dataEndpoint2": ["ble", "rfid"] }` | BLE and RFID on both endpoints. |
| `{ "dataEndpoint1": ["ble"], "dataEndpoint2": ["rfid"] }` | BLE on endpoint 1, RFID on endpoint 2. |

> Firmware requirement: BLE scanning — and with it the `scanType` field — is available from reader build **4.0.11** onward. On builds older than 4.0.11, `scanType` is not supported: omit it, and `PUT /cloud/start` starts RFID inventory only. Check the installed build with `GET /cloud/version` (`readerApplication`).

### Persistence Across Reboots

The `doNotPersistState` field controls whether the reader resumes RFID inventory automatically after a reboot or reconnect. It applies to RFID only and has no effect on BLE scanning — a BLE scan never auto-resumes.

| `doNotPersistState` | Behavior on Reboot or Reconnect |
|---|---|
| `false` (default) | The reader **remembers the running RFID inventory state** and automatically resumes it. |
| `true` | The running state is **not saved**. The reader stays Idle until `PUT /cloud/start` is called again. |

> Tip: Use `doNotPersistState: true` for one-time or debugging sessions where automatic resume after reboot is not desired.
