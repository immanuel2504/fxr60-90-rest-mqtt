Updates reader network configuration for **one interface per request**.

> [!warning]
> Cellular interface `wan0` is supported on **FXR90 only**. It is not present on FXR60. Do not send a `wan0` body to an FXR60 reader.

> [!important]
> `uap0` (hotspot) and `mlan0` (Wi-Fi client) share one Wi-Fi radio and cannot be active at the same time. To enable hotspot, disable `mlan0` first, then enable `uap0`. To enable Wi-Fi client, disable `uap0` first, then enable `mlan0`. Sending `uap0` with `enable: true` while `mlan0` is connected is rejected (for example `Disable WiFi to enable Hotspot`). Configure them in separate requests.

Configure:

- Ethernet (`eth0`) — DHCP, static IPv4/IPv6 addressing, and 802.1X security
- Wi-Fi station (`mlan0`) — DHCP, static addressing, access point connection, and WPA2/WPA3/Enterprise security
- Bluetooth PAN (`bnep0`) — discoverability, pairing, and DHCP address pool
- Cellular WAN (`wan0`) — SIM selection, APN, network type preference, and IPv6 — **FXR90 only**
- Wi-Fi hotspot (`uap0`) — SSID, password, country code, and security type

Typical uses: join a Wi-Fi access point, switch Ethernet from DHCP to static IP, enable or disable an interface, set cellular APN/SIM (**FXR90 / `wan0` only**), or provision a hotspot.

## Endpoint details

| Property | Value |
| --- | --- |
| Pattern name | Network Configuration |
| REST endpoint | `PUT /cloud/network` |
| Communication type | Client to device (HTTP request/response) |
| Applies to | FXR60 / FXR90 (`wan0` = FXR90 only) |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Supported interface keys | `eth0`, `mlan0`, `bnep0`, `wan0` (**FXR90 only**), `uap0` |
| Supported Wi-Fi security types | `WPA2Personal`, `WPA2Enterprise`, `WPA3Personal`, `WPA3Enterprise` |
| Supported 802.1X outer methods | `TLS`, `TTLS`, `PEAP` |
| Supported 802.1X inner methods | `TLS` (certificate-based), `MSCHAPV2` (credential-based) |

## Before you begin

Gather interface-specific settings before sending this request. A wrong static IP, gateway, Wi-Fi credential, or cellular setting can disconnect the reader from your network.

| What you need | Details |
| --- | --- |
| Interface key | Include exactly one top-level interface key: `eth0`, `mlan0`, `bnep0`, `wan0` (**FXR90 only**), or `uap0`. |
| Cellular (`wan0`) | **FXR90 only** — not supported on FXR60. |
| Hotspot vs Wi-Fi client | `uap0` and `mlan0` cannot be active at the same time. Disable one before enabling the other. |
| IPv4 addressing | `IPV4.dhcp: true` for DHCP. For static IPv4, set `dhcp: false` and supply `ipAddress`, `subnetMask`, `gatewayAddress`, and `dnsAddress`. |
| IPv6 addressing | `IPV6.dhcp: true` for DHCP. For static IPv6, set `dhcp: false` and supply `ipAddress`, `gatewayAddress`, `dnsAddress`, `domainName`, and `prefix`. IPv6 has no `subnetMask` — use `prefix` (CIDR length, for example `64`). |
| Wi-Fi access point | For `mlan0`, include `accesspoint` with `essid`, `connect`, `autoConn`, and `security`. |
| Wi-Fi security | WPA2 Personal needs `password`. Enterprise (WPA2/WPA3) needs `authentication` plus a client certificate or a username and password. |
| Cellular settings | For `wan0` (**FXR90 only**), set `activeSim` (`psim` or `esim`) and supply `apn` and `preferredNetworkType` for the chosen SIM. |
| Hotspot settings | For `uap0`, provide `ssid`, `ssidPassword`, `countryCode`, `securityType` (`WPA2Personal` or `WPA3Personal` only), and `isHidden`. |
| Interface enablement | Always include `enable: true` or `enable: false` on the interface object. |
| 802.1X enablement | When configuring 802.1X, set `security.enable: true`. JSON key is `802_1XEAP` (case-sensitive). |
| Success response (200) | Empty string (`""`). The reader does not echo the new configuration. Confirm with `GET /cloud/network`. |

<details>
<summary>IPv4 and IPv6 addressing</summary>

IPv4 and IPv6 are configured independently under `IPV4` and `IPV6`. Each can be DHCP or static. Applies to `eth0` and `mlan0`.

| | IPv4 | IPv6 |
| --- | --- | --- |
| DHCP | `"dhcp": true` | `"dhcp": true` |
| Static | `"dhcp": false` plus address fields | `"dhcp": false` plus address fields |
| Network size | `subnetMask` (for example `255.255.255.0`) | `prefix` (for example `64`) |

`prefix` is the IPv6 prefix length (CIDR). It is required when `IPV6.dhcp` is `false`. A typical LAN value is `64`.

DHCP — the reader obtains addresses automatically:

```json
"IPV4": { "dhcp": true },
"IPV6": { "dhcp": true }
```

Static IPv6 — set `dhcp` to `false` and supply the address fields, including `prefix`:

```json
"IPV6": {
  "dhcp": false,
  "ipAddress": "2001:db8:1:0:8731:2eb1:cd28:f0cd",
  "gatewayAddress": "fe80::1643:8376:b32:4a16",
  "dnsAddress": "2001:4860:4860::9999",
  "domainName": "example.ee.com",
  "prefix": 64
}
```

See the Ethernet static IP example for a full request that sets both IPv4 and IPv6.

</details>

<details>
<summary>802.1X enterprise authentication</summary>

Ethernet `802_1XEAP` and Wi-Fi `WPA2Enterprise` / `WPA3Enterprise` pair an outer EAP method (`authentication`) with an inner method (`innerAuthentication`).

Supported inner methods:

- `TLS` — certificate-based
- `MSCHAPV2` — credential-based (username and password)

| Outer (`authentication`) | Inner (`innerAuthentication`) | Type | Credentials required |
| --- | --- | --- | --- |
| `TLS` | `""` | Certificate-based | Client certificate |
| `TTLS` | `TLS` | Certificate-based | Client certificate |
| `PEAP` | `TLS` | Certificate-based | Client certificate |
| `TTLS` | `MSCHAPV2` | Credential-based | Username and password |
| `PEAP` | `MSCHAPV2` | Credential-based | Username and password |

`innerAuthentication` rules:

- **TTLS** or **PEAP** — set `innerAuthentication` to the inner method (`MSCHAPV2` for username/password, or `TLS` for a client certificate).
- **TLS** (outer) — there is no inner method. Send `innerAuthentication` as an empty string (`""`). Do not omit the field and do not send a space.

> [!note]
> `TTLS`+`TLS` and `PEAP`+`TLS` are supported on the reader but are non-standard on many RADIUS servers. Cisco ISE does not support TTLS-TLS. FreeRADIUS does not support PEAP-TLS. Confirm RADIUS-server support before using these combinations. The credential-based combinations `TTLS`+`MSCHAPV2` and `PEAP`+`MSCHAPV2` are widely supported.

Credential-based Ethernet example (`TTLS` + `MSCHAPV2`). The same `802_1XEAP` object applies to `mlan0` under `accesspoint.security`:

```json
{
  "eth0": {
    "enable": true,
    "security": {
      "enable": true,
      "802_1XEAP": {
        "authentication": "TTLS",
        "innerAuthentication": "MSCHAPV2",
        "username": "testuser1",
        "password": "secret"
      }
    }
  }
}
```

</details>
