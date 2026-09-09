# `get_hostname`

REST: `GET /cloud/hostName` → `cloud-hostname/`

MQTT command key: `get_hostName`

Stable `command_id`: `req-get-hostname`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_hostName request |
| `response/configured.json` | response | `configured` | `cloud-hostname/GET/configured.json` | Current hostname |
