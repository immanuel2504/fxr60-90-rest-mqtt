# `/cloud/hostName`

- **GET** - Retrieves reader hostname (`getHostName`)
- **PUT** - Sets reader hostname (`setHostName`)

1 example(s) exported from the spec, 2 proposed.

> **Note.** Request field is `hostname`; response field is `hostName`.

## Method folders

Examples are split by HTTP method:

```
cloud-hostname/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `GET/configured.json` | GET | response 200 | `configured` | proposed | yes | Current hostname |
| `PUT/hostName.json` | PUT | request | `hostName` | in-spec | yes |  |
| `PUT/hostName_lab.json` | PUT | request | `hostName_lab` | proposed | yes | Alternate hostname style |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X GET "https://$READER/cloud/hostName" \
  -H "Authorization: Bearer $TOKEN"

curl -sk -X PUT "https://$READER/cloud/hostName" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/hostName.json

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

Then run `python ../validate_pack.py cloud-hostname`.
