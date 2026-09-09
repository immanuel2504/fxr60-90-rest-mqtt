# `get_bleConfig`

REST: `GET /cloud/bleConfig` → `cloud-bleconfig/`

MQTT command key: `get_bleConfig`

Stable `command_id`: `req-get-bleConfig`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty `get_bleConfig` request |
| `response/disabled.json` | response | `disabled` | `cloud-bleconfig/GET/disabled.json` | `ble.enable` false |
| `response/all_protocols.json` | response | `all_protocols` | `cloud-bleconfig/GET/all_protocols.json` | All protocols and filters |
