# `/cloud/start`

- **PUT** - Start RFID Inventory or BLE scan (`startInventory`)

| File | Example name | Summary |
|---|---|---|
| `PUT/start_Inventory.json` | `start_Inventory` | Start RFID inventory (default) |
| `PUT/start_Inventory_with_AutoStart.json` | `start_Inventory with AutoStart` | Start inventory with AutoStart |
| `PUT/start_Inventory_with_ImpinjGen2X.json` | `start_Inventory with ImpinjGen2X` | Start inventory with Impinj Gen2X |
| `PUT/start_Global_BLE_only.json` | `start_Global_BLE_only` | Global BLE only |
| `PUT/start_Global_RFID_only.json` | `start_Global_RFID_only` | Global RFID only |
| `PUT/start_Global_BLE_and_RFID.json` | `start_Global_BLE_and_RFID` | Global BLE and RFID |
| `PUT/start_Targeted.json` | `start_Targeted` | Targeted per data endpoint |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/start" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/start_Inventory.json
```
