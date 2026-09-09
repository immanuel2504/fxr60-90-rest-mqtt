# `/cloud/stack-led`

- **GET** — Stack LED state (`get_stackled`). FXR60 Premium only.
- **PUT** — Set color, brightness, flash, and seconds (`set_stackled`).

## GET examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `GET/default_state.json` | response 200 | `default_state` | Reader controls LED |
| `GET/green_med_solid.json` | response 200 | `green_med_solid` | Green, med, solid |
| `GET/red_flash_countdown.json` | response 200 | `red_flash_countdown` | Red flash with countdown |

## PUT examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `PUT/red_high_flash.json` | request | `red_high_flash` | Red, high, flashing |
| `PUT/green_solid.json` | request | `green_solid` | Green solid |
| `PUT/amber_med_flash.json` | request | `amber_med_flash` | Amber, med, flashing |
