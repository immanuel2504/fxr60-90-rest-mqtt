# `stop`

REST: `PUT /cloud/stop` → `cloud-stop/`

Stable `command_id`: `req-stop`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/stop_RFID_default.json` | request | `stop_RFID_default` | `cloud-stop/PUT/stop_RFID_default.json` | Stop RFID (default) |
| `request/stop_Global_RFID_only.json` | request | `stop_Global_RFID_only` | `cloud-stop/PUT/stop_Global_RFID_only.json` | Global RFID only |
| `request/stop_Global_BLE_only.json` | request | `stop_Global_BLE_only` | `cloud-stop/PUT/stop_Global_BLE_only.json` | Global BLE only |
| `request/stop_Global_BLE_and_RFID.json` | request | `stop_Global_BLE_and_RFID` | `cloud-stop/PUT/stop_Global_BLE_and_RFID.json` | Global BLE and RFID |
| `request/stop_Targeted.json` | request | `stop_Targeted` | `cloud-stop/PUT/stop_Targeted.json` | Targeted per data endpoint |
| `response/success.json` | response | `success` | `—` | Command succeeded |
