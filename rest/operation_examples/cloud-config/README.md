# `/cloud/config`

- **GET** - Retrieves reader configuration (`getConfig`). GPIO-LED unset is `{}`.
- **PUT** - Updates reader configuration (`setConfigMqtt`). Send at least one of `GPIO-LED` or `READER-GATEWAY`. `batching` / `retention` must be arrays and must be sent with `endpointConfig`.

## GET examples

| File | Example name | Summary |
|---|---|---|
| `GET/full_configuration.json` | `full_configuration` | Full configuration (MQTT endpoints, GPIO-LED unset) |

## PUT examples (15)

| File | Example name | Summary |
|---|---|---|
| `PUT/clear_data_configuration.json` | `clear_data_configuration` | Clear data connections |
| `PUT/aws_data_endpoint.json` | `aws_data_endpoint` | AWS IoT Core data endpoint |
| `PUT/azure_data_endpoint.json` | `azure_data_endpoint` | Azure IoT Hub data endpoint |
| `PUT/http_post_data_endpoint.json` | `http_post_data_endpoint` | HTTP POST data endpoint |
| `PUT/mqtt_data_endpoint.json` | `mqtt_data_endpoint` | MQTT data endpoint |
| `PUT/mqtt_data_endpoint_with_batching.json` | `mqtt_data_endpoint_with_batching` | MQTT data endpoint with batching |
| `PUT/tcpip_server_data_endpoint.json` | `tcpip_server_data_endpoint` | TCP/IP server data endpoint |
| `PUT/websocket_data_endpoint.json` | `websocket_data_endpoint` | WebSocket data endpoint |
| `PUT/cloud_event_gpio_led.json` | `cloud_event_gpio_led` | GPIO-LED for cloud connect/disconnect |
| `PUT/conditional_gpio_led.json` | `conditional_gpio_led` | GPIO-LED actions with conditions |
| `PUT/gpio_led_defaults.json` | `gpio_led_defaults` | GPIO-LED defaults only |
| `PUT/gpi_event_gpio_led.json` | `gpi_event_gpio_led` | GPIO-LED for GPI high/low events |
| `PUT/tag_and_radio_event_gpio_led.json` | `tag_and_radio_event_gpio_led` | GPIO-LED for tag read and radio start/stop |
| `PUT/rfid_xml_profile.json` | `rfid_xml_profile` | RFID XML profile |
| `PUT/combined_configuration.json` | `combined_configuration` | MQTT data plus GPIO-LED |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/config" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/mqtt_data_endpoint.json
```
