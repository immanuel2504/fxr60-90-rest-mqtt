# `/cloud/supportedStandardList`

- **GET** - Retrieves the standard channels of the supported regions (`getSupportedstandardlist`)

1 example(s) exported from the spec, 1 proposed.

## Method folders

Examples are split by HTTP method:

```
cloud-supportedstandardlist/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `GET/inline.json` | GET | response 200 | `inline` | in-spec | yes |  |
| `parameters.json` | - | parameters | `-` | proposed | yes | Suggested path/query parameter examples |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X GET "https://$READER/cloud/supportedStandardList?region=India" \
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

Then run `python ../validate_pack.py cloud-supportedstandardlist`.
