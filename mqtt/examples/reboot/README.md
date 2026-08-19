# `reboot`

REST: `PUT /cloud/reboot` → `cloud-reboot/`

Stable `command_id`: `req-reboot`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `response/success.json` | response | `success` | `cloud-reboot/PUT/success.json` | Empty string on success (REST) / success envelope (MQTT) |

No request payload. NEED LIVE TEST — reboot is disruptive.
