## 1. Description

The `GET /cloud/network` REST endpoint retrieves the reader's complete network configuration across all interfaces.

This endpoint returns:

- The device hostname
- Ethernet (`eth0`) interface configuration and connection status
- Wi-Fi station (`mlan0`) interface configuration and access point details
- Bluetooth PAN (`bnep0`) configuration and status
- Cellular (`wan0`) configuration and status
- Wi-Fi hotspot (`uap0`) configuration, connected clients, and status

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Network Configuration Query |
| REST Endpoint | `GET /cloud/network` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve active network configuration for all interfaces |

## 3. When to Use This Endpoint

Use `GET /cloud/network` to:

- Confirm the reader's IP addressing before changing it
- Verify which interfaces are connected or enabled
- Audit network identity and interface status across a fleet
- Troubleshoot Wi-Fi, Bluetooth, cellular, or hotspot connectivity

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `eth0` | Is the Ethernet interface connected and does it have an IP? | Primary connectivity path; must be up for cloud communication over wired LAN. |
| `mlan0` | Is Wi-Fi associated and which SSID? | Confirms the correct access point is in use for wireless deployments. |
| `wan0` | Is cellular connected and does it have a carrier? | Required for deployments relying on cellular backhaul. |
| `uap0` | Is the hotspot enabled and are clients connected? | Used to confirm hotspot provisioning mode is active. |
| `hostName` | Does the hostname match expected naming? | Used for device identification on the local network and in management systems. |
