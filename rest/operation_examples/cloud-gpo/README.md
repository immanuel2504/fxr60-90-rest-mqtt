# `/cloud/gpo`

- **GET** — Current GPO pin states (`get_gpoStatus`)
- **PUT** — Set one GPO pin (`set_gpo`)

## GET examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `GET/gpo_status.json` | response 200 | `gpo_status` | All pins LOW |

## PUT examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `PUT/gpo.json` | request | `gpo` | Port 3 HIGH |
| `PUT/success.json` | response 200 | `success` | Empty string on success |
