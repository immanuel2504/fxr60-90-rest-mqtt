# `set_logs`

REST: `PUT /cloud/logs` → `cloud-logs/`

Stable `command_id`: `req-set-logs`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/logs.json` | request | `logs` | `cloud-logs/PUT/logs.json` | DEBUG radio_control and cloud_agent |
| `response/success.json` | response | `success` | `—` | Command succeeded |

NEED LIVE TEST on a reader (body accepted + effect visible via get_logs).
