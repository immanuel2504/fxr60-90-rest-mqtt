## 1. Description

The `PUT /cloud/region` REST endpoint sets the RF region and regulatory standard.

This endpoint requires:

- `country` — exact name from `GET /cloud/supportedRegionList`
- `standardname` — exact name from `GET /cloud/supportedStandardList`

Optional:

- `isLBT` — `true` or `false`, when `isLBTConfigurable` is `"true"`
- `channeldata` — frequencies in kHz, when `isChannelSelectable` is `"true"`

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_region` |
| Pattern Name | Region Configuration |
| REST Endpoint | `PUT /cloud/region` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `country`, `standardname` |

## 3. Before You Begin

Take `country` and `standardname` from this reader's lists. Use the JSON field names below.

| Field | What to set |
|---|---|
| `country` | Exact string from `GET /cloud/supportedRegionList`. |
| `standardname` | Exact string from `GET /cloud/supportedStandardList`. |
| `isLBT` | Optional. `true` or `false` when `isLBTConfigurable` is `"true"`. |
| `channeldata` | Optional. Frequencies in kHz when `isChannelSelectable` is `"true"`. |
