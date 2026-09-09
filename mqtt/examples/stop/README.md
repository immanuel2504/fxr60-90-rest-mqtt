# `stop`

REST: `PUT /cloud/stop` → `cloud-stop/`

Stable `command_id`: `req-stop`

`scanType` is an array of `ble` and/or `rfid`.

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/stop_RFID_default.json` | request | `stop_RFID_default` | `cloud-stop/PUT/stop_RFID_default.json` | Stop RFID (default) |
| `request/stop_RFID_explicit.json` | request | `stop_RFID_explicit` | `cloud-stop/PUT/stop_RFID_explicit.json` | Stop RFID (explicit) |
| `request/stop_BLE_only.json` | request | `stop_BLE_only` | `cloud-stop/PUT/stop_BLE_only.json` | Stop BLE only |
| `request/stop_BLE_and_RFID.json` | request | `stop_BLE_and_RFID` | `cloud-stop/PUT/stop_BLE_and_RFID.json` | Stop BLE and RFID |
| `response/success.json` | response | `success` | `—` | Command succeeded |
