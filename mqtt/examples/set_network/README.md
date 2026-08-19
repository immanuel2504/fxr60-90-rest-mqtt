# `set_network`

REST: `PUT /cloud/network` → `cloud-network/`

Stable `command_id`: `req-set-network`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/Network_ethernet_dhcp.json` | request | `Network_ethernet_dhcp` | `cloud-network/PUT/Network_ethernet_dhcp.json` | Ethernet — DHCP |
| `request/Network_ethernet_static.json` | request | `Network_ethernet_static` | `cloud-network/PUT/Network_ethernet_static.json` | Ethernet — static IP |
| `request/Network_ethernet_static_8021x_tls.json` | request | `Network_ethernet_static_8021x_tls` | `cloud-network/PUT/Network_ethernet_static_8021x_tls.json` | Ethernet — 802.1X (TLS).Similarly applicable for TTLS/TLS, PEAP/TTLS, TTLS/MSCHAPV2, PEAP/MSCHAPV2. |
| `request/Network_ethernet_dhcp_8021x_tls.json` | request | `Network_ethernet_dhcp_8021x_tls` | `cloud-network/PUT/Network_ethernet_dhcp_8021x_tls.json` | Ethernet — 802.1X (TLS) |
| `request/Network_ethernet_dhcp_8021x_ttls_mschapv2.json` | request | `Network_ethernet_dhcp_8021x_ttls_mschapv2` | `cloud-network/PUT/Network_ethernet_dhcp_8021x_ttls_mschapv2.json` | Ethernet — 802.1X (TTLS/MSCHAPV2) |
| `request/Network_ethernet_dhcp_8021x_peap_mschapv2.json` | request | `Network_ethernet_dhcp_8021x_peap_mschapv2` | `cloud-network/PUT/Network_ethernet_dhcp_8021x_peap_mschapv2.json` | Ethernet — 802.1X (PEAP/MSCHAPV2) |
| `request/Network_wifi_static.json` | request | `Network_wifi_static` | `cloud-network/PUT/Network_wifi_static.json` | WiFi — static IP .Similarly applicable for WPA3Personal, WPA2Enterprise, WPA3Enterprise |
| `request/Network_wifi_dhcp.json` | request | `Network_wifi_dhcp` | `cloud-network/PUT/Network_wifi_dhcp.json` | WiFi — WPA3 Personal.Similarly applicable for WPA2Personal,WPA2Enterprise, WPA3Enterprise, |
| `request/Network_wifi_security_wpa2_personal.json` | request | `Network_wifi_security_wpa2_personal` | `cloud-network/PUT/Network_wifi_security_wpa2_personal.json` | WiFi — WPA2 Personal |
| `request/Network_wifi_security_wpa3_personal.json` | request | `Network_wifi_security_wpa3_personal` | `cloud-network/PUT/Network_wifi_security_wpa3_personal.json` | WiFi — WPA3 Personal |
| `request/Network_wifi_wpa2_enterprise_tls.json` | request | `Network_wifi_wpa2_enterprise_tls` | `cloud-network/PUT/Network_wifi_wpa2_enterprise_tls.json` | WiFi — WPA2 Enterprise (TLS).Similary applicable for WPA3 Enterprise(WPA3Enterprise) |
| `request/Network_wifi_wpa3_enterprise_ttls_mschapv2.json` | request | `Network_wifi_wpa3_enterprise_ttls_mschapv2` | `cloud-network/PUT/Network_wifi_wpa3_enterprise_ttls_mschapv2.json` | WiFi — WPA3 Enterprise (TTLS/MSCHAPV2).similarly applicable for WPA2 Enterprise (WPA2Enterprise) |
| `request/Network_wifi_wpa2_enterprise_peap_tls.json` | request | `Network_wifi_wpa2_enterprise_peap_tls` | `cloud-network/PUT/Network_wifi_wpa2_enterprise_peap_tls.json` | WiFi — WPA2 Enterprise (PEAP/TLS).Similarly applicable for WPA3 Enterprise(WPA3Enterprise) |
| `request/Network_wifi_wpa2_enterprise_ttls_tls.json` | request | `Network_wifi_wpa2_enterprise_ttls_tls` | `cloud-network/PUT/Network_wifi_wpa2_enterprise_ttls_tls.json` | WiFi — WPA2 Enterprise (TTLS/TLS).Similarly applicable for WPA3 Enterprise(WPA3Enterprise) |
| `request/Network_wifi_wpa3_enterprise_peap_mschapv2.json` | request | `Network_wifi_wpa3_enterprise_peap_mschapv2` | `cloud-network/PUT/Network_wifi_wpa3_enterprise_peap_mschapv2.json` | WiFi — WPA3 Enterprise (PEAP/MSCHAPV2).Similarly applicable for WPA2 Enterprise(WPA2Enterprise) |
| `request/Network_bluetooth.json` | request | `Network_bluetooth` | `cloud-network/PUT/Network_bluetooth.json` | Bluetooth PAN |
| `request/Network_wan.json` | request | `Network_wan` | `cloud-network/PUT/Network_wan.json` | WAN — cellular (psim) |
| `request/Network_hotspot.json` | request | `Network_hotspot` | `cloud-network/PUT/Network_hotspot.json` | WiFi Hotspot (uap0) |
| `response/success.json` | response | `success` | `cloud-network/PUT/success.json` | Empty string on success |

