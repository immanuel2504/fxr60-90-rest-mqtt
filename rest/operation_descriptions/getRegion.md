## 1. Description

The `GET /cloud/region` REST endpoint retrieves the reader's currently configured RF region and the regulatory parameters in effect.

This endpoint returns:

- The active region code and country name
- The regulatory standard currently applied
- Listen Before Talk (LBT) enable state
- Frequency hopping state
- Enabled channel list for the active region
- Minimum and maximum transmit power supported

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_region` |
| Pattern Name | Region Configuration Query |
| REST Endpoint | `GET /cloud/region` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve active RF region and regulatory settings |

## 3. When to Use This Endpoint

Use `GET /cloud/region` to:

- Confirm the reader is set to the correct regulatory region before deployment
- Verify LBT and channel configuration before starting inventory
- Audit minimum and maximum transmit power for the region
- Validate region settings after deploying to a new country

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `country` | Is the correct country configured? | The reader must match the regulatory region of its deployment location. |
| `regulatoryStandard` | Which standard is applied (e.g., `CANADA_FCC_15`)? | Determines which transmission rules apply - channels, power limits, and LBT behavior. |
| `lbtEnabled` | Is Listen Before Talk active? | Required in some regions (e.g., ETSI). Affects when the radio may transmit. |
| `FrequencyHopping` | Is frequency hopping enabled? | Mandatory in most regions. Confirms the radio is operating compliantly. |
| `maxTxPowerSupported` | What is the allowed power ceiling? | Use this to validate transmit power settings before starting inventory. |
| `channelData` | How many channels are available? | The channel list defines where the reader can operate within the region. |
