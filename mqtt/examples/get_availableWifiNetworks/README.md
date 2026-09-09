# `get_availableWifiNetworks`

REST: `GET /cloud/wifiNetworks` → `cloud-wifinetworks/`

Stable `command_id`: `req-get-availableWifiNetworks`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_availableWifiNetworks request |
| `response/visible_networks.json` | response | `visible_networks` | `cloud-wifinetworks/GET/visible_networks.json` | Visible access points with `essid` and `signalStrength` |
