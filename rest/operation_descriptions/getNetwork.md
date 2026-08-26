## 1. Description

**Product note:** Cellular interface `wan0` is supported on **FXR90 only**. It is **not present on FXR60**. On FXR60, expect interfaces such as `eth0`, `mlan0`, `bnep0`, and `uap0` only.

The `GET /cloud/network` REST endpoint retrieves the reader's network configuration.

Omit the request body (or send `{}`) to return **all** interfaces. To return one interface, send:

```json
{ "interface": "eth0" }
```

Supported `interface` values: `eth0`, `mlan0`, `bnep0`, `wan0`, `uap0`, `blescan`. `wan0` is **FXR90 only**.

This endpoint returns:

- The device hostname
- Ethernet (`eth0`) interface configuration and connection status
- Wi-Fi station (`mlan0`) interface configuration and access point details
- Bluetooth PAN (`bnep0`) configuration and status
- Cellular (`wan0`) configuration and status — **FXR90 only**
- Wi-Fi hotspot (`uap0`) configuration, connected clients, and status
- BLE scan (`blescan`) when requested

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_network` |
| Pattern Name | Network Configuration Query |
| REST Endpoint | `GET /cloud/network` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 (`wan0` = FXR90 only) |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve network configuration for all interfaces, or one interface via `interface` |

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
| `wan0` | Is cellular connected and does it have a carrier? (**FXR90 only**; absent on FXR60) | Required for deployments relying on cellular backhaul. |
| `uap0` | Is the hotspot enabled and are clients connected? | Used to confirm hotspot provisioning mode is active. |
| `hostName` | Does the hostname match expected naming? | Used for device identification on the local network and in management systems. |
