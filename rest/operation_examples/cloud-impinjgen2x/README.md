# `/cloud/impinjGen2X`

- **GET** - Get Impinj Gen2X configuration (`getImpinjGen2X`)
- **PUT** - Set Impinj Gen2X configuration (`setImpinjGen2X`)

19 example(s). PUT request bodies are the 12 live-accepted examples from 6 September 2026 (FXR60 5.0.7). Rejected combination and validation probes are not published.

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
| `GET/fastID_disabled.json` | GET | response 200 | `fastID_disabled` | live 8 Sep 2026 | yes | FXR60 and FXR90 5.0.7 after FastID PUT |
| `GET/fastID_configured.json` | GET | response 200 | `fastID_configured` | live | yes | Last PUT was FastID enabled |
| `GET/tagFocus_configured.json` | GET | response 200 | `tagFocus_configured` | live | yes | Last PUT was TagFocus |
| `GET/tagProtect_configured.json` | GET | response 200 | `tagProtect_configured` | live | yes | Last PUT was TagProtect |
| `GET/tagQuieting_basic_configured.json` | GET | response 200 | `tagQuieting_basic_configured` | live | yes | Last PUT was basic quieting |
| `GET/tagQuieting_advanced_configured.json` | GET | response 200 | `tagQuieting_advanced_configured` | live | yes | Last PUT was advanced quieting |
| `PUT/response_200_success.json` | PUT | response 200 | `success` | live 6 Sep 2026 | yes | Response: Gen2X configured (apply on start) |
| `PUT/enable_fastID.json` | PUT | request | `enable_fastID` | live 6 Sep 2026 | yes | Enable FastID |
| `PUT/disable_fastID.json` | PUT | request | `disable_fastID` | live 6 Sep 2026 | yes | Disable FastID |
| `PUT/protect_tag.json` | PUT | request | `protect_tag` | live 6 Sep 2026 | yes | Protect tag |
| `PUT/unprotect_tag.json` | PUT | request | `unprotect_tag` | live 6 Sep 2026 | yes | Unprotect tag; reader may inject `enableShortRange: false` |
| `PUT/enable_protect_read.json` | PUT | request | `enable_protect_read` | live 6 Sep 2026 | yes | Enable protected-tag visibility |
| `PUT/disable_protect_read.json` | PUT | request | `disable_protect_read` | live 6 Sep 2026 | yes | Disable protected-tag visibility |
| `PUT/enable_tagFocus.json` | PUT | request | `enable_tagFocus` | live 6 Sep 2026 | yes | Enable TagFocus |
| `PUT/disable_tagFocus.json` | PUT | request | `disable_tagFocus` | live 6 Sep 2026 | yes | Disable TagFocus |
| `PUT/quiet_tags.json` | PUT | request | `quiet_tags` | live 6 Sep 2026 | yes | Quiet tags by EPC list |
| `PUT/unquiet_tags.json` | PUT | request | `unquiet_tags` | live 6 Sep 2026 | yes | Unquiet tags by EPC list (accepted; visibility returns by not applying Gen2X) |
| `PUT/advanced_quiet_tags.json` | PUT | request | `advanced_quiet_tags` | live 6 Sep 2026 | yes | Advanced quiet tags |
| `PUT/advanced_unquiet_tags.json` | PUT | request | `advanced_unquiet_tags` | live 6 Sep 2026 | yes | Advanced unquiet tags |

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
