# `get_user_apps`

REST: `GET /cloud/apps` → `cloud-apps/`

MQTT command key: `get_userapps`

Stable `command_id`: `req-get-user-apps`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty `get_userapps` request |
| `response/none_installed.json` | response | `none_installed` | `cloud-apps/GET/none_installed.json` | No user applications |
| `response/sampleNew_sampleAntenna.json` | response | `sampleNew_sampleAntenna` | `cloud-apps/GET/sampleNew_sampleAntenna.json` | `sampleNew` and `sampleAntenna` |
