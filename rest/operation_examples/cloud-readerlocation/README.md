# `/cloud/readerLocation`

- **GET** - Gets the GPS coordinates (lat/long) (`getGpsCoordinates`)

**Status: Deferred — discuss with developer** before finalizing examples  
(`lastReportedTime` unix vs ISO; no-fix shape; one vs two examples). Packs left as-is for now.

## Method folders

Examples are split by HTTP method:

```
cloud-readerlocation/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `GET/fix_acquired.json` | GET | response 200 | `fix_acquired` | proposed | yes | GPS fix — lat/long are strings in the schema |
| `GET/no_fix.json` | GET | response 200 | `no_fix` | proposed | yes | No satellites locked |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X GET "https://$READER/cloud/readerLocation" \
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

Then run `python ../validate_pack.py cloud-readerlocation`.
