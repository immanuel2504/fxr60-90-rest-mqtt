# `/cloud/apps/{appname}/autostart`

- **PUT** — Autostart a user application (`set_autostartUserapp`)

Path: `appname` = `mylogger`.

## PUT examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `PUT/autostart_true.json` | request | `autostart_true` | `autostart` true |
| `PUT/autostart_false.json` | request | `autostart_false` | `autostart` false |
| `PUT/success.json` | response 200 | `success` | Empty string on success |
