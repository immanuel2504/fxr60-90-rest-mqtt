# `set_preSelection`

REST: `PUT /cloud/preSelection` → `cloud-preselection/`

Stable `command_id`: `req-set-preSelection`

PUT sends a boolean (`true` / `false`). GET returns `"enabled"` / `"disabled"`.

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/enable.json` | request | `enable` | `cloud-preselection/PUT/enable.json` | Enable preSelection |
| `response/success.json` | response | `success` | `—` | Command succeeded |
