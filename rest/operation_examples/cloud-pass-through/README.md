# `/cloud/pass-through`

- **PUT** - Pass-through command (`setPassthru`)

2 example(s) exported from the spec, 2 proposed.

## Method folders

Examples are split by HTTP method:

```
cloud-pass-through/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `PUT/passthru.json` | PUT | request | `passthru` | in-spec | yes |  |
| `PUT/status.json` | PUT | request | `status` | in-spec | yes |  |
| `PUT/passthru_version.json` | PUT | request | `passthru_version` | proposed | yes | Extra RC payload |
| `PUT/rc_status.json` | PUT | response 200 | `rc_status` | proposed | yes | Raw RC reply |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/pass-through" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/passthru.json

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

Then run `python ../validate_pack.py cloud-pass-through`.
