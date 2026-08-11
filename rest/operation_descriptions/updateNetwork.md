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
| Supported 802.1X Inner Methods | `TLS` (certificate-based), `MSCHAPv2` (credential-based) |

## 3. Before You Begin

Gather all interface-specific settings before sending this request. A wrong static IP, gateway, Wi-Fi credential, or cellular setting can disconnect the reader from your network.

| What You Need | Details |
|---|---|
| Interface key | Include exactly one top-level interface key: `eth0`, `mlan0`, `bnep0`, `wan0` (**FXR90 only**), or `uap0`. Only one interface can be configured per request. |
| Cellular (`wan0`) | **FXR90 only** — not supported on FXR60. |
| Hotspot vs Wi-Fi client | `uap0` (hotspot) and `mlan0` (Wi-Fi client) share the same Wi-Fi radio and **cannot be active at the same time**. Enabling one disables the other. |
| IP addressing | Use `IPV4.dhcp: true` for dynamic addressing, or supply `ipAddress`, `subnetMask`, `gatewayAddress`, and `dnsAddress` for static. |
| Wi-Fi access point | For `mlan0`, include the `accesspoint` object with `essid`, `connect`, `autoConn`, and the `security` sub-object. |
| Wi-Fi security | For WPA2 Personal, provide the `password`. For Enterprise (WPA2/WPA3), provide the `authentication` type and either a client certificate (certificate-based) or a username and password (credential-based). See the 802.1X authentication combinations below. |
| Cellular settings | For `wan0` (**FXR90 only**), set `activeSim` (`psim` or `esim`) and supply the `apn` and `preferredNetworkType` for the chosen SIM. |
| Hotspot settings | For `uap0`, provide `ssid`, `ssidPassword`, `countryCode`, `securityType` (`WPA2Personal` or `WPA3Personal` only), and `isHidden`. |
| Interface enablement | Always include `enable: true` or `enable: false` on the interface object to control whether the interface is active after configuration. |

### 802.1X Enterprise Authentication Combinations

`WPA2Enterprise` and `WPA3Enterprise` pair an outer EAP method with an inner method. The reader supports the following combinations:

| Authentication type | Combination | Credentials required |
|---|---|---|
| Certificate-based | `TLS` | Client certificate |
| Certificate-based | `TTLS-TLS` | Client certificate |
| Certificate-based | `PEAP-TLS` | Client certificate |
| Credential-based | `TTLS-MSCHAPv2` | Username and password |
| Credential-based | `PEAP-MSCHAPv2` | Username and password |

> Important: `uap0` and `mlan0` are mutually exclusive. The reader has one Wi-Fi radio, which operates either as a client joining an access point (`mlan0`) or as an access point of its own (`uap0`) — never both. Sending `uap0` with `enable: true` while `mlan0` is connected drops the Wi-Fi client connection, and vice versa. Configure them in separate requests and enable only the one you intend to run. If the reader's only route to your network is `mlan0`, enabling the hotspot will disconnect it.
