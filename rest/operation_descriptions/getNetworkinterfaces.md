## 1. Description

**Product note:** Cellular interface `wan0` appears in this list on **FXR90 only**. It is **not present on FXR60**.

The `GET /cloud/networkInterfaces` REST endpoint retrieves the list of network interfaces available on the reader.

This endpoint returns:

- The list of available network interface names, returned in `availableNetworkInterfaces` (e.g., `eth0`, `mlan0`, `bnep0`, `uap0`, and on **FXR90** also `wan0`)

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_networkInterfaces` |
| Pattern Name | Network Interface Query |
| REST Endpoint | `GET /cloud/networkInterfaces` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 (`wan0` = FXR90 only) |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve available network interface names |

## 3. When to Use This Endpoint

Use `GET /cloud/networkInterfaces` to:

- Identify which network interfaces are present before configuring them via `PUT /cloud/network`
- Confirm Ethernet, Wi-Fi, Bluetooth, or cellular interface availability on this reader model
- Use returned interface names as valid keys in subsequent network configuration calls

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `availableNetworkInterfaces` | Are expected interfaces present (`eth0`, `mlan0`, …)? | Only interfaces returned here can be configured in `PUT /cloud/network`. |
| `wan0` presence | Is the cellular interface listed? (**FXR90 only**; absent on FXR60) | Confirms whether this reader supports cellular / WAN. |
