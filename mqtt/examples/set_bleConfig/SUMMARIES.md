# Example summary titles — `set_bleConfig`

## PUT request

### `request/enable_ble.json`

| Field | Value |
|---|---|
| **Example name** | `enable_ble` |
| **Summary title** | `ble.enable true, interval 0` |

### `request/enable_with_interval.json`

| Field | Value |
|---|---|
| **Example name** | `enable_with_interval` |
| **Summary title** | `Interval 5` |

### `request/enable_with_rssi_filter.json`

| Field | Value |
|---|---|
| **Example name** | `enable_with_rssi_filter` |
| **Summary title** | `additionalFilters.rssi -70` |

### `request/enable_with_protocols.json`

| Field | Value |
|---|---|
| **Example name** | `enable_with_protocols` |
| **Summary title** | `All protocols and filters` |

### `request/disable_ble.json`

| Field | Value |
|---|---|
| **Example name** | `disable_ble` |
| **Summary title** | `ble.enable false` |

## PUT response

### `response/success.json`

| Field | Value |
|---|---|
| **Example name** | `success` |
| **Summary title** | `Empty payload on success` |
