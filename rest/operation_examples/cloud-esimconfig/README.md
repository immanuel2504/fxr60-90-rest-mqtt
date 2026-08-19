# `/cloud/eSimConfig`

- **GET** - Gets the eSIM configuration (`getEsimConfig`)
- **PUT** - Sets the eSIM configuration (`setEsimConfig`)

## Reviewed GET

| File | Example name | Summary |
|---|---|---|
| `GET/profiles_present.json` | `profiles_present` | Two profiles |

`no_profiles` removed.

## Method folders

```
cloud-esimconfig/
  GET/     # GET response examples
  PUT/     # PUT request examples (not reviewed yet)
```

| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `GET/profiles_present.json` | GET | response 200 | `profiles_present` | reviewed | yes | Two profiles |
| `PUT/eSimConfig_enable.json` | PUT | request | `eSimConfig_enable` | in-spec | yes | eSimConfig enable |
| `PUT/eSimConfig_disable.json` | PUT | request | `eSimConfig_disable` | reviewed | yes | eSimConfig disable |
| `PUT/eSimConfig_add.json` | PUT | request | `eSimConfig_add` | in-spec | yes | eSimConfig add |
| `PUT/eSimConfig_delete.json` | PUT | request | `eSimConfig_delete` | in-spec | yes | eSimConfig delete |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X GET "https://$READER/cloud/eSimConfig" \
  -H "Authorization: Bearer $TOKEN"
```
