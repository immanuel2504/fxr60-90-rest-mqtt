# `/cloud/stack-led`

- **GET** - Retrieves stack LED state (`getStackled`)
- **PUT** - Updates stack LED state (`setStackled`)

2 example(s) exported from the spec, 3 proposed.

## Method folders

Examples are split by HTTP method:

```
cloud-stack-led/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `GET/solid_green.json` | GET | response 200 | `solid_green` | proposed | yes | Solid green |
| `GET/flashing_red_with_countdown.json` | GET | response 200 | `flashing_red_with_countdown` | proposed | yes | Flashing red alert with countdown |
| `PUT/red_high_alert.json` | PUT | request | `red_high_alert` | in-spec | yes | Color:Red, Brightness:High, Flashing |
| `PUT/green_solid.json` | PUT | request | `green_solid` | in-spec | yes | Color:Green, Brightness:Low(Default), Solid |
| `PUT/amber_med_flash.json` | PUT | request | `amber_med_flash` | proposed | yes | Extra color/brightness |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X GET "https://$READER/cloud/stack-led" \
  -H "Authorization: Bearer $TOKEN"

curl -sk -X PUT "https://$READER/cloud/stack-led" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/red_high_alert.json

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

Then run `python ../validate_pack.py cloud-stack-led`.
