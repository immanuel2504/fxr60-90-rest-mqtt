# `/cloud/stop`

- **PUT** - Stop RFID Inventory or BLE scan (`stopInventory`)

| File | Example name | Summary |
|---|---|---|
| `PUT/stop_RFID_default.json` | `stop_RFID_default` | Stop RFID (default) |
| `PUT/stop_Global_RFID_only.json` | `stop_Global_RFID_only` | Global RFID only |
| `PUT/stop_Global_BLE_only.json` | `stop_Global_BLE_only` | Global BLE only |
| `PUT/stop_Global_BLE_and_RFID.json` | `stop_Global_BLE_and_RFID` | Global BLE and RFID |
| `PUT/stop_Targeted.json` | `stop_Targeted` | Targeted per data endpoint |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/stop" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/stop_RFID_default.json
```
