# `get_appled`

REST: `GET /cloud/app-led` → `cloud-app-led/`

Stable `command_id`: `req-get-appled`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_appled request |
| `response/default_state.json` | response | `default_state` | `cloud-app-led/GET/default_state.json` | LED under reader control |
| `response/overridden_state.json` | response | `overridden_state` | `cloud-app-led/GET/overridden_state.json` | LED overridden by PUT /cloud/app-led |

