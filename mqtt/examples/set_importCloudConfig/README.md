# `set_importCloudConfig`

REST: `PUT /cloud/cloudConfig` → `cloud-cloudconfig/`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/mqtt_all_channels.json` | request | `mqtt_all_channels` | `cloud-cloudconfig/PUT/mqtt_all_channels.json` | All channels over MQTT, port 1883 |
| `request/mqtt_tls_all_channels.json` | request | `mqtt_tls_all_channels` | `cloud-cloudconfig/PUT/mqtt_tls_all_channels.json` | All channels over MQTT mTLS file paths, port 8884 |
| `request/data_mqtt_tls_installed_cert.json` | request | `data_mqtt_tls_installed_cert` | `cloud-cloudconfig/PUT/data_mqtt_tls_installed_cert.json` | MQTT mTLS via cert store plus CA, port 8884 |
| `request/mqtt_aws_all_channels.json` | request | `mqtt_aws_all_channels` | `cloud-cloudconfig/PUT/mqtt_aws_all_channels.json` | AWS IoT FileLocation, port 443 |
| `request/mqtt_aws_installed_cert.json` | request | `mqtt_aws_installed_cert` | `cloud-cloudconfig/PUT/mqtt_aws_installed_cert.json` | AWS IoT installed cert, port 443 |
| `request/mqtt_azure_all_channels.json` | request | `mqtt_azure_all_channels` | `cloud-cloudconfig/PUT/mqtt_azure_all_channels.json` | All channels over Azure IoT Hub |
| `request/data_http_post.json` | request | `data_http_post` | `cloud-cloudconfig/PUT/data_http_post.json` | HTTP POST |
| `request/data_tcpip_server.json` | request | `data_tcpip_server` | `cloud-cloudconfig/PUT/data_tcpip_server.json` | TCP/IP server |
| `request/data_websocket.json` | request | `data_websocket` | `cloud-cloudconfig/PUT/data_websocket.json` | WebSocket |
| `request/management_cmd_mqtt.json` | request | `management_cmd_mqtt` | `cloud-cloudconfig/PUT/management_cmd_mqtt.json` | Management command/response over MQTT |
| `request/management_event_mqtt.json` | request | `management_event_mqtt` | `cloud-cloudconfig/PUT/management_event_mqtt.json` | Management events over MQTT |
| `request/clear_data.json` | request | `clear_data` | `cloud-cloudconfig/PUT/clear_data.json` | Clear all data connections |
| `response/success.json` | response | `success` | `—` | Command succeeded |
