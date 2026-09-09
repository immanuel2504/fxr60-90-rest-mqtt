# `/cloud/timeZone`

- **GET** — Current time zone (`get_timeZone`)
- **PUT** — Set time zone (`set_timeZone`)

## GET examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `GET/utc.json` | response 200 | `utc` | `timeZone` UTC |

## PUT examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `PUT/utc.json` | request | `utc` | Set `UTC` |
| `PUT/kolkata.json` | request | `kolkata` | Set `Kolkata` |
| `PUT/pacific.json` | request | `pacific` | Set `Pacific Time (US & Canada)` |
| `PUT/success.json` | response 200 | `success` | Empty string on success |
