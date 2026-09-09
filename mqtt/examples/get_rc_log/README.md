# `get_rc_log`

REST: `GET /cloud/logs/RcLog` → `cloud-logs-rclog/`

MQTT command key: `get_logs_rcLog`

Stable `command_id`: `req-get-rc-log`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_logs_rcLog request |
| `response/rc_log.json` | response | `rc_log` | `cloud-logs-rclog/GET/rc_log.json` | rcLog.tar.gz archive |
