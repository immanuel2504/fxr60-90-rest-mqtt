# `/cloud/impinjGen2X`

- **GET** - Get Impinj Gen2X configuration (`getImpinjGen2X`)
- **PUT** - Set Impinj Gen2X configuration (`setImpinjGen2X`)

19 example(s).

## Method folders

Examples are split by HTTP method:

```
cloud-impinjgen2x/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Summary |
|---|---|---|---|---|
| `GET/fastID_disabled.json` | GET | response 200 | `fastID_disabled` | FXR60 and FXR90 5.0.7 after FastID PUT |
| `GET/fastID_configured.json` | GET | response 200 | `fastID_configured` | Last PUT was FastID enabled |
| `GET/tagFocus_configured.json` | GET | response 200 | `tagFocus_configured` | Last PUT was TagFocus |
| `GET/tagProtect_configured.json` | GET | response 200 | `tagProtect_configured` | Last PUT was TagProtect |
| `GET/tagQuieting_basic_configured.json` | GET | response 200 | `tagQuieting_basic_configured` | Last PUT was basic quieting |
| `GET/tagQuieting_advanced_configured.json` | GET | response 200 | `tagQuieting_advanced_configured` | Last PUT was advanced quieting |
| `PUT/response_200_success.json` | PUT | response 200 | `success` | Response: Gen2X configured (apply on start) |
| `PUT/enable_fastID.json` | PUT | request | `enable_fastID` | Enable FastID |
| `PUT/disable_fastID.json` | PUT | request | `disable_fastID` | Disable FastID |
| `PUT/protect_tag.json` | PUT | request | `protect_tag` | Protect tag |
| `PUT/unprotect_tag.json` | PUT | request | `unprotect_tag` | Unprotect tag; reader may inject `enableShortRange: false` |
| `PUT/enable_protect_read.json` | PUT | request | `enable_protect_read` | Enable protected-tag visibility |
| `PUT/disable_protect_read.json` | PUT | request | `disable_protect_read` | Disable protected-tag visibility |
| `PUT/enable_tagFocus.json` | PUT | request | `enable_tagFocus` | Enable TagFocus |
| `PUT/disable_tagFocus.json` | PUT | request | `disable_tagFocus` | Disable TagFocus |
| `PUT/quiet_tags.json` | PUT | request | `quiet_tags` | Quiet tags by EPC list |
| `PUT/unquiet_tags.json` | PUT | request | `unquiet_tags` | Unquiet tags by EPC list (accepted; visibility returns by not applying Gen2X) |
| `PUT/advanced_quiet_tags.json` | PUT | request | `advanced_quiet_tags` | Advanced quiet tags |
| `PUT/advanced_unquiet_tags.json` | PUT | request | `advanced_unquiet_tags` | Advanced unquiet tags |

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
