# `/cloud/config`

- **GET** - Retrieves reader configuration (`getConfig`). Optional `xml` (Cloud Connect RFID profile). GPIO-LED unset is `{}`.
- **PUT** - Updates reader configuration (`setConfigMqtt`). Send at least one of `xml`, `GPIO-LED`, or `READER-GATEWAY`. LED actions may use `led` 1, 2, or 3. `postActionColor` is `GREEN`, `RED`, or `AMBER` (`OFF` is rejected).

## PUT examples (12)

| File | Example name | Summary |
|---|---|---|
| `PUT/xml.json` | `xml` | Cloud Connect RFID XML profile |
| `PUT/data_mqtt.json` | `data_mqtt` | MQTT data with GPIO-LED, global batching/retention, and management events |
| `PUT/data_aws.json` | `data_aws` | Tag events over AWS IoT Core |
| `PUT/data_azure.json` | `data_azure` | Tag events over Azure IoT Hub |
| `PUT/data_http_post.json` | `data_http_post` | Tag events over HTTP POST |
| `PUT/data_tcpip_server.json` | `data_tcpip_server` | Tag events over TCP/IP server |
| `PUT/data_websocket.json` | `data_websocket` | Tag events over WebSocket |
| `PUT/clear_data.json` | `clear_data` | Clear all data connections |
| `PUT/gpio_led_tag_radio.json` | `gpio_led_tag_radio` | GPIO-LED for tag read and radio start/stop |
| `PUT/gpio_led_cloud.json` | `gpio_led_cloud` | GPIO-LED for cloud connect/disconnect |
| `PUT/gpio_led_gpi.json` | `gpio_led_gpi` | GPIO-LED for GPI high/low events |
| `PUT/gpio_led_conditions.json` | `gpio_led_conditions` | GPIO-LED actions with conditions |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/config" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/data_mqtt.json
```
