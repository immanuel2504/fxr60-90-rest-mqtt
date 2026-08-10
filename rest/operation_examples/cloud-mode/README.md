# `/cloud/mode`

- **GET** - Retrieves the operating mode (`getMode`)
- **PUT** - Updates the reader's operating mode (`setMode`)

6 example(s) exported from the spec, 7 proposed.

> **Note.** only SIMPLE and CUSTOM demonstrated. Proposed adds INVENTORY / PORTAL / CONVEYOR and GET response samples per mode type.

## Method folders

Examples are split by HTTP method:

```
cloud-mode/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `GET/default_configured_only.json` | GET | request | `default_configured_only` | in-spec | yes | Configured values only (default) |
| `GET/verbose_full.json` | GET | request | `verbose_full` | in-spec | yes | Entire configuration including defaults |
| `GET/inline.json` | GET | response 200 | `inline` | in-spec | yes |  |
| `GET/SIMPLE.json` | GET | response 200 | `SIMPLE` | proposed | yes | SIMPLE response sample |
| `GET/INVENTORY.json` | GET | response 200 | `INVENTORY` | proposed | yes | INVENTORY response sample |
| `GET/PORTAL.json` | GET | response 200 | `PORTAL` | proposed | yes | PORTAL response sample |
| `PUT/mode.json` | PUT | request | `mode` | in-spec | yes |  |
| `PUT/mode_default_FXR90.json` | PUT | request | `mode_default_FXR90` | in-spec | yes |  |
| `PUT/mode_TAG_FOCUS.json` | PUT | request | `mode_TAG_FOCUS` | in-spec | yes |  |
| `PUT/mode_INVENTORY.json` | PUT | request | `mode_INVENTORY` | proposed | yes | INVENTORY|
| `PUT/mode_PORTAL.json` | PUT | request | `mode_PORTAL` | proposed | yes | PORTAL — dock-door style |
| `PUT/mode_CONVEYOR.json` | PUT | request | `mode_CONVEYOR` | proposed | yes | CONVEYOR — fast single-stream |
| `PUT/mode_SIMPLE_minimal.json` | PUT | request | `mode_SIMPLE_minimal` | proposed | yes | Minimal SIMPLE body |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X GET "https://$READER/cloud/mode" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @GET/default_configured_only.json

curl -sk -X PUT "https://$READER/cloud/mode" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/mode.json

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

Then run `python ../validate_pack.py cloud-mode`.
