# Example summary titles — `/cloud/config`

### `GET/full_configuration.json`

| Field | Value |
|---|---|
| **Example name** | `full_configuration` |
| **Summary title** | `Full configuration (MQTT endpoints, GPIO-LED unset)` |

### `GET/gpio_led_not_configured.json`

| Field | Value |
|---|---|
| **Example name** | `gpio_led_not_configured` |
| **Summary title** | `GPIO-LED not configured (empty object)` |

### `PUT/data_mqtt.json`

| Field | Value |
|---|---|
| **Example name** | `data_mqtt` |
| **Summary title** | `MQTT data endpoint (tags delivered)` |

### `PUT/data_mqtt_batching.json`

| Field | Value |
|---|---|
| **Example name** | `data_mqtt_batching` |
| **Summary title** | `MQTT with batching and retention arrays` |

### `PUT/data_aws.json`

| Field | Value |
|---|---|
| **Example name** | `data_aws` |
| **Summary title** | `AWS IoT Core (port 443 + ALPN)` |

### `PUT/data_azure.json`

| Field | Value |
|---|---|
| **Example name** | `data_azure` |
| **Summary title** | `Azure IoT Hub` |

### `PUT/data_http_post.json`

| Field | Value |
|---|---|
| **Example name** | `data_http_post` |
| **Summary title** | `HTTP POST (tags delivered)` |

### `PUT/data_tcpip_server.json`

| Field | Value |
|---|---|
| **Example name** | `data_tcpip_server` |
| **Summary title** | `TCP/IP server (tags received)` |

### `PUT/data_websocket.json`

| Field | Value |
|---|---|
| **Example name** | `data_websocket` |
| **Summary title** | `WebSocket` |

### `PUT/clear_data.json`

| Field | Value |
|---|---|
| **Example name** | `clear_data` |
| **Summary title** | `Clear all data connections` |

### `PUT/gpio_led_defaults.json`

| Field | Value |
|---|---|
| **Example name** | `gpio_led_defaults` |
| **Summary title** | `GPIO-LED defaults only` |

### `PUT/gpio_led_tag_radio.json`

| Field | Value |
|---|---|
| **Example name** | `gpio_led_tag_radio` |
| **Summary title** | `GPIO-LED for tag read and radio start/stop` |

### `PUT/gpio_led_cloud.json`

| Field | Value |
|---|---|
| **Example name** | `gpio_led_cloud` |
| **Summary title** | `GPIO-LED for cloud connect/disconnect` |

### `PUT/gpio_led_gpi.json`

| Field | Value |
|---|---|
| **Example name** | `gpio_led_gpi` |
| **Summary title** | `GPIO-LED for GPI high/low events` |

### `PUT/gpio_led_conditions.json`

| Field | Value |
|---|---|
| **Example name** | `gpio_led_conditions` |
| **Summary title** | `GPIO-LED actions with conditions` |

### `PUT/combined_mqtt_gpio.json`

| Field | Value |
|---|---|
| **Example name** | `combined_mqtt_gpio` |
| **Summary title** | `MQTT data plus GPIO-LED` |

### `PUT/combined_http_gpio.json`

| Field | Value |
|---|---|
| **Example name** | `combined_http_gpio` |
| **Summary title** | `HTTP POST plus conditional GPIO-LED` |

### `PUT/combined_clear_gpio.json`

| Field | Value |
|---|---|
| **Example name** | `combined_clear_gpio` |
| **Summary title** | `Clear data endpoint and keep GPIO-LED` |

### `PUT/combined_aws_cloud_gpio.json`

| Field | Value |
|---|---|
| **Example name** | `combined_aws_cloud_gpio` |
| **Summary title** | `AWS data plus cloud-event GPIO-LED` |
