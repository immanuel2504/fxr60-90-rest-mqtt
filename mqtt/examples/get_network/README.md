# `get_network`

REST: `GET /cloud/network` → `cloud-network/`

Stable `command_id`: `req-get-network`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_network request |
| `response/Ethernet.json` | response | `Ethernet` | `cloud-network/GET/Ethernet.json` | eth0 Interface |
| `response/WiFi.json` | response | `WiFi` | `cloud-network/GET/WiFi.json` | mlan0 Interface |
| `response/Bluetooth.json` | response | `Bluetooth` | `cloud-network/GET/Bluetooth.json` | bnep0 Interface |
| `response/WAN.json` | response | `WAN` | `cloud-network/GET/WAN.json` | wan0 Interface |
| `response/Hotspot.json` | response | `Hotspot` | `cloud-network/GET/Hotspot.json` | uap0 Interface |

