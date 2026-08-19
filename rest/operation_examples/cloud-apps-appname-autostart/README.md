# `/cloud/apps/{appname}/autostart`

- **PUT** - Autostart user application (`setAutostartuserapp`)

2 example(s) exported from the spec, 1 proposed.

## Method folders

Examples are split by HTTP method:

```
cloud-apps-appname-autostart/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `PUT/autostartUserapp.json` | PUT | request | `autostartUserapp` | in-spec | yes |  |
| `PUT/autostartUserapp-false.json` | PUT | request | `autostartUserapp-false` | in-spec | yes |  |
| `parameters.json` | - | parameters | `-` | proposed | yes | Suggested path/query parameter examples |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/apps/mylogger/autostart" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/autostartUserapp.json

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

Then run `python ../validate_pack.py cloud-apps-appname-autostart`.
