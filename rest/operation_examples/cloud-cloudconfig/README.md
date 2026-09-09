# `/cloud/cloudConfig`

- **PUT** — Import cloud endpoint configuration (`set_importCloudConfig`)

## PUT examples (12)

| File | Example name | Summary |
|---|---|---|
| `PUT/mqtt_all_channels.json` | `mqtt_all_channels` | All channels over MQTT, port 1883 |
| `PUT/mqtt_tls_all_channels.json` | `mqtt_tls_all_channels` | All channels over MQTT mTLS file paths, port 8884 |
| `PUT/data_mqtt_tls_installed_cert.json` | `data_mqtt_tls_installed_cert` | MQTT mTLS via cert store plus CA, port 8884 |
| `PUT/mqtt_aws_all_channels.json` | `mqtt_aws_all_channels` | AWS IoT FileLocation, port 443 |
| `PUT/mqtt_aws_installed_cert.json` | `mqtt_aws_installed_cert` | AWS IoT installed cert, port 443 |
| `PUT/mqtt_azure_all_channels.json` | `mqtt_azure_all_channels` | All channels over Azure IoT Hub |
| `PUT/data_http_post.json` | `data_http_post` | HTTP POST |
| `PUT/data_tcpip_server.json` | `data_tcpip_server` | TCP/IP server |
| `PUT/data_websocket.json` | `data_websocket` | WebSocket |
| `PUT/management_cmd_mqtt.json` | `management_cmd_mqtt` | Management command/response over MQTT |
| `PUT/management_event_mqtt.json` | `management_event_mqtt` | Management events over MQTT |
| `PUT/clear_data.json` | `clear_data` | Clear all data connections |

See **`SUMMARIES.md`**.
