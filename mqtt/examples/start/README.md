# `start`

REST: `PUT /cloud/start` → `cloud-start/`

Stable `command_id`: `req-start`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/start_Inventory.json` | request | `start_Inventory` | `cloud-start/PUT/start_Inventory.json` | Start RFID inventory (default) |
| `request/start_Inventory with AutoStart.json` | request | `start_Inventory with AutoStart` | `cloud-start/PUT/start_Inventory_with_AutoStart.json` | Start inventory with AutoStart |
| `request/start_Inventory with ImpinjGen2X.json` | request | `start_Inventory with ImpinjGen2X` | `cloud-start/PUT/start_Inventory_with_ImpinjGen2X.json` | Start inventory with Impinj Gen2X |
| `request/start_Global_BLE_only.json` | request | `start_Global_BLE_only` | `cloud-start/PUT/start_Global_BLE_only.json` | Global BLE only |
| `request/start_Global_RFID_only.json` | request | `start_Global_RFID_only` | `cloud-start/PUT/start_Global_RFID_only.json` | Global RFID only |
| `request/start_Global_BLE_and_RFID.json` | request | `start_Global_BLE_and_RFID` | `cloud-start/PUT/start_Global_BLE_and_RFID.json` | Global BLE and RFID |
| `request/start_Targeted.json` | request | `start_Targeted` | `cloud-start/PUT/start_Targeted.json` | Targeted per data endpoint |
| `response/success.json` | response | `success` | `—` | Command succeeded |
