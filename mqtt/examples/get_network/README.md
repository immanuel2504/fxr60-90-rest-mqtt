# `get_network`

REST: `GET /cloud/network` → `cloud-network/`

Stable `command_id`: `req-get-network`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `cloud-network/GET/request_all.json` | Empty payload, all interfaces |
| `request/request_eth0.json` | request | `request_eth0` | `cloud-network/GET/request_eth0.json` | `interface` eth0 |
| `response/all_interfaces.json` | response | `all_interfaces` | `cloud-network/GET/all_interfaces.json` | `hostName` and `networkInterface` |
| `response/WiFi.json` | response | `WiFi` | `cloud-network/GET/WiFi.json` | `mlan0` connected |
| `response/Hotspot.json` | response | `Hotspot` | `cloud-network/GET/Hotspot.json` | `uap0` enabled |
| `response/WAN.json` | response | `WAN` | `cloud-network/GET/WAN.json` | `wan0` |
