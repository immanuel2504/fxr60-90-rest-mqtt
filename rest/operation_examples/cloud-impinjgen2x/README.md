# `/cloud/impinjGen2X`

- **GET** - Get Impinj Gen2X configuration (`getImpinjGen2X`)
- **PUT** - Set Impinj Gen2X configuration (`setImpinjGen2X`)

18 example(s) exported from the spec, 0 proposed.

## Method folders

Examples are split by HTTP method:

```
cloud-impinjgen2x/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `GET/empty.json` | GET | response 200 | `empty` | in-spec | yes |  |
| `GET/fastID_configured.json` | GET | response 200 | `fastID_configured` | in-spec | yes |  |
| `GET/tagFocus_configured.json` | GET | response 200 | `tagFocus_configured` | in-spec | yes |  |
| `GET/tagProtect_configured.json` | GET | response 200 | `tagProtect_configured` | in-spec | yes |  |
| `GET/tagQuieting_basic_configured.json` | GET | response 200 | `tagQuieting_basic_configured` | in-spec | yes |  |
| `GET/tagQuieting_advanced_configured.json` | GET | response 200 | `tagQuieting_advanced_configured` | in-spec | yes |  |
| `PUT/enable_fastID.json` | PUT | request | `enable_fastID` | in-spec | yes |  |
| `PUT/disable_fastID.json` | PUT | request | `disable_fastID` | in-spec | yes |  |
| `PUT/protect_tag.json` | PUT | request | `protect_tag` | in-spec | yes |  |
| `PUT/unprotect_tag.json` | PUT | request | `unprotect_tag` | in-spec | yes |  |
| `PUT/enable_protect_read.json` | PUT | request | `enable_protect_read` | in-spec | yes |  |
| `PUT/disable_protect_read.json` | PUT | request | `disable_protect_read` | in-spec | yes |  |
| `PUT/enable_tagFocus.json` | PUT | request | `enable_tagFocus` | in-spec | yes |  |
| `PUT/disable_tagFocus.json` | PUT | request | `disable_tagFocus` | in-spec | yes |  |
| `PUT/quiet_tags.json` | PUT | request | `quiet_tags` | in-spec | yes |  |
| `PUT/unquiet_tags.json` | PUT | request | `unquiet_tags` | in-spec | yes |  |
| `PUT/advanced_quiet_tags.json` | PUT | request | `advanced_quiet_tags` | in-spec | yes |  |
| `PUT/advanced_unquiet_tags.json` | PUT | request | `advanced_unquiet_tags` | in-spec | yes |  |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X GET "https://$READER/cloud/impinjGen2X" \
  -H "Authorization: Bearer $TOKEN"

curl -sk -X PUT "https://$READER/cloud/impinjGen2X" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/enable_fastID.json

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

Then run `python ../validate_pack.py cloud-impinjgen2x`.
