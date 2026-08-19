# `stop`

REST: `PUT /cloud/stop` → `cloud-stop/`

Stable `command_id`: `req-stop`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/stop_RFID_default.json` | request | `stop_RFID_default` | `cloud-stop/PUT/stop_RFID_default.json` |  |
| `request/stop_RFID_explicit.json` | request | `stop_RFID_explicit` | `cloud-stop/PUT/stop_RFID_explicit.json` |  |
| `request/stop_BLE_only.json` | request | `stop_BLE_only` | `cloud-stop/PUT/stop_BLE_only.json` |  |
| `request/stop_BLE_and_RFID.json` | request | `stop_BLE_and_RFID` | `cloud-stop/PUT/stop_BLE_and_RFID.json` | Global BLE and RFID |
| `request/stop_targeted_RFID.json` | request | `stop_targeted_RFID` | `cloud-stop/PUT/stop_targeted_RFID.json` | Targeted RFID on dataEndpoint1 and dataEndpoint2 |
| `request/stop_targeted_BLE.json` | request | `stop_targeted_BLE` | `cloud-stop/PUT/stop_targeted_BLE.json` | Targeted BLE on dataEndpoint1 and dataEndpoint2 |
| `request/stop_targeted_BLE_and_RFID.json` | request | `stop_targeted_BLE_and_RFID` | `cloud-stop/PUT/stop_targeted_BLE_and_RFID.json` | Targeted BLE and RFID on both endpoints |
| `request/stop_targeted_mixed.json` | request | `stop_targeted_mixed` | `cloud-stop/PUT/stop_targeted_mixed.json` | Targeted mixed — BLE on dataEndpoint1, RFID on dataEndpoint2 |
| `response/success.json` | response | `success` | `—` | Command succeeded |

