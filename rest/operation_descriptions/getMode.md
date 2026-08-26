## 1. Description

The `GET /cloud/mode` REST endpoint retrieves the reader's current operating mode and the RF settings associated with that mode.

This endpoint returns:

- The operating mode type (`SIMPLE`, `INVENTORY`, `PORTAL`, `CONVEYOR`, or `CUSTOM`)
- Active antennas and their transmit power settings
- The environment profile in use
- Mode-specific configuration settings (portal, conveyor, etc.)
- Gen2 query, select, and access settings
- Report filtering, RSSI filtering, metadata fields, and radio start/stop conditions

An optional `verbose` flag controls how much of the configuration is returned.

## 2. The `verbose` Flag

The request body optionally accepts a single boolean field, `verbose`, that controls the level of detail in the response:

| `verbose` | Response |
|---|---|
| `false` (or body omitted) | Returns **only the settings explicitly configured** for the current mode. Defaults are omitted. |
| `true` | Returns the **full effective configuration** — your settings plus every default the reader is applying for the current mode. |

An empty body (`{}`) behaves the same as `verbose: false`.

## 3. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_mode` |
| Pattern Name | Operating Mode Query |
| REST Endpoint | `GET /cloud/mode` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve active operating mode and RF settings |

## 4. When to Use This Endpoint

Use `GET /cloud/mode` to:

- Confirm the active mode before starting an inventory session
- Verify antenna and transmit power selection before RF operations
- Check the environment profile currently in use
- Review mode-specific settings before changing them with `PUT /cloud/mode`
- Check tag reporting and RSSI filter settings before a site validation

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `type` | Which mode is active (`SIMPLE`, `INVENTORY`, `PORTAL`, ...)? | Determines which RF behavior and tag reporting logic the reader uses. |
| `antennas` | Are the right ports enabled with the expected transmit power? | Misconfigured antennas result in missed reads or coverage gaps. |
| `transmitPower` | Is the power level within regulatory limits? | Transmit power must stay below the regional maximum reported by `GET /cloud/region`. |
| `environment` | Is the profile matched to the deployment environment? | Affects reader sensitivity and false-read filtering for the deployment environment. |
