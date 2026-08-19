# `/cloud/certificates/{certname}`

- **PUT** - Refresh certificate (`setRefreshcertificate`)
- **DELETE** - Delete certificate (`delCertificate`)

## Reviewed DELETE

| File | Example name | Summary |
|---|---|---|
| `DELETE/success.json` | `success` | Empty string on success |

| Parameter | Value |
|---|---|
| Path `certname` | `mqtt-client-cert` |
| Query `type` | `client` |

MQTT twin: `del_certs` → `request/del_certs.json` (`name` + `type` in payload).

## Method folders

```
cloud-certificates-certname/
  PUT/     # refresh examples (not reviewed yet)
  DELETE/  # delete success response
```

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X DELETE "https://$READER/cloud/certificates/mqtt-client-cert?type=client" \
  -H "Authorization: Bearer $TOKEN"
```
