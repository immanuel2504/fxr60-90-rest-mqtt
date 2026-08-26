# `/cloud/os`

- **PUT** - Updates OS software on device (`setOs`)

## NEED LIVE TEST

For HTTPS firmware download: does TLS trust use **installed** certs (`installedCertificateName`/`Type`) or **inline/file CA** (`CACertificateFileContent` / `CACertificateFileLocation`)?

See `NEED_LIVE_TEST.md`. Until confirmed, prefer `os.json` / `os_basic_auth.json` / `os_scp.json` — do not finalize `os_https_pinned_ca.json`.

1 example(s) exported from the spec, 3 proposed.

## Method folders

Examples are split by HTTP method:

```
cloud-os/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `PUT/os.json` | PUT | request | `os` | in-spec | yes |  |
| `PUT/os_https_retry.json` | PUT | request | `os_https_retry` | proposed | yes | HTTPS OS update with retry (always async) |
| `PUT/os_basic_auth.json` | PUT | request | `os_basic_auth` | proposed | yes | HTTPS + BASIC |
| `PUT/os_scp.json` | PUT | request | `os_scp` | proposed | yes | SCP transfer |
| `PUT/os_https_pinned_ca.json` | PUT | request | `os_https_pinned_ca` | proposed | yes | HTTPS with pinned CA + retry |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/os" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/os.json

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

Then run `python ../validate_pack.py cloud-os`.
