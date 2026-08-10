# `/cloud/cloudConfig`

- **PUT** - Import cloud endpoint configuration (`setImportcloudconfig`)

1 example(s) exported from the spec, 4 proposed.

> **Note.** priority: only one import sample in the spec. Proposed MQTT / AWS / Azure / httpPost variants mirror PUT /cloud/config connection types under endpointConfig.

## Method folders

Examples are split by HTTP method:

```
cloud-cloudconfig/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `PUT/importCloudConfig.json` | PUT | request | `importCloudConfig` | in-spec | yes |  |
| `PUT/importCloudConfig_mqtt.json` | PUT | request | `importCloudConfig_mqtt` | proposed | yes | MQTT data plane import |
| `PUT/importCloudConfig_aws.json` | PUT | request | `importCloudConfig_aws` | proposed | yes | AWS IoT mqtt-AWS data plane |
| `PUT/importCloudConfig_azure.json` | PUT | request | `importCloudConfig_azure` | proposed | yes | Azure IoT Hub mqtt-AZURE data plane |
| `PUT/importCloudConfig_httpPost.json` | PUT | request | `importCloudConfig_httpPost` | proposed | yes | HTTP POST webhook data plane |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/cloudConfig" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/importCloudConfig.json

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

Then run `python ../validate_pack.py cloud-cloudconfig`.
