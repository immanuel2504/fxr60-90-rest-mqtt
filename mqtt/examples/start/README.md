# `start`

REST: `PUT /cloud/start` → `cloud-start/`

Stable `command_id`: `req-start`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/start_Inventory.json` | request | `start_Inventory` | `cloud-start/PUT/start_Inventory.json` |  |
| `request/start_Inventory with AutoStart.json` | request | `start_Inventory with AutoStart` | `cloud-start/PUT/start_Inventory_with_AutoStart.json` |  |
| `request/start_Inventory with ImpinjGen2X.json` | request | `start_Inventory with ImpinjGen2X` | `cloud-start/PUT/start_Inventory_with_ImpinjGen2X.json` |  |
| `request/start_BLE_only.json` | request | `start_BLE_only` | `cloud-start/PUT/start_BLE_only.json` |  |
| `request/start_RFID_only.json` | request | `start_RFID_only` | `cloud-start/PUT/start_RFID_only.json` |  |
| `request/start_BLE_and_RFID.json` | request | `start_BLE_and_RFID` | `cloud-start/PUT/start_BLE_and_RFID.json` | Global BLE and RFID |
| `request/start_targeted_RFID.json` | request | `start_targeted_RFID` | `cloud-start/PUT/start_targeted_RFID.json` | Targeted RFID on dataEndpoint1 and dataEndpoint2 |
| `request/start_targeted_BLE.json` | request | `start_targeted_BLE` | `cloud-start/PUT/start_targeted_BLE.json` | Targeted BLE on dataEndpoint1 and dataEndpoint2 |
| `request/start_targeted_BLE_and_RFID.json` | request | `start_targeted_BLE_and_RFID` | `cloud-start/PUT/start_targeted_BLE_and_RFID.json` | Targeted BLE and RFID on both endpoints |
| `request/start_targeted_mixed.json` | request | `start_targeted_mixed` | `cloud-start/PUT/start_targeted_mixed.json` | Targeted mixed — BLE on dataEndpoint1, RFID on dataEndpoint2 |
| `response/success.json` | response | `success` | `—` | Command succeeded |

