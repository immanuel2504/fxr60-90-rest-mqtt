# `set_logs`

REST: `PUT /cloud/logs` → `cloud-logs/`

Stable `command_id`: `req-set-logs`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/logs.json` | request | `logs` | `cloud-logs/PUT/logs.json` | Set reader_gateway DEBUG and enable radioPacketLog |
| `request/radioPacketLog_on.json` | request | `radioPacketLog_on` | `cloud-logs/PUT/radioPacketLog_on.json` | Enable radioPacketLog |
| `response/success.json` | response | `success` | `—` | Command succeeded |
