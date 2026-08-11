# `/cloud/cloudConfig`

- **PUT** — Import cloud endpoint configuration (`set_importCloudConfig`)

## Examples

| File | Example name | Summary |
|---|---|---|
| `PUT/mqtt_all_channels.json` | `mqtt_all_channels` | All channels over MQTT (no TLS) |
| `PUT/mqtt_tls_all_channels.json` | `mqtt_tls_all_channels` | All channels over MQTT TLS |
| `PUT/mqtt_aws_all_channels.json` | `mqtt_aws_all_channels` | All channels over AWS IoT Core |
| `PUT/mqtt_azure_all_channels.json` | `mqtt_azure_all_channels` | All channels over Azure IoT Hub |
| `PUT/data_tcpip_server.json` | `data_tcpip_server` | Tag events over TCP/IP server |
| `PUT/data_websocket.json` | `data_websocket` | Tag events over WebSocket |
| `PUT/data_http_post.json` | `data_http_post` | Tag events over HTTP POST |
| `PUT/management_event_mqtt.json` | `management_event_mqtt` | Management events over MQTT |
| `PUT/clear_data.json` | `clear_data` | Clear all data connections |
| `PUT/data_mqtt_tls_installed_cert.json` | `data_mqtt_tls_installed_cert` | Tag events over MQTT TLS with installed cert |

See **`SUMMARIES.md`**.
