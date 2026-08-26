Retrieves the reader's network configuration. Omit the body (or send `{}`) for all interfaces. Send `{"interface": "eth0"}` (or `mlan0`, `bnep0`, `wan0`, `uap0`, `blescan`) for one interface.

> [!warning]
> Cellular interface `wan0` is supported on **FXR90 only**. It is not present on FXR60. On FXR60, expect interfaces such as `eth0`, `mlan0`, `bnep0`, and `uap0` only.

The response includes:

- Device hostname
- Ethernet (`eth0`) configuration and connection status
- Wi-Fi station (`mlan0`) configuration and access point details
- Bluetooth PAN (`bnep0`) configuration and status
- Cellular (`wan0`) configuration and status — **FXR90 only**
- Wi-Fi hotspot (`uap0`) configuration, connected clients, and status

> [!tip]
> Call this endpoint after `PUT /cloud/network`. The PUT success body is an empty string (`""`); this GET is how you confirm the change. To confirm one interface only, send `{"interface": "<name>"}`.

## Endpoint details

| Property | Value |
| --- | --- |
| MQTT Command | `get_network` |
| Pattern name | Network Configuration Query |
| REST endpoint | `GET /cloud/network` |
| Communication type | Client to device (HTTP request/response) |
| Applies to | FXR60 / FXR90 (`wan0` = FXR90 only) |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported operations | Retrieve all interfaces, or one interface via `interface` |

## When to use this endpoint

- Confirm the reader's IP addressing before changing it
- Verify which interfaces are connected or enabled
- Audit network identity and interface status across a fleet
- Troubleshoot Wi-Fi, Bluetooth, cellular, or hotspot connectivity

<details>
<summary>Key fields to check</summary>

| Field | What to check | Why it matters |
| --- | --- | --- |
| `eth0` | Is Ethernet connected and does it have an IP? | Primary wired path for cloud communication. |
| `mlan0` | Is Wi-Fi associated, and which SSID? | Confirms the correct access point for wireless deployments. |
| `wan0` | Is cellular connected and does it have a carrier? (**FXR90 only**; absent on FXR60) | Required for cellular backhaul. |
| `uap0` | Is the hotspot enabled, and are clients connected? | Confirms hotspot provisioning mode. |
| `hostName` | Does the hostname match expected naming? | Device identity on the LAN and in management systems. |

</details>
