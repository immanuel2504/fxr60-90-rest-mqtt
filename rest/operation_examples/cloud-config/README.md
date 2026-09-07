# `/cloud/config`

- **GET** - Retrieves reader configuration (`getConfig`). Optional `xml` (Cloud Connect RFID profile). GPIO-LED unset is `{}`.
- **PUT** - Updates reader configuration (`setConfigMqtt`). Send at least one of `GPIO-LED` or `READER-GATEWAY`. `batching` / `retention` must be arrays and must be sent with `endpointConfig`.

## PUT examples (17)

Live accepted or working bodies from reader 5.0.7, plus `data_azure` (not live-tested). Failed, rejected, and bug-only cases are not included.

| File | Example name | Summary |
|---|---|---|
| `PUT/data_mqtt.json` | `data_mqtt` | MQTT data endpoint (tags delivered) |
| `PUT/data_mqtt_batching.json` | `data_mqtt_batching` | MQTT with batching and retention arrays |
| `PUT/data_aws.json` | `data_aws` | AWS IoT Core (connected; port 443 + ALPN) |
| `PUT/data_azure.json` | `data_azure` | Azure IoT Hub (not live-tested) |
| `PUT/data_http_post.json` | `data_http_post` | HTTP POST (tags delivered) |
| `PUT/data_tcpip_server.json` | `data_tcpip_server` | TCP/IP server (tags received) |
| `PUT/data_websocket.json` | `data_websocket` | WebSocket (accepted; did not connect) |
| `PUT/clear_data.json` | `clear_data` | Clear all data connections |
| `PUT/gpio_led_defaults.json` | `gpio_led_defaults` | GPIO-LED defaults only |
| `PUT/gpio_led_tag_radio.json` | `gpio_led_tag_radio` | GPIO-LED for tag read and radio start/stop |
| `PUT/gpio_led_cloud.json` | `gpio_led_cloud` | GPIO-LED for cloud connect/disconnect |
| `PUT/gpio_led_gpi.json` | `gpio_led_gpi` | GPIO-LED for GPI high/low events (accepted; not triggerable via API) |
| `PUT/gpio_led_conditions.json` | `gpio_led_conditions` | GPIO-LED actions with conditions |
| `PUT/combined_mqtt_gpio.json` | `combined_mqtt_gpio` | MQTT data plus GPIO-LED |
| `PUT/combined_http_gpio.json` | `combined_http_gpio` | HTTP POST plus conditional GPIO-LED |
| `PUT/combined_clear_gpio.json` | `combined_clear_gpio` | Clear data endpoint and keep GPIO-LED |
| `PUT/combined_aws_cloud_gpio.json` | `combined_aws_cloud_gpio` | AWS data plus cloud-event GPIO-LED |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/config" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/data_mqtt.json
```
