## 1. Description

The `PUT /cloud/region` REST endpoint updates the reader's RF region and the regulatory standard applied during inventory.

This endpoint allows you to configure:

- The deployment country through `country`
- The regulatory standard to apply through `standardname`
- Optionally, the Listen Before Talk (LBT) state through `isLBT`, when the selected standard supports it
- Optionally, a specific channel frequency list (kHz) through `channeldata`, when the selected standard supports channel selection

Use this endpoint to:

- Set the correct RF region before first use in a deployment country
- Switch the reader to a different region when relocating hardware
- Apply a specific regulatory standard within a multi-standard country

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

Verify the target country and standard are supported before sending this request. Applying an incorrect region may make the reader non-compliant with local RF regulations.

| What You Need | Details |
|---|---|
| Country name | Use `GET /cloud/supportedRegionList` to retrieve the exact country name string accepted by the reader. |
| Standard name | Use `GET /cloud/supportedStandardList` to retrieve valid standard names for the target country. |
| LBT override (optional) | Provide `isLBT` (boolean) to set Listen Before Talk when the selected standard supports it. |
| Channel selection (optional) | Provide `channeldata` (list of center frequencies in kHz) when the selected standard supports channel selection. |
| Active inventory | Stop inventory with `PUT /cloud/stop` before changing region. Region changes take effect immediately and affect all RF parameters. |
| LBT and channel behavior | Some standards mandate LBT always-on or restrict channel usage. Review the standard entry from `GET /cloud/supportedStandardList` before applying. |
