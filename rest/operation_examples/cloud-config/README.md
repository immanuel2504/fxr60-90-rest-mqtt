# `/cloud/config`

- **GET** - Retrieves reader configuration (`getConfig`)
- **PUT** - Updates reader configuration (`setConfigMqtt`)

13 example(s) exported from the spec, 1 proposed. **1 fail schema validation.**

> **Note.** SCHEMA DEFECT on GET: GetConfigResponse.GPIO-LED oneOf is only `string`. In-spec `{}` is invalid. Proposed file uses NOT_CONFIGURED string (valid today).

## Method folders

Examples are split by HTTP method:

```
cloud-config/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `GET/inline.json` | GET | response 200 | `inline` | in-spec | NO | $.GPIO-LED: expected string, got dict |
| `GET/gpio_led_not_configured.json` | GET | response 200 | `gpio_led_not_configured` | proposed | yes | Valid today — GPIO-LED NOT_CONFIGURED string (in-spec {} is invalid) |
| `PUT/config_data_mqtt_async.json` | PUT | request | `config_data_mqtt_async` | in-spec | yes |  |
| `PUT/config_data_aws.json` | PUT | request | `config_data_aws` | in-spec | yes |  |
| `PUT/config_data_azure_mqtt.json` | PUT | request | `config_data_azure_mqtt` | in-spec | yes |  |
| `PUT/config_data_clear.json` | PUT | request | `config_data_clear` | in-spec | yes |  |
| `PUT/config_data_httpPost.json` | PUT | request | `config_data_httpPost` | in-spec | yes |  |
| `PUT/config_data_mqtt.json` | PUT | request | `config_data_mqtt` | in-spec | yes |  |
| `PUT/config_data_tcp_ip.json` | PUT | request | `config_data_tcp_ip` | in-spec | yes |  |
| `PUT/config_data_websocket.json` | PUT | request | `config_data_websocket` | in-spec | yes |  |
| `PUT/config_global_batching.json` | PUT | request | `config_global_batching` | in-spec | yes |  |
| `PUT/config_global_retention.json` | PUT | request | `config_global_retention` | in-spec | yes |  |
| `PUT/config_management_events.json` | PUT | request | `config_management_events` | in-spec | yes |  |
| `PUT/config_gpio_led.json` | PUT | request | `config_gpio_led` | in-spec | yes |  |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X GET "https://$READER/cloud/config" \
  -H "Authorization: Bearer $TOKEN"

curl -sk -X PUT "https://$READER/cloud/config" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/config_data_mqtt_async.json

```

## Folding a file back into the spec

Add under the operation `examples:` map in `FXR90-rest-api.yaml`:

```yaml
      examples:
        <example_name>:
          summary: <summary from the table>
          value:
            # contents of the .json file
```

Then run `python ../validate_pack.py cloud-config`.
