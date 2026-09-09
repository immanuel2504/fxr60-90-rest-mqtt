# `set_config`

REST: `PUT /cloud/config` → `cloud-config/`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/data_mqtt.json` | request | `data_mqtt` | `cloud-config/PUT/data_mqtt.json` | MQTT data endpoint (tags delivered) |
| `request/data_mqtt_batching.json` | request | `data_mqtt_batching` | `cloud-config/PUT/data_mqtt_batching.json` | MQTT with batching and retention arrays |
| `request/data_aws.json` | request | `data_aws` | `cloud-config/PUT/data_aws.json` | AWS IoT Core (port 443 + ALPN) |
| `request/data_azure.json` | request | `data_azure` | `cloud-config/PUT/data_azure.json` | Azure IoT Hub |
| `request/data_http_post.json` | request | `data_http_post` | `cloud-config/PUT/data_http_post.json` | HTTP POST (tags delivered) |
| `request/data_tcpip_server.json` | request | `data_tcpip_server` | `cloud-config/PUT/data_tcpip_server.json` | TCP/IP server (tags received) |
| `request/data_websocket.json` | request | `data_websocket` | `cloud-config/PUT/data_websocket.json` | WebSocket |
| `request/clear_data.json` | request | `clear_data` | `cloud-config/PUT/clear_data.json` | Clear all data connections |
| `request/gpio_led_defaults.json` | request | `gpio_led_defaults` | `cloud-config/PUT/gpio_led_defaults.json` | GPIO-LED defaults only |
| `request/gpio_led_tag_radio.json` | request | `gpio_led_tag_radio` | `cloud-config/PUT/gpio_led_tag_radio.json` | GPIO-LED for tag read and radio start/stop |
| `request/gpio_led_cloud.json` | request | `gpio_led_cloud` | `cloud-config/PUT/gpio_led_cloud.json` | GPIO-LED for cloud connect/disconnect |
| `request/gpio_led_gpi.json` | request | `gpio_led_gpi` | `cloud-config/PUT/gpio_led_gpi.json` | GPIO-LED for GPI high/low events |
| `request/gpio_led_conditions.json` | request | `gpio_led_conditions` | `cloud-config/PUT/gpio_led_conditions.json` | GPIO-LED actions with conditions |
| `request/combined_mqtt_gpio.json` | request | `combined_mqtt_gpio` | `cloud-config/PUT/combined_mqtt_gpio.json` | MQTT data plus GPIO-LED |
| `request/combined_http_gpio.json` | request | `combined_http_gpio` | `cloud-config/PUT/combined_http_gpio.json` | HTTP POST plus conditional GPIO-LED |
| `request/combined_clear_gpio.json` | request | `combined_clear_gpio` | `cloud-config/PUT/combined_clear_gpio.json` | Clear data endpoint and keep GPIO-LED |
| `request/combined_aws_cloud_gpio.json` | request | `combined_aws_cloud_gpio` | `cloud-config/PUT/combined_aws_cloud_gpio.json` | AWS data plus cloud-event GPIO-LED |
| `response/success.json` | response | `success` | `—` | Command succeeded |
