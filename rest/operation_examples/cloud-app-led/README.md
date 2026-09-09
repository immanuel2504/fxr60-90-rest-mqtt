# `/cloud/app-led`

- **GET** — Returns `DEFAULT` or `NON_DEFAULT` (`get_appled`).
- **PUT** — Sets color, flash, and seconds (`set_appled`).

## GET examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `GET/default_state.json` | response 200 | `default_state` | Reader controls LED |
| `GET/non_default_state.json` | response 200 | `non_default_state` | App controls LED |

## PUT examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `PUT/amber_flash_60s.json` | request | `amber_flash_60s` | Amber flash 60 seconds |
| `PUT/red_flash_indefinite.json` | request | `red_flash_indefinite` | Red flash indefinite |
| `PUT/green_solid_10s.json` | request | `green_solid_10s` | Green solid 10 seconds |
| `PUT/off.json` | request | `off` | LED off |
| `PUT/success.json` | response 200 | `success` | Empty string on success |
