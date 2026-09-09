# `/cloud/network`

- **GET** — Network configuration (`get_network`)
- **PUT** — Update one interface (`set_network`)

## GET examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `GET/request_all.json` | request | `request_all` | Empty body, all interfaces |
| `GET/request_eth0.json` | request | `request_eth0` | `interface` eth0 |
| `GET/all_interfaces.json` | response 200 | `all_interfaces` | `hostName` and `networkInterface` |
| `GET/WiFi.json` | response 200 | `WiFi` | `mlan0` connected |
| `GET/Hotspot.json` | response 200 | `Hotspot` | `uap0` enabled |
| `GET/WAN.json` | response 200 | `WAN` | `wan0` |

## PUT examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `PUT/Network_ethernet_dhcp.json` | request | `Network_ethernet_dhcp` | `eth0` DHCP |
| `PUT/Network_ethernet_static.json` | request | `Network_ethernet_static` | `eth0` static |
| `PUT/Network_ethernet_static_8021x_tls.json` | request | `Network_ethernet_static_8021x_tls` | `eth0` 802.1X TLS static |
| `PUT/Network_ethernet_dhcp_8021x_tls.json` | request | `Network_ethernet_dhcp_8021x_tls` | `eth0` 802.1X TLS DHCP |
| `PUT/Network_ethernet_dhcp_8021x_ttls_mschapv2.json` | request | `Network_ethernet_dhcp_8021x_ttls_mschapv2` | `eth0` TTLS/MSCHAPV2 |
| `PUT/Network_ethernet_dhcp_8021x_peap_mschapv2.json` | request | `Network_ethernet_dhcp_8021x_peap_mschapv2` | `eth0` PEAP/MSCHAPV2 |
| `PUT/Network_wifi_static.json` | request | `Network_wifi_static` | `mlan0` static |
| `PUT/Network_wifi_dhcp.json` | request | `Network_wifi_dhcp` | `mlan0` DHCP |
| `PUT/Network_wifi_security_wpa2_personal.json` | request | `Network_wifi_security_wpa2_personal` | `mlan0` WPA2Personal |
| `PUT/Network_wifi_security_wpa3_personal.json` | request | `Network_wifi_security_wpa3_personal` | `mlan0` WPA3Personal |
| `PUT/Network_wifi_wpa2_enterprise_tls.json` | request | `Network_wifi_wpa2_enterprise_tls` | `mlan0` WPA2Enterprise TLS |
| `PUT/Network_wifi_wpa3_enterprise_ttls_mschapv2.json` | request | `Network_wifi_wpa3_enterprise_ttls_mschapv2` | `mlan0` WPA3Enterprise TTLS/MSCHAPV2 |
| `PUT/Network_wifi_wpa2_enterprise_peap_tls.json` | request | `Network_wifi_wpa2_enterprise_peap_tls` | `mlan0` WPA2Enterprise PEAP/TLS |
| `PUT/Network_wifi_wpa2_enterprise_ttls_tls.json` | request | `Network_wifi_wpa2_enterprise_ttls_tls` | `mlan0` WPA2Enterprise TTLS/TLS |
| `PUT/Network_wifi_wpa3_enterprise_peap_mschapv2.json` | request | `Network_wifi_wpa3_enterprise_peap_mschapv2` | `mlan0` WPA3Enterprise PEAP/MSCHAPV2 |
| `PUT/Network_bluetooth.json` | request | `Network_bluetooth` | `bnep0` |
| `PUT/Network_wan.json` | request | `Network_wan` | `wan0` psim |
| `PUT/Network_wan_esim.json` | request | `Network_wan_esim` | `wan0` esim |
| `PUT/Network_hotspot.json` | request | `Network_hotspot` | `uap0` |
| `PUT/success.json` | response 200 | `success` | Empty string on success |
