# `/cloud/network`

- **GET** - Retrieves reader network configuration (`getNetwork`)
- **PUT** - Updates reader network configuration (`updateNetwork`)

22 example(s) exported from the spec, 0 proposed. **5 fail schema validation.**

> **Note.** SCHEMA DEFECT: IPV6.prefix is `type: string` but examples use integer 64. Fix the schema (`type: integer`). Exported examples keep the integer form.

## Method folders

Examples are split by HTTP method:

```
cloud-network/
  GET/     # GET request/response examples
  PUT/     # PUT request/response examples
  DELETE/  # when present
```
| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `GET/Ethernet.json` | GET | response 200 | `Ethernet` | in-spec | NO | eth0 Interface — $.networkInterface.eth0.IPV6.prefix: expected string, got int |
| `GET/WiFi.json` | GET | response 200 | `WiFi` | in-spec | NO | mlan0 Interface — $.networkInterface.mlan0.IPV6.prefix: expected string, got int |
| `GET/Bluetooth.json` | GET | response 200 | `Bluetooth` | in-spec | yes | bnep0 Interface |
| `GET/WAN.json` | GET | response 200 | `WAN` | in-spec | yes | wan0 Interface |
| `GET/Hotspot.json` | GET | response 200 | `Hotspot` | in-spec | yes | uap0 Interface |
| `PUT/Network_ethernet_dhcp.json` | PUT | request | `Network_ethernet_dhcp` | in-spec | yes | Ethernet — DHCP |
| `PUT/Network_ethernet_static.json` | PUT | request | `Network_ethernet_static` | in-spec | NO | Ethernet — static IP — $.eth0.IPV6.prefix: expected string, got int |
| `PUT/Network_ethernet_static_8021x_tls.json` | PUT | request | `Network_ethernet_static_8021x_tls` | in-spec | NO | Ethernet — 802.1X (TLS).Similarly applicable for TTLS/TLS, PEAP/TTLS, TTLS/MSCHAPV2, PEAP/MSCHAPV2. — $.eth0.IPV6.prefix: expected string, got int |
| `PUT/Network_ethernet_dhcp_8021x_tls.json` | PUT | request | `Network_ethernet_dhcp_8021x_tls` | in-spec | yes | Ethernet — 802.1X (TLS) |
| `PUT/Network_ethernet_dhcp_8021x_ttls_mschapv2.json` | PUT | request | `Network_ethernet_dhcp_8021x_ttls_mschapv2` | in-spec | yes | Ethernet — 802.1X (TTLS/MSCHAPv2) |
| `PUT/Network_ethernet_dhcp_8021x_peap_mschapv2.json` | PUT | request | `Network_ethernet_dhcp_8021x_peap_mschapv2` | in-spec | yes | Ethernet — 802.1X (PEAP/MSCHAPv2) |
| `PUT/Network_wifi_static.json` | PUT | request | `Network_wifi_static` | in-spec | NO | WiFi — static IP .Similarly applicable for WPA3Personal, WPA2Enterprise, WPA3Enterprise — $.mlan0.IPV6.prefix: expected string, got int |
| `PUT/Network_wifi_dhcp.json` | PUT | request | `Network_wifi_dhcp` | in-spec | yes | WiFi — WPA3 Personal.Similarly applicable for WPA2Personal,WPA2Enterprise, WPA3Enterprise, |
| `PUT/Network_wifi_security_wpa2_personal.json` | PUT | request | `Network_wifi_security_wpa2_personal` | in-spec | yes | WiFi — WPA2 Personal |
| `PUT/Network_wifi_wpa2_enterprise_tls.json` | PUT | request | `Network_wifi_wpa2_enterprise_tls` | in-spec | yes | WiFi — WPA2 Enterprise (TLS).Similary applicable for WPA3 Enterprise(WPA3Enterprise) |
| `PUT/Network_wifi_wpa3_enterprise_ttls_mschapv2.json` | PUT | request | `Network_wifi_wpa3_enterprise_ttls_mschapv2` | in-spec | yes | WiFi — WPA3 Enterprise (TTLS/MSCHAPv2).similarly applicable for WPA2 Enterprise (WPA2Enterprise) |
| `PUT/Network_wifi_wpa2_enterprise_peap_tls.json` | PUT | request | `Network_wifi_wpa2_enterprise_peap_tls` | in-spec | yes | WiFi — WPA2 Enterprise (PEAP/TLS).Similarly applicable for WPA3 Enterprise(WPA3Enterprise) |
| `PUT/Network_wifi_wpa2_enterprise_ttls_tls.json` | PUT | request | `Network_wifi_wpa2_enterprise_ttls_tls` | in-spec | yes | WiFi — WPA2 Enterprise (TTLS/TLS).Similarly applicable for WPA3 Enterprise(WPA3Enterprise) |
| `PUT/Network_wifi_wpa3_enterprise_peap_mschapv2.json` | PUT | request | `Network_wifi_wpa3_enterprise_peap_mschapv2` | in-spec | yes | WiFi — WPA3 Enterprise (PEAP/MSCHAPv2).Similarly applicable for WPA2 Enterprise(WPA2Enterprise) |
| `PUT/Network_bluetooth.json` | PUT | request | `Network_bluetooth` | in-spec | yes | Bluetooth PAN |
| `PUT/Network_wan.json` | PUT | request | `Network_wan` | in-spec | yes | WAN — cellular (psim) |
| `PUT/Network_hotspot.json` | PUT | request | `Network_hotspot` | in-spec | yes | WiFi Hotspot (uap0) |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X GET "https://$READER/cloud/network" \
  -H "Authorization: Bearer $TOKEN"

curl -sk -X PUT "https://$READER/cloud/network" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/Network_ethernet_dhcp.json

```

## Folding a file back into the spec

Add under the operation `examples:` map in `FXR90-rest-api.yaml`:

```yaml
      examples:
        <example_name>:
          summary: <summary from the table>
          value:
            # contents of the .json file
```

Then run `python ../validate_pack.py cloud-network`.
