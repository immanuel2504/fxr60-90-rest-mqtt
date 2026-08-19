# set_importCloudConfig

REST: PUT /cloud/cloudConfig -> cloud-cloudconfig/

| File | Direction | Example | Summary |
|---|---|---|---|
| request/mqtt_all_channels.json | request | mqtt_all_channels | All channels over MQTT (no TLS) |
| request/mqtt_tls_all_channels.json | request | mqtt_tls_all_channels | All channels over MQTT TLS |
| request/mqtt_aws_all_channels.json | request | mqtt_aws_all_channels | All channels over AWS IoT Core |
| request/mqtt_azure_all_channels.json | request | mqtt_azure_all_channels | All channels over Azure IoT Hub |
| request/data_tcpip_server.json | request | data_tcpip_server | Tag events over TCP/IP server |
| request/data_websocket.json | request | data_websocket | Tag events over WebSocket |
| request/data_http_post.json | request | data_http_post | Tag events over HTTP POST |
| request/management_cmd_mqtt.json | request | management_cmd_mqtt | Management command/response over MQTT |
| request/management_event_mqtt.json | request | management_event_mqtt | Management events over MQTT |
| request/clear_data.json | request | clear_data | Clear all data connections |
| request/data_mqtt_tls_installed_cert.json | request | data_mqtt_tls_installed_cert | Tag events over MQTT TLS with installed cert |
| response/success.json | response | success | Empty string on success |
