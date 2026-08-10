# `/cloud/networkInterfaces`

- **GET** - Retrieves network interfaces (`getNetworkinterfaces`)

1 example(s) exported from the spec, 0 proposed.

## Method folders

Examples are split by HTTP method:

```
cloud-networkinterfaces/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `GET/application_json.json` | GET | response 200 | `application/json` | in-spec | yes |  |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X GET "https://$READER/cloud/networkInterfaces" \
  -H "Authorization: Bearer $TOKEN"

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

Then run `python ../validate_pack.py cloud-networkinterfaces`.
