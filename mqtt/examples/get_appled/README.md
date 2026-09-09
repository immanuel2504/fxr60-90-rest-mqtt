# `get_appled`

REST: `GET /cloud/app-led` → `cloud-app-led/`

Stable `command_id`: `req-get-appled`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_appled request |
| `response/default_state.json` | response | `default_state` | `cloud-app-led/GET/default_state.json` | Reader controls LED |
| `response/non_default_state.json` | response | `non_default_state` | `cloud-app-led/GET/non_default_state.json` | App controls LED |
