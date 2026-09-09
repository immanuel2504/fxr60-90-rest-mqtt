# `set_bleConfig`

REST: `PUT /cloud/bleConfig` → `cloud-bleconfig/`

MQTT command key: `set_bleConfig`

Stable `command_id`: `req-set-bleConfig`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/enable_ble.json` | request | `enable_ble` | `cloud-bleconfig/PUT/enable_ble.json` | `ble.enable` true, interval `0` |
| `request/enable_with_interval.json` | request | `enable_with_interval` | `cloud-bleconfig/PUT/enable_with_interval.json` | Interval `5` |
| `request/enable_with_rssi_filter.json` | request | `enable_with_rssi_filter` | `cloud-bleconfig/PUT/enable_with_rssi_filter.json` | `additionalFilters.rssi` `-70` |
| `request/enable_with_protocols.json` | request | `enable_with_protocols` | `cloud-bleconfig/PUT/enable_with_protocols.json` | All protocols and filters |
| `request/disable_ble.json` | request | `disable_ble` | `cloud-bleconfig/PUT/disable_ble.json` | `ble.enable` false |
| `response/success.json` | response | `success` | `—` | Empty payload on success |
