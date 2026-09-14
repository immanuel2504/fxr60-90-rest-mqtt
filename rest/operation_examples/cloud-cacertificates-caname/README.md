# `/cloud/caCertificates/{caname}`

- **PUT** - Install CA certificate (`setInstallCACertificate`)
- **DELETE** - Delete CA certificate (`delCACertificate`)

## Reviewed DELETE

| File | Example name | Summary |
|---|---|---|
| `DELETE/success.json` | `success` | Empty string on success |

Path parameter: `caname` = `AmazonRootCA1`

## Method folders

```
cloud-cacertificates-caname/
  PUT/     # install request examples
  DELETE/  # delete success response
```

| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `DELETE/success.json` | DELETE | response | `success` | reviewed | yes | Empty string on success |
| `PUT/InstallCACertificate.json` | PUT | request | `InstallCACertificate` | in-spec | yes |  |
| `PUT/InstallCACertificate_named.json` | PUT | request | `InstallCACertificate_named` | proposed | yes | MQTT-style body includes name; REST uses path {caname} |
| `parameters.json` | - | parameters | `-` | proposed | yes | Suggested path/query parameter examples |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/caCertificates/AmazonRootCA1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/InstallCACertificate.json

curl -sk -X DELETE "https://$READER/cloud/caCertificates/AmazonRootCA1" \
  -H "Authorization: Bearer $TOKEN"

```

Path parameter values above come from `parameters.json`; substitute your own.

## Folding a file back into the spec

Add under the operation `examples:` map in `FXR90-rest-api.yaml`:

```yaml
      examples:
        <example_name>:
          summary: <summary from the table>
          value:
            # contents of the .json file
```

Then run `python ../validate_pack.py cloud-cacertificates-caname`.
