# Example summary titles — `/cloud/network`

`PUT/` example names and summary titles are copied **verbatim** from the developer
OpenAPI (`rest/RestDeveloperfile.yaml` → `PUT /cloud/network` → `examples`).
Do not edit here — change the developer file and re-copy.

**NEED LIVE TEST — 802.1X enterprise bodies.** Only `Network_wifi_wpa2_enterprise_tls`
was captured from a reader (lab AP `Vulcan_WPA2_5_ENT_802.1x`, installed client cert
`COMMON`). The four PEAP/TTLS variants and the two `eth0` 802.1X TLS bodies were
written by hand and reshaped on 2026-08-12 to match that captured body — placeholder
`CorpNetwork` / `my-client-cert` values were replaced with the lab SSIDs from the
`GET /cloud/wifiNetworks` example and the `COMMON` cert from `GET /cloud/certificates`,
and the missing `security.enable: true` was added to the four Wi-Fi bodies. The shape is
now consistent with the one body known to work, but none of the six has been confirmed
against a reader with an enterprise AP. Two schema gaps remain open (see the tracker):
`security.enable` is undeclared, and `mlan0.enable` is declared inside `accesspoint`
though every example sends it one level up.

## GET

### `GET/request_all.json`

| Field | Value |
|---|---|
| **Example name** | `get_network_all` |
| **Summary title** | `Request — all interfaces` |

### `GET/request_eth0.json`

| Field | Value |
|---|---|
| **Example name** | `get_network_eth0` |
| **Summary title** | `Request — Ethernet (eth0)` |

### `GET/WiFi.json`

| Field | Value |
|---|---|
| **Example name** | `WiFi` |
| **Summary title** | `WiFi (mlan0) — WPA2 Enterprise (PEAP/MSCHAPV2)` |

### `GET/WAN.json`

| Field | Value |
|---|---|
| **Example name** | `wan_fxr90` |
| **Summary title** | `FXR90 WAN (wan0) — esim with apn — not on FXR60` |

### `GET/Hotspot.json`

| Field | Value |
|---|---|
| **Example name** | `Hotspot` |
| **Summary title** | `Hotspot (uap0) — VULCAN_HOTSPOT` |

## PUT

### `PUT/Network_ethernet_dhcp.json`

| Field | Value |
|---|---|
| **Example name** | `Network_ethernet_dhcp` |
| **Summary title** | `Ethernet — DHCP` |

### `PUT/Network_ethernet_static.json`

| Field | Value |
|---|---|
| **Example name** | `Network_ethernet_static` |
| **Summary title** | `Ethernet — static IP` |

### `PUT/Network_ethernet_static_8021x_tls.json`

| Field | Value |
|---|---|
| **Example name** | `Network_ethernet_static_8021x_tls` |
| **Summary title** | `Ethernet — 802.1X (TLS).Similarly applicable for TTLS/TLS, PEAP/TTLS, TTLS/MSCHAPV2, PEAP/MSCHAPV2.` |

### `PUT/Network_ethernet_dhcp_8021x_tls.json`

| Field | Value |
|---|---|
| **Example name** | `Network_ethernet_dhcp_8021x_tls` |
| **Summary title** | `Ethernet — 802.1X (TLS)` |

### `PUT/Network_ethernet_dhcp_8021x_ttls_mschapv2.json`

| Field | Value |
|---|---|
| **Example name** | `Network_ethernet_dhcp_8021x_ttls_mschapv2` |
| **Summary title** | `Ethernet — 802.1X (TTLS/MSCHAPV2)` |

### `PUT/Network_ethernet_dhcp_8021x_peap_mschapv2.json`

| Field | Value |
|---|---|
| **Example name** | `Network_ethernet_dhcp_8021x_peap_mschapv2` |
| **Summary title** | `Ethernet — 802.1X (PEAP/MSCHAPV2)` |

### `PUT/Network_wifi_static.json`

| Field | Value |
|---|---|
| **Example name** | `Network_wifi_static` |
| **Summary title** | `WiFi — static IP .Similarly applicable for WPA3Personal, WPA2Enterprise, WPA3Enterprise` |

### `PUT/Network_wifi_security_wpa2_personal.json`

| Field | Value |
|---|---|
| **Example name** | `Network_wifi_security_wpa2_personal` |
| **Summary title** | `WiFi — WPA2 Personal` |

### `PUT/Network_wifi_security_wpa3_personal.json`

| Field | Value |
|---|---|
| **Example name** | `Network_wifi_security_wpa3_personal` |
| **Summary title** | `WiFi — WPA3 Personal` |

### `PUT/Network_wifi_wpa2_enterprise_tls.json`

| Field | Value |
|---|---|
| **Example name** | `Network_wifi_wpa2_enterprise_tls` |
| **Summary title** | `WiFi — WPA2 Enterprise (TLS).Similary applicable for WPA3 Enterprise(WPA3Enterprise)` |

### `PUT/Network_wifi_wpa3_enterprise_ttls_mschapv2.json`

| Field | Value |
|---|---|
| **Example name** | `Network_wifi_wpa3_enterprise_ttls_mschapv2` |
| **Summary title** | `WiFi — WPA3 Enterprise (TTLS/MSCHAPV2).similarly applicable for WPA2 Enterprise (WPA2Enterprise)` |

### `PUT/Network_wifi_wpa2_enterprise_peap_tls.json`

| Field | Value |
|---|---|
| **Example name** | `Network_wifi_wpa2_enterprise_peap_tls` |
| **Summary title** | `WiFi — WPA2 Enterprise (PEAP/TLS).Similarly applicable for WPA3 Enterprise(WPA3Enterprise)` |

### `PUT/Network_wifi_wpa2_enterprise_ttls_tls.json`

| Field | Value |
|---|---|
| **Example name** | `Network_wifi_wpa2_enterprise_ttls_tls` |
| **Summary title** | `WiFi — WPA2 Enterprise (TTLS/TLS).Similarly applicable for WPA3 Enterprise(WPA3Enterprise)` |

### `PUT/Network_wifi_wpa3_enterprise_peap_mschapv2.json`

| Field | Value |
|---|---|
| **Example name** | `Network_wifi_wpa3_enterprise_peap_mschapv2` |
| **Summary title** | `WiFi — WPA3 Enterprise (PEAP/MSCHAPV2).Similarly applicable for WPA2 Enterprise(WPA2Enterprise)` |

### `PUT/Network_bluetooth.json`

| Field | Value |
|---|---|
| **Example name** | `Network_bluetooth` |
| **Summary title** | `Bluetooth PAN` |

### `PUT/Network_wan.json`

| Field | Value |
|---|---|
| **Example name** | `Network_wan` |
| **Summary title** | `WAN — cellular (psim)` |

### `PUT/Network_wan_esim.json`

| Field | Value |
|---|---|
| **Example name** | `Network_wan_esim` |
| **Summary title** | `WAN — cellular (esim)` |

### `PUT/Network_hotspot.json`

| Field | Value |
|---|---|
| **Example name** | `Network_hotspot` |
| **Summary title** | `Hotspot` |

## PUT response

### `PUT/success.json`

| Field | Value |
|---|---|
| **Example name** | `success` |
| **Summary title** | `Empty string on success` |
| **HTTP status** | `200` |

