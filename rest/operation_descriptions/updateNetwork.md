## 1. Description

The `PUT /cloud/network` REST endpoint updates one network interface per request.

Send exactly one of:

- `eth0`
- `mlan0`
- `bnep0`
- `wan0` — FXR90 only
- `uap0`

Also send `enable` on that interface. `uap0` and `mlan0` cannot both be enabled.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_network` |
| Pattern Name | Network Configuration |
| REST Endpoint | `PUT /cloud/network` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | one of `eth0`, `mlan0`, `bnep0`, `wan0`, `uap0` |

## 3. Before You Begin

Decide the interface and fields. Use the JSON field names below.

| Field | What to set |
|---|---|
| `eth0`, `mlan0`, `bnep0`, `wan0`, `uap0` | Send exactly one of these keys. |
| `enable` | `true` or `false` on that interface. |
| `IPV4.dhcp` | `true` for DHCP. `false` plus `ipAddress`, `subnetMask`, `gatewayAddress`, `dnsAddress` for static IPv4. |
| `IPV6.dhcp` | `true` for DHCP. `false` plus `ipAddress`, `gatewayAddress`, `dnsAddress`, `domainName`, `prefix` for static IPv6. |
| `accesspoint.essid` | `mlan0` SSID. Also send `connect` and `autoConn`. |
| `accesspoint.security` | One of `WPA2Personal`, `WPA3Personal`, `WPA2Enterprise`, `WPA3Enterprise`. |
| `security.802_1XEAP` | `eth0` 802.1X. |
| `authentication` | `TLS`, `TTLS`, or `PEAP`. |
| `innerAuthentication` | `TLS` or `MSCHAPV2` when `authentication` is `TTLS` or `PEAP`. When `authentication` is `TLS`, empty string or any string (for example `"tt"`) will work. |
| `bnep0` | `dhcpStartAddress`, `dhcpEndAddress`, `discoverable`, `pairable`, `passKey`, `usePassKey`. |
| `wan0.activeSim` | `psim` or `esim`. FXR90 only. |
| `psim` / `esim` | `apn`, `preferredNetworkType`, `enableIPv6` for the chosen SIM. |
| `uap0` | `ssid`, `ssidPassword`, `securityType`, `isHidden`, `countryCode`. `securityType` is `WPA2Personal` or `WPA3Personal`. |

`authentication` and `innerAuthentication` pairs:

| `authentication` | `innerAuthentication` |
|---|---|
| `TLS` | empty string or any string |
| `TTLS` | `TLS` or `MSCHAPV2` |
| `PEAP` | `TLS` or `MSCHAPV2` |
