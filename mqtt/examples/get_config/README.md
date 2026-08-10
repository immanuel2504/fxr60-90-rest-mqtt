# `get_config`

REST: `GET /cloud/config` → `cloud-config/`

Stable `command_id`: `req-get-config`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_config request |
| `response/inline.json` | response | `inline` | `cloud-config/GET/inline.json` |  |
| `response/gpio_led_not_configured.json` | response | `gpio_led_not_configured` | `cloud-config/GET/gpio_led_not_configured.json` | Valid today — GPIO-LED NOT_CONFIGURED string (in-spec {} is invalid) |

