# `/cloud/gpo`

- **GET** - Get GPO status (`getGpoStatus`)
- **PUT** - Set GPO (`setGpo`)

## Reviewed

| File | Example name | Summary |
|---|---|---|
| `GET/gpo_status.json` | `gpo_status` | Current GPO pin states |
| `PUT/gpo.json` | `gpo` | Port 3 HIGH |
| `PUT/success.json` | `success` | Empty string on success |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/gpo" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/gpo.json
```
