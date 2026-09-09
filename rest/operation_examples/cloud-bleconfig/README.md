# `/cloud/bleConfig`

- **GET** — BLE scanner configuration (`get_bleConfig`)
- **PUT** — Set BLE scanner configuration (`set_bleConfig`)

## GET examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `GET/disabled.json` | response 200 | `disabled` | `ble.enable` false |
| `GET/all_protocols.json` | response 200 | `all_protocols` | All protocols and filters |

## PUT examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `PUT/enable_ble.json` | request | `enable_ble` | `ble.enable` true, interval `0` |
| `PUT/enable_with_interval.json` | request | `enable_with_interval` | Interval `5` |
| `PUT/enable_with_rssi_filter.json` | request | `enable_with_rssi_filter` | `additionalFilters.rssi` `-70` |
| `PUT/enable_with_protocols.json` | request | `enable_with_protocols` | All protocols and filters |
| `PUT/disable_ble.json` | request | `disable_ble` | `ble.enable` false |
| `PUT/success.json` | response 200 | `success` | Empty string on success |
