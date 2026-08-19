# `/cloud/certificates`

- **GET** - Retrieve installed certificate details (`getCertificates`)
- **PUT** - Install certificate (`setUpdatecertificate`)

## Reviewed GET

| File | Example name | Summary |
|---|---|---|
| `GET/installed.json` | `installed` | Server and client certificates |

## PUT — NEED LIVE TEST

Do not finalize PUT examples until live install is confirmed. See `NEED_LIVE_TEST.md`.

## Method folders

```
cloud-certificates/
  GET/     # GET response examples
  PUT/     # PUT request examples (not reviewed yet)
```

| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `GET/installed.json` | GET | response 200 | `installed` | reviewed | yes | Server and client certificates |
| `PUT/updateCertificate.json` | PUT | request | `updateCertificate` | in-spec | yes |  |
| `PUT/updateCertificate_client.json` | PUT | request | `updateCertificate_client` | proposed | yes | Client cert for mTLS MQTT |
| `PUT/updateCertificate_app.json` | PUT | request | `updateCertificate_app` | proposed | yes | App certificate, no download auth |
| `PUT/updateCertificate_inline_pem.json` | PUT | request | `updateCertificate_inline_pem` | proposed | yes | Inline CA content |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X GET "https://$READER/cloud/certificates" \
  -H "Authorization: Bearer $TOKEN"

curl -sk -X PUT "https://$READER/cloud/certificates" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/updateCertificate.json

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

Then run `python ../validate_pack.py cloud-certificates`.
