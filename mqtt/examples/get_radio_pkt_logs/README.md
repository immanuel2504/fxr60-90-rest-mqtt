# `get_radio_pkt_logs`

REST: `GET /cloud/logs/radioPacketLog` → `cloud-logs-radiopacketlog/`

Stable `command_id`: `req-get-radio-pkt-logs`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_radio_pkt_logs request |
| `response/download.json` | response | `download` | `cloud-logs-radiopacketlog/GET/download.json` | Radio packet log archive |

NEED LIVE TEST: enable radioPacketLog first via set_logs / PUT /cloud/logs.
