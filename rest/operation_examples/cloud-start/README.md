# `/cloud/start`

- **PUT** - Start RFID Inventory or BLE scan (`startInventory`)

6 example(s) exported from the spec, 0 proposed.

## Method folders

Examples are split by HTTP method:

```
cloud-start/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `PUT/start_Inventory.json` | PUT | request | `start_Inventory` | in-spec | yes |  |
| `PUT/start_Inventory_with_AutoStart.json` | PUT | request | `start_Inventory with AutoStart` | in-spec | yes |  |
| `PUT/start_Inventory_with_ImpinjGen2X.json` | PUT | request | `start_Inventory with ImpinjGen2X` | in-spec | yes |  |
| `PUT/start_BLE_only.json` | PUT | request | `start_BLE_only` | in-spec | yes |  |
| `PUT/start_RFID_only.json` | PUT | request | `start_RFID_only` | in-spec | yes |  |
| `PUT/start_BLE_and_RFID.json` | PUT | request | `start_BLE_and_RFID` | in-spec | yes | Global BLE and RFID |
| `PUT/start_targeted_RFID.json` | PUT | request | `start_targeted_RFID` | added | yes | Targeted RFID on dataEndpoint1 and dataEndpoint2 |
| `PUT/start_targeted_BLE.json` | PUT | request | `start_targeted_BLE` | added | yes | Targeted BLE on dataEndpoint1 and dataEndpoint2 |
| `PUT/start_targeted_BLE_and_RFID.json` | PUT | request | `start_targeted_BLE_and_RFID` | added | yes | Targeted BLE and RFID on both endpoints |
| `PUT/start_targeted_mixed.json` | PUT | request | `start_targeted_mixed` | added | yes | Targeted mixed — BLE on dataEndpoint1, RFID on dataEndpoint2 |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/start" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/start_Inventory.json

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

Then run `python ../validate_pack.py cloud-start`.
