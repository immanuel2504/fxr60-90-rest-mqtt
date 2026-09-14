# `set_config`

REST: `PUT /cloud/config` → `cloud-config/`

| File | Direction | Example name | Summary title |
|---|---|---|---|
| `request/clear_data_configuration.json` | request | `clear_data_configuration` | Clear data connections |
| `request/aws_data_endpoint.json` | request | `aws_data_endpoint` | AWS IoT Core data endpoint |
| `request/azure_data_endpoint.json` | request | `azure_data_endpoint` | Azure IoT Hub data endpoint |
| `request/http_post_data_endpoint.json` | request | `http_post_data_endpoint` | HTTP POST data endpoint |
| `request/mqtt_data_endpoint.json` | request | `mqtt_data_endpoint` | MQTT data endpoint |
| `request/mqtt_data_endpoint_with_batching.json` | request | `mqtt_data_endpoint_with_batching` | MQTT data endpoint with batching |
| `request/tcpip_server_data_endpoint.json` | request | `tcpip_server_data_endpoint` | TCP/IP server data endpoint |
| `request/websocket_data_endpoint.json` | request | `websocket_data_endpoint` | WebSocket data endpoint |
| `request/cloud_event_gpio_led.json` | request | `cloud_event_gpio_led` | GPIO-LED for cloud connect/disconnect |
| `request/conditional_gpio_led.json` | request | `conditional_gpio_led` | GPIO-LED actions with conditions |
| `request/gpio_led_defaults.json` | request | `gpio_led_defaults` | GPIO-LED defaults only |
| `request/gpi_event_gpio_led.json` | request | `gpi_event_gpio_led` | GPIO-LED for GPI high/low events |
| `request/tag_and_radio_event_gpio_led.json` | request | `tag_and_radio_event_gpio_led` | GPIO-LED for tag read and radio start/stop |
| `request/rfid_xml_profile.json` | request | `rfid_xml_profile` | RFID XML profile |
| `request/combined_configuration.json` | request | `combined_configuration` | MQTT data plus GPIO-LED |
| `response/success.json` | response | `success` | Command succeeded |
