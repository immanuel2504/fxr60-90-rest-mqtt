# `get_stackled`

REST: `GET /cloud/stack-led` → `cloud-stack-led/`

FXR60 Premium only.

Stable `command_id`: `req-get-stackled`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_stackled request |
| `response/default_state.json` | response | `default_state` | `cloud-stack-led/GET/default_state.json` | Reader controls LED |
| `response/green_med_solid.json` | response | `green_med_solid` | `cloud-stack-led/GET/green_med_solid.json` | Green, med, solid |
| `response/red_flash_countdown.json` | response | `red_flash_countdown` | `cloud-stack-led/GET/red_flash_countdown.json` | Red flash with countdown |
