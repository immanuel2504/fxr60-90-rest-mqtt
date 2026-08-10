# `/cloud/ble-config`

- **PUT** - Set BLE configuration (`setBleConfig`)
- **GET** - Get BLE configuration (`getBleConfig`)

6 example(s) exported from the spec, 1 proposed.

## Method folders

Examples are split by HTTP method:

```
cloud-ble-config/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `PUT/enable_ble.json` | PUT | request | `enable_ble` | in-spec | yes |  |
| `PUT/enable_with_interval.json` | PUT | request | `enable_with_interval` | in-spec | yes |  |
| `PUT/enable_with_rssi_filter.json` | PUT | request | `enable_with_rssi_filter` | in-spec | yes |  |
| `PUT/enable_with_protocols.json` | PUT | request | `enable_with_protocols` | in-spec | yes |  |
| `PUT/disable_ble.json` | PUT | request | `disable_ble` | in-spec | yes |  |
| `GET/inline.json` | GET | response 200 | `inline` | in-spec | yes |  |
| `GET/disabled.json` | GET | response 200 | `disabled` | proposed | yes | BLE off |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/ble-config" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/enable_ble.json

curl -sk -X GET "https://$READER/cloud/ble-config" \
  -H "Authorization: Bearer $TOKEN"

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

Then run `python ../validate_pack.py cloud-ble-config`.
