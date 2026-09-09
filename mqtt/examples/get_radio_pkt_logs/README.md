# `get_radio_pkt_logs`

REST: `GET /cloud/logs/radioPacketLog` → `cloud-logs-radiopacketlog/`

MQTT command key: `get_logs_radioPacketLog`

Stable `command_id`: `req-get-radio-pkt-logs`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_logs_radioPacketLog request |
| `response/radio_packet.json` | response | `radio_packet` | `cloud-logs-radiopacketlog/GET/radio_packet.json` | radioPktLog.tar.gz archive |
