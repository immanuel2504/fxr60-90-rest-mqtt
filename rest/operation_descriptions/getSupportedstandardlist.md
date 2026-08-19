## 1. Description

The `GET /cloud/supportedStandardList` REST endpoint retrieves the list of RF regulatory standards supported by the reader and the channel details for each.

This endpoint returns:

- Supported regulatory standard names
- LBT and frequency hopping configurability per standard
- Whether individual channels are selectable per standard
- Enabled channel data per standard

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Supported Standard Query |
| REST Endpoint | `GET /cloud/supportedStandardList` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve supported regulatory standards and their channel details |

## 3. When to Use This Endpoint

Use `GET /cloud/supportedStandardList` to:

- Discover which regulatory standards are available for a given region
- Determine whether LBT or channel hopping is configurable per standard
- Inspect channel availability before tuning RF settings
- Populate standard selection options in provisioning tools

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `StandardName` | Is the target regulatory standard listed? | Confirms that the required standard is available before configuring the region. |
| `isLBTConfigurable` | Can LBT be enabled or disabled for this standard? (string-encoded `"true"`/`"false"`) | Some standards mandate LBT always-on; knowing configurability prevents invalid region settings. |
| `isChannelSelectable` | Can individual channels be selected for this standard? | Determines whether `channeldata` can be supplied when setting the region. |
| `channeldata` | Which channels are available for each standard? | Determines the frequency plan the reader will use for that standard. |
