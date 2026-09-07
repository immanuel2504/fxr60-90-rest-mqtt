# `/cloud/logs`

- **GET** - Get log configuration
- **PUT** - Update log configuration (`setLogs`)

## Reviewed PUT

Only live-working request bodies. `radio_control` / `cloud_agent` were accepted but did not apply as documented, so they are not included. Always send `radioPacketLog` if you do not want it reset to `false`.

| File | Example name | Summary |
|---|---|---|
| `PUT/logs.json` | `logs` | Set `reader_gateway` to DEBUG and enable radioPacketLog |
| `PUT/radioPacketLog_on.json` | `radioPacketLog_on` | Enable radioPacketLog only |
| `PUT/success.json` | `success` | Empty string on success |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/logs" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/logs.json
```
