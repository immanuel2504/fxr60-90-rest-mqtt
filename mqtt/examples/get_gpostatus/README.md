# `get_gpostatus`

REST: `GET /cloud/gpo` → `cloud-gpo/`

MQTT command key: `get_gpoStatus`

Stable `command_id`: `req-get-gpostatus`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_gpoStatus request |
| `response/gpo_status.json` | response | `gpo_status` | `cloud-gpo/GET/gpo_status.json` | All pins LOW |
