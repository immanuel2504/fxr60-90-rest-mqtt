# `get_gpi_status`

REST: `GET /cloud/gpi` → `cloud-gpi/`

MQTT command key: `get_gpiStatus`

Stable `command_id`: `req-get-gpi-status`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_gpiStatus request |
| `response/gpi_status.json` | response | `gpi_status` | `cloud-gpi/GET/gpi_status.json` | All pins HIGH |
