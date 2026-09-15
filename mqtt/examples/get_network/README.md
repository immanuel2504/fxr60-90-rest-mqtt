# `get_network`

REST: `GET /cloud/network` → `cloud-network/`

| File | Direction | Example name | REST map | Summary |
|---|---|---|---|---|
| `request/all_interfaces.json` | request | `all_interfaces` | `cloud-network/GET/query_all_interfaces.json` | Empty payload, all interfaces |
| `request/interface_eth0.json` | request | `interface_eth0` | `cloud-network/GET/interface_eth0.json` | `interface` eth0 |
| `request/interface_bnep0.json` | request | `interface_bnep0` | `cloud-network/GET/interface_bnep0.json` | `interface` bnep0 |
| `response/all_interfaces.json` | response | `all_interfaces` | `cloud-network/GET/all_interfaces.json` | `hostName` and `networkInterface` |
| `response/WiFi.json` | response | `WiFi` | `cloud-network/GET/WiFi.json` | `mlan0` connected |
| `response/Hotspot.json` | response | `Hotspot` | `cloud-network/GET/Hotspot.json` | `uap0` enabled |
| `response/WAN.json` | response | `WAN` | `cloud-network/GET/WAN.json` | `wan0` |
