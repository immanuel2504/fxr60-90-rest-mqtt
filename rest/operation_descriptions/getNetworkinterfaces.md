## 1. Description

The `GET /cloud/networkInterfaces` REST endpoint retrieves the list of network interfaces available on the reader.

This endpoint returns:

- The list of available network interface names, returned in `availableNetworkInterfaces` (e.g., `eth0`, `mlan0`, `wan0`, `bnep0`, `uap0`)

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Network Interface Query |
| REST Endpoint | `GET /cloud/networkInterfaces` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
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
| `availableNetworkInterfaces` | Are all expected interfaces present (`eth0`, `mlan0`, `wan0`)? | Only interfaces returned here can be configured in `PUT /cloud/network`. |
| `wan0` presence | Is the cellular interface listed? | Confirms whether the reader hardware supports cellular connectivity. |
