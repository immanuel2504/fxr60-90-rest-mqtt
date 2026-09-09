# `/cloud/eSimConfig`

- **GET** — eSIM identity and profiles (`get_eSimConfig`)
- **PUT** — Update an eSIM profile (`set_eSimConfig`)

## GET examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `GET/gnd1_gnd2.json` | response 200 | `gnd1_gnd2` | Profiles `gnd1` and `gnd2` |

## PUT examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `PUT/enable_profile.json` | request | `enable_profile` | `operation` enable |
| `PUT/disable_profile.json` | request | `disable_profile` | `operation` disable |
| `PUT/add_profile.json` | request | `add_profile` | `operation` add with `activationID` |
| `PUT/delete_profile.json` | request | `delete_profile` | `operation` delete |
| `PUT/success.json` | response 200 | `success` | Empty string on success |
