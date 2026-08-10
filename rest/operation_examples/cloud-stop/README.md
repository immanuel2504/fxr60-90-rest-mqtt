# `/cloud/stop`

- **PUT** - Stop RFID Inventory or BLE scan (`stopInventory`)

4 example(s) exported from the spec, 0 proposed.

## Method folders

Examples are split by HTTP method:

```
cloud-stop/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `PUT/stop_RFID_default.json` | PUT | request | `stop_RFID_default` | in-spec | yes |  |
| `PUT/stop_RFID_explicit.json` | PUT | request | `stop_RFID_explicit` | in-spec | yes |  |
| `PUT/stop_BLE_only.json` | PUT | request | `stop_BLE_only` | in-spec | yes |  |
| `PUT/stop_BLE_and_RFID.json` | PUT | request | `stop_BLE_and_RFID` | in-spec | yes |  |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/stop" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/stop_RFID_default.json

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

Then run `python ../validate_pack.py cloud-stop`.
