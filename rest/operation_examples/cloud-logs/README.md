# `/cloud/logs`

- **GET** - Get log configuration
- **PUT** - Update log configuration (`setLogs`)

## Reviewed PUT

| File | Example name | Summary |
|---|---|---|
| `PUT/logs.json` | `logs` | DEBUG radio_control and cloud_agent |
| `PUT/success.json` | `success` | Empty string on success |

## NEED LIVE TEST

Confirm request is accepted and success body is `""`; verify with GET `/cloud/logs`.

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/logs" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/logs.json
```
