## 1. Description

The `PUT /cloud/start` REST endpoint starts RFID inventory, BLE scanning, or both on the reader.

By default, an empty request body starts RFID inventory only. Use the `scanType` field to explicitly start BLE, RFID, or both together. Optional flags allow you to apply a previously saved Impinj Gen2X configuration or control whether the start state persists across reboots.

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

| Scan Type | Behavior |
|---|---|
| `rfid` (default) | Starts RFID inventory only. Tag read events stream on the reader's RFID data channel. |
| `ble` | Starts BLE scanning only. BLE advertisement events stream on the reader's BLE data channel. |
| `["ble", "rfid"]` | Starts both scanners in a single session. RFID and BLE events stream independently on their respective data channels. |

> Firmware requirement: BLE scanning — and with it the `scanType` field — is available from reader build **4.0.11** onward. On builds older than 4.0.11, `scanType` is not supported: omit it, and `PUT /cloud/start` starts RFID inventory only. Check the installed build with `GET /cloud/version` (`readerApplication`).

### Persistence Across Reboots

The `doNotPersistState` field controls whether the reader resumes RFID inventory automatically after a reboot or reconnect. It applies to RFID only and has no effect on BLE scanning — a BLE scan never auto-resumes.

| `doNotPersistState` | Behavior on Reboot or Reconnect |
|---|---|
| `false` (default) | The reader **remembers the running RFID inventory state** and automatically resumes it. |
| `true` | The running state is **not saved**. The reader stays Idle until `PUT /cloud/start` is called again. |

> Tip: Use `doNotPersistState: true` for one-time or debugging sessions where automatic resume after reboot is not desired.
