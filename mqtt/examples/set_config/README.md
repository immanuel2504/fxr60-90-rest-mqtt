# `set_config`

REST: `PUT /cloud/config` → `cloud-config/`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/xml.json` | request | `xml` | `cloud-config/PUT/xml.json` | Cloud Connect RFID XML profile |
| `request/data_mqtt.json` | request | `data_mqtt` | `cloud-config/PUT/data_mqtt.json` | MQTT data with GPIO-LED, global batching/retention, and management events |
| `request/data_aws.json` | request | `data_aws` | `cloud-config/PUT/data_aws.json` | Tag events over AWS IoT Core |
| `request/data_azure.json` | request | `data_azure` | `cloud-config/PUT/data_azure.json` | Tag events over Azure IoT Hub |
| `request/data_http_post.json` | request | `data_http_post` | `cloud-config/PUT/data_http_post.json` | Tag events over HTTP POST |
| `request/data_tcpip_server.json` | request | `data_tcpip_server` | `cloud-config/PUT/data_tcpip_server.json` | Tag events over TCP/IP server |
| `request/data_websocket.json` | request | `data_websocket` | `cloud-config/PUT/data_websocket.json` | Tag events over WebSocket |
| `request/clear_data.json` | request | `clear_data` | `cloud-config/PUT/clear_data.json` | Clear all data connections |
| `request/gpio_led_tag_radio.json` | request | `gpio_led_tag_radio` | `cloud-config/PUT/gpio_led_tag_radio.json` | GPIO-LED for tag read and radio start/stop |
| `request/gpio_led_cloud.json` | request | `gpio_led_cloud` | `cloud-config/PUT/gpio_led_cloud.json` | GPIO-LED for cloud connect/disconnect |
| `request/gpio_led_gpi.json` | request | `gpio_led_gpi` | `cloud-config/PUT/gpio_led_gpi.json` | GPIO-LED for GPI high/low events |
| `request/gpio_led_conditions.json` | request | `gpio_led_conditions` | `cloud-config/PUT/gpio_led_conditions.json` | GPIO-LED actions with conditions |
| `response/success.json` | response | `success` | `—` | Command succeeded |
