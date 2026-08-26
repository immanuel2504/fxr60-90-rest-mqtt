# `get_config`

REST: `GET /cloud/config` → `cloud-config/`

Stable `command_id`: `req-get-config`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_config request |
| `response/full_configuration.json` | response | `full_configuration` | `cloud-config/GET/full_configuration.json` | Full configuration with GPIO-LED and xml profile |
| `response/gpio_led_not_configured.json` | response | `gpio_led_not_configured` | `cloud-config/GET/gpio_led_not_configured.json` | GPIO-LED not configured (empty object) |

