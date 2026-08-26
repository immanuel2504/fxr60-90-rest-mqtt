# `get_network`

REST: `GET /cloud/network` → `cloud-network/`

Stable `command_id`: `req-get-network`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `cloud-network/GET/request_all.json` | All interfaces (empty payload) |
| `request/eth0.json` | request | `eth0` | `cloud-network/GET/request_eth0.json` | Ethernet only |
| `response/Ethernet.json` | response | `Ethernet` | `cloud-network/GET/Ethernet.json` | eth0 Interface |
| `response/WiFi.json` | response | `WiFi` | `cloud-network/GET/WiFi.json` | WiFi (mlan0) — WPA2 Enterprise (PEAP/MSCHAPV2) |
| `response/Bluetooth.json` | response | `Bluetooth` | `cloud-network/GET/Bluetooth.json` | bnep0 Interface |
| `response/WAN.json` | response | `WAN` | `cloud-network/GET/WAN.json` | FXR90 WAN (wan0) — esim with apn — not on FXR60 |
| `response/Hotspot.json` | response | `Hotspot` | `cloud-network/GET/Hotspot.json` | Hotspot (uap0) — VULCAN_HOTSPOT |

