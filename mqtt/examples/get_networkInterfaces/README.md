# `get_networkInterfaces`

REST: `GET /cloud/networkInterfaces` → `cloud-networkinterfaces/`

Stable `command_id`: `req-get-networkInterfaces`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_networkInterfaces request |
| `response/with_uap0.json` | response | `with_uap0` | `cloud-networkinterfaces/GET/with_uap0.json` | `eth0`, `mlan0`, `bnep0`, `blescan`, `uap0` |
| `response/with_wan0.json` | response | `with_wan0` | `cloud-networkinterfaces/GET/with_wan0.json` | `eth0`, `mlan0`, `bnep0`, `wan0` |
