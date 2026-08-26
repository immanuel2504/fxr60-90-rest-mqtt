## 1. Description

The `GET /cloud/wifiNetworks` REST endpoint triggers a Wi-Fi scan and retrieves the list of all visible Wi-Fi networks in the reader's vicinity.

This endpoint returns:

- The ESSID (network name) of each visible access point
- The current signal strength of each network as a percentage
- The security protocols and capabilities supported by each access point (e.g., WPA2, WPA3, 802.1X)
- Any existing saved configuration profiles on the reader for these networks, including auto-connect behavior and enterprise security details

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_availableWifiNetworks` |
| Pattern Name | Wi-Fi Site Survey |
| REST Endpoint | `GET /cloud/wifiNetworks` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve visible Wi-Fi networks and saved connection profiles |

## 3. When to Use This Endpoint

Use `GET /cloud/wifiNetworks` to:

- Perform a remote site survey to evaluate Wi-Fi coverage at the reader's location
- Troubleshoot wireless connectivity by verifying the target network is broadcasting with adequate signal strength
- Identify the security protocols required by local access points before pushing a new Wi-Fi configuration
- Audit which saved profiles are configured to auto-connect

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `essid` | Is the target network visible? | If the network is not listed, the reader cannot connect to it regardless of configuration. |
| `signalStrength` | What is the signal strength percentage? | Low signal causes unstable connectivity and increased retransmissions. |
| `configuration.security.type` | What security type is required (WPA2, WPA3, 802.1X)? | The network configuration in `PUT /cloud/network` must match the access point's security requirements. |
| `configuration.autoConnect` | Is a saved profile configured for auto-connect? | Confirms whether the reader will reconnect to this network automatically after a restart. |
