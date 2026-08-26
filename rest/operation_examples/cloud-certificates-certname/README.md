# `/cloud/certificates/{certname}`

- **PUT** - Refresh certificate (`setRefreshcertificate`)
- **DELETE** - Delete certificate (`delCertificate`)

## DELETE

`type` is in the **JSON request body**, not the URL. Device test 26 Aug 2026.

```http
DELETE /cloud/certificates/mqtt-client-cert
Content-Type: application/json

{ "type": "client" }
```

| File | Example name | Summary |
|---|---|---|
| `DELETE/request_del_certificate.json` | `del_certificate` | Delete client certificate |

MQTT twin: `del_certs` → `request/del_certs.json` (`name` + `type` in payload).

## Method folders

```
cloud-certificates-certname/
  PUT/     # refresh examples
  DELETE/  # delete request body
```

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X DELETE "https://$READER/cloud/certificates/mqtt-client-cert" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @DELETE/request_del_certificate.json
```
