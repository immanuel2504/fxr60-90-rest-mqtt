# `/cloud/apps/install`

- **PUT** - Install user application (`setInstalluserapp`)

## NOTE — NEED LIVE TEST

Can HTTPS install use installed certs via `installedCertificateName` / `installedCertificateType` (from `GET /cloud/certificates`), or must trust come from the CA store / inline PEM?

See `NEED_LIVE_TEST.md`. Until confirmed, prefer SFTP + BASIC (`installUserapp.json`) over `installUserapp_pinned_ca.json`.

1 example(s) exported from the spec, 3 proposed.

## Method folders

Examples are split by HTTP method:

```
cloud-apps-install/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `PUT/installUserapp.json` | PUT | request | `installUserapp` | in-spec | yes | Install app over SFTP (BASIC) |
| `PUT/installUserapp_async.json` | PUT | request | `installUserapp_async` | proposed | yes | Install app over HTTPS with retry (async) |
| `PUT/installUserapp_no_auth.json` | PUT | request | `installUserapp_no_auth` | proposed | yes | NONE auth |
| `PUT/installUserapp_pinned_ca.json` | PUT | request | `installUserapp_pinned_ca` | proposed | yes | BASIC + TLS pin |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/apps/install" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/installUserapp.json

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

Then run `python ../validate_pack.py cloud-apps-install`.
