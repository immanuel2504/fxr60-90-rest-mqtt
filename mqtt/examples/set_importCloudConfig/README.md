# set_importCloudConfig

REST: PUT /cloud/cloudConfig -> cloud-cloudconfig/

| File | Direction | Example | Summary |
|---|---|---|---|
| 
equest/mqtt_all_channels.json | request | mqtt_all_channels | All channels over MQTT (no TLS) |
| 
equest/mqtt_tls_all_channels.json | request | mqtt_tls_all_channels | All channels over MQTT TLS |
| 
equest/mqtt_aws_all_channels.json | request | mqtt_aws_all_channels | All channels over AWS IoT Core |
| 
equest/mqtt_azure_all_channels.json | request | mqtt_azure_all_channels | All channels over Azure IoT Hub |
| 
equest/data_tcpip_server.json | request | data_tcpip_server | Tag events over TCP/IP server |
| 
equest/data_websocket.json | request | data_websocket | Tag events over WebSocket |
| 
equest/data_http_post.json | request | data_http_post | Tag events over HTTP POST |
| 
equest/management_event_mqtt.json | request | management_event_mqtt | Management events over MQTT |
| 
equest/clear_data.json | request | clear_data | Clear all data connections |
| 
equest/data_mqtt_tls_installed_cert.json | request | data_mqtt_tls_installed_cert | Tag events over MQTT TLS with installed cert |
| 
esponse/success.json | response | success | Empty string on success |
