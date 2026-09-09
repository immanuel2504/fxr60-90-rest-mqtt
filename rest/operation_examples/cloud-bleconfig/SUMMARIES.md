# Example summary titles — `/cloud/bleConfig`

## GET response

### `GET/disabled.json`

| Field | Value |
|---|---|
| **Example name** | `disabled` |
| **Summary title** | `ble.enable false` |
| **HTTP status** | `200` |

### `GET/all_protocols.json`

| Field | Value |
|---|---|
| **Example name** | `all_protocols` |
| **Summary title** | `All protocols and filters` |
| **HTTP status** | `200` |

## PUT request

### `PUT/enable_ble.json`

| Field | Value |
|---|---|
| **Example name** | `enable_ble` |
| **Summary title** | `ble.enable true, interval 0` |

### `PUT/enable_with_interval.json`

| Field | Value |
|---|---|
| **Example name** | `enable_with_interval` |
| **Summary title** | `Interval 5` |

### `PUT/enable_with_rssi_filter.json`

| Field | Value |
|---|---|
| **Example name** | `enable_with_rssi_filter` |
| **Summary title** | `additionalFilters.rssi -70` |

### `PUT/enable_with_protocols.json`

| Field | Value |
|---|---|
| **Example name** | `enable_with_protocols` |
| **Summary title** | `All protocols and filters` |

### `PUT/disable_ble.json`

| Field | Value |
|---|---|
| **Example name** | `disable_ble` |
| **Summary title** | `ble.enable false` |

## PUT response

### `PUT/success.json`

| Field | Value |
|---|---|
| **Example name** | `success` |
| **Summary title** | `Empty string on success` |
| **HTTP status** | `200` |
