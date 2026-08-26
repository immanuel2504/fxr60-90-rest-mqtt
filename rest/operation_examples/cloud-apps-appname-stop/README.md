# `/cloud/apps/{appname}/stop`

- **PUT** - Stop user application (`setStopuserapp`)

1 example(s) exported from the spec, 2 proposed.

## Method folders

Examples are split by HTTP method:

```
cloud-apps-appname-stop/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `PUT/stopUserapp.json` | PUT | request | `stopUserapp` | in-spec | yes |  |
| `PUT/success.json` | PUT | response 200 | `success` | proposed | yes | Empty string on success |
| `parameters.json` | - | parameters | `-` | proposed | yes | Suggested path/query parameter examples |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/apps/mylogger/stop" \
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

Then run `python ../validate_pack.py cloud-apps-appname-stop`.
