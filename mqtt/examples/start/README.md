# `start`

REST: `PUT /cloud/start` → `cloud-start/`

Stable `command_id`: `req-start`

`scanType` is an array of `ble` and/or `rfid`.

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/start_Inventory.json` | request | `start_Inventory` | `cloud-start/PUT/start_Inventory.json` | Start RFID inventory (default) |
| `request/start_RFID_only.json` | request | `start_RFID_only` | `cloud-start/PUT/start_RFID_only.json` | Start RFID inventory (explicit) |
| `request/start_Inventory with AutoStart.json` | request | `start_Inventory with AutoStart` | `cloud-start/PUT/start_Inventory_with_AutoStart.json` | Start inventory with AutoStart |
| `request/start_Inventory with ImpinjGen2X.json` | request | `start_Inventory with ImpinjGen2X` | `cloud-start/PUT/start_Inventory_with_ImpinjGen2X.json` | Start inventory with Impinj Gen2X |
| `request/start_BLE_only.json` | request | `start_BLE_only` | `cloud-start/PUT/start_BLE_only.json` | Start BLE only |
| `request/start_BLE_and_RFID.json` | request | `start_BLE_and_RFID` | `cloud-start/PUT/start_BLE_and_RFID.json` | Start BLE and RFID |
| `response/success.json` | response | `success` | `—` | Command succeeded |
