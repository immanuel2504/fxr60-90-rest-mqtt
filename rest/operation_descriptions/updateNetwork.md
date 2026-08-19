## 1. Description

**Product note:** Cellular interface `wan0` is supported on **FXR90 only**. It is **not present on FXR60**. Do not send a `wan0` body to an FXR60 reader.

The `PUT /cloud/network` REST endpoint updates reader network configuration for a single interface per request.

This endpoint allows you to configure:

- Ethernet (`eth0`) - DHCP, static IPv4/IPv6 addressing, and 802.1X security
- Wi-Fi station (`mlan0`) - DHCP, static addressing, access point connection, and WPA2/WPA3/Enterprise security
- Bluetooth PAN (`bnep0`) - discoverability, pairing, and DHCP address pool
- Cellular WAN (`wan0`) - SIM selection, APN, network type preference, and IPv6 — **FXR90 only**
- Wi-Fi hotspot (`uap0`) - SSID, password, country code, and security type

Use this endpoint to:

- Connect the reader to a new Wi-Fi access point
- Switch from DHCP to static IP addressing on Ethernet
- Enable or disable a network interface
- Configure cellular APN and SIM settings (**FXR90 / `wan0` only**)
- Provision a Wi-Fi hotspot on the reader

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Network Configuration |
| REST Endpoint | `PUT /cloud/network` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 (`wan0` = FXR90 only) |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Supported Interface Keys | `eth0`, `mlan0`, `bnep0`, `wan0` (**FXR90 only**), `uap0` |
| Supported Wi-Fi Security Types | `WPA2Personal`, `WPA2Enterprise`, `WPA3Personal`, `WPA3Enterprise` |
| Supported 802.1X Outer Methods | `TLS`, `TTLS`, `PEAP` |
| Supported 802.1X Inner Methods | `TLS` (certificate-based), `MSCHAPV2` (credential-based) |

## 3. Before You Begin

Gather all interface-specific settings before sending this request. A wrong static IP, gateway, Wi-Fi credential, or cellular setting can disconnect the reader from your network.

| What You Need | Details |
|---|---|
| Interface key | Include exactly one top-level interface key: `eth0`, `mlan0`, `bnep0`, `wan0` (**FXR90 only**), or `uap0`. Only one interface can be configured per request. |
| Cellular (`wan0`) | **FXR90 only** — not supported on FXR60. |
| Hotspot vs Wi-Fi client | `uap0` (hotspot) and `mlan0` (Wi-Fi client) share the same Wi-Fi radio and **cannot be active at the same time**. To enable hotspot, disable `mlan0` first. To enable Wi-Fi client, disable `uap0` first. |
| IPv4 addressing | Use `IPV4.dhcp: true` for dynamic addressing. For static IPv4, set `IPV4.dhcp: false` and supply `ipAddress`, `subnetMask`, `gatewayAddress`, and `dnsAddress`. |
| IPv6 addressing | Use `IPV6.dhcp: true` for dynamic addressing. For static IPv6, set `IPV6.dhcp: false` and supply `ipAddress`, `gatewayAddress`, `dnsAddress`, `domainName`, and `prefix`. `prefix` is the IPv6 prefix length (CIDR), for example `64`. IPv6 has no `subnetMask` field — use `prefix` instead. |
| Wi-Fi access point | For `mlan0`, include the `accesspoint` object with `essid`, `connect`, `autoConn`, and the `security` sub-object. |
| Wi-Fi security | For WPA2 Personal, provide the `password`. For Enterprise (WPA2/WPA3), provide the `authentication` type and either a client certificate (certificate-based) or a username and password (credential-based). See the 802.1X authentication combinations below. |
| Cellular settings | For `wan0` (**FXR90 only**), set `activeSim` (`psim` or `esim`) and supply the `apn` and `preferredNetworkType` for the chosen SIM. |
| Hotspot settings | For `uap0`, provide `ssid`, `ssidPassword`, `countryCode`, `securityType` (`WPA2Personal` or `WPA3Personal` only), and `isHidden`. |
| Interface enablement | Always include `enable: true` or `enable: false` on the interface object to control whether the interface is active after configuration. |
| Success response (200) | Empty string (`""`). The reader does not return the updated configuration. Confirm the change with `GET /cloud/network`. |

### IPv4 and IPv6 addressing

IPv4 and IPv6 are configured independently under `IPV4` and `IPV6`. Each can be DHCP or static.

| | IPv4 | IPv6 |
|---|---|---|
| DHCP | `"dhcp": true` | `"dhcp": true` |
| Static | `"dhcp": false` plus address fields | `"dhcp": false` plus address fields |
| Network size | `subnetMask` (for example `255.255.255.0`) | `prefix` (for example `64`) |

`prefix` is the IPv6 prefix length (CIDR). It is the IPv6 equivalent of `subnetMask`. IPv6 has no `subnetMask` field. `prefix` is required when `IPV6.dhcp` is `false`. A typical LAN value is `64`.

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

Applies to `eth0` and `mlan0`. See the Ethernet static IP example for a full request that sets both IPv4 and IPv6.

### 802.1X Enterprise Authentication Combinations

Ethernet `802_1XEAP` and Wi-Fi `WPA2Enterprise` / `WPA3Enterprise` pair an outer EAP method (`authentication`) with an inner method (`innerAuthentication`).

Supported inner methods:

- `TLS` — certificate-based
- `MSCHAPV2` — credential-based (username and password)

The reader supports the following combinations:

| Outer (`authentication`) | Inner (`innerAuthentication`) | Type | Credentials required |
|---|---|---|---|
| `TLS` | `""` | Certificate-based | Client certificate |
| `TTLS` | `TLS` | Certificate-based | Client certificate |
| `PEAP` | `TLS` | Certificate-based | Client certificate |
| `TTLS` | `MSCHAPV2` | Credential-based | Username and password |
| `PEAP` | `MSCHAPV2` | Credential-based | Username and password |

`innerAuthentication` rules:

- **TTLS** or **PEAP** — set `innerAuthentication` to the inner method (`MSCHAPV2` for username/password, or `TLS` for a client certificate).
- **TLS** (outer) — there is no inner method. Send `innerAuthentication` as an empty string (`""`). Do not omit the field and do not send a space.

> Note: `TTLS`+`TLS` and `PEAP`+`TLS` are supported on the reader but are non-standard on many RADIUS servers. Cisco ISE does not support TTLS-TLS. FreeRADIUS does not support PEAP-TLS. Confirm RADIUS-server support before using these combinations. The credential-based combinations `TTLS`+`MSCHAPV2` and `PEAP`+`MSCHAPV2` are widely supported.

> Important: `uap0` and `mlan0` are mutually exclusive. The reader has one Wi-Fi radio, which operates either as a client joining an access point (`mlan0`) or as an access point of its own (`uap0`) — never both. If hotspot needs to be enabled, disable `mlan0` first, then enable `uap0`. If Wi-Fi client needs to be enabled, disable `uap0` first, then enable `mlan0`. Sending `uap0` with `enable: true` while `mlan0` is connected is rejected (for example `Disable WiFi to enable Hotspot`). The same applies in the other direction. Configure them in separate requests.
