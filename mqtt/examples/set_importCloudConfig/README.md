# set_importCloudConfig

REST: PUT /cloud/cloudConfig -> cloud-cloudconfig/

| File | Direction | Example | Summary |
|---|---|---|---|
| request/mqtt_all_channels.json | request | mqtt_all_channels | All channels over MQTT, port 1883 |
| request/mqtt_tls_all_channels.json | request | mqtt_tls_all_channels | All channels over MQTT mTLS file paths, port 8884 |
| request/data_mqtt_tls_installed_cert.json | request | data_mqtt_tls_installed_cert | MQTT mTLS via cert store plus CA, port 8884 |
| request/mqtt_aws_all_channels.json | request | mqtt_aws_all_channels | AWS IoT FileLocation, port 443 |
| request/mqtt_aws_installed_cert.json | request | mqtt_aws_installed_cert | AWS IoT installed cert, port 443 |
| request/mqtt_azure_all_channels.json | request | mqtt_azure_all_channels | All channels over Azure IoT Hub (not live-tested) |
| request/data_tcpip_server.json | request | data_tcpip_server | TCP/IP server (reader listens) |
| request/data_websocket.json | request | data_websocket | WebSocket (accepted) |
| request/data_http_post.json | request | data_http_post | HTTP POST (tags delivered) |
| request/management_cmd_mqtt.json | request | management_cmd_mqtt | Management command/response over MQTT |
| request/management_event_mqtt.json | request | management_event_mqtt | Management events over MQTT |
| request/clear_data.json | request | clear_data | Clear all data connections |
| response/success.json | response | success | Empty string on success |
