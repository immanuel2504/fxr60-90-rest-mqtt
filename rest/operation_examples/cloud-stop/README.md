# `/cloud/stop`

- **PUT** - Stop RFID Inventory or BLE scan (`stopInventory`)

`scanType` is an array of `ble` and/or `rfid`.

| File | Example name | Summary |
|---|---|---|
| `PUT/stop_RFID.json` | `stop_RFID` | Stop RFID |
| `PUT/stop_RFID_explicit.json` | `stop_RFID_explicit` | Stop RFID (explicit) |
| `PUT/stop_BLE_only.json` | `stop_BLE_only` | Stop BLE only |
| `PUT/stop_BLE_and_RFID.json` | `stop_BLE_and_RFID` | Stop BLE and RFID |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/stop" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/stop_RFID.json
```
