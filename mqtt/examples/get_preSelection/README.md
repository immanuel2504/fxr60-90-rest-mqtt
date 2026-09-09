# `get_preSelection`

REST: `GET /cloud/preSelection` → `cloud-preselection/`

Stable `command_id`: `req-get-preSelection`

GET returns a string: `"enabled"` or `"disabled"`. PUT uses a boolean.

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_preSelection request |
| `response/disabled.json` | response | `disabled` | `cloud-preselection/GET/disabled.json` | preSelection disabled |
