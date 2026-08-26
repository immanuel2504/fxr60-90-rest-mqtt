## 1. Description

**Product note:** `eSimConfig` is supported on **FXR90 only**. It is not available on FXR60 (no eSIM / cellular modem).

The `PUT /cloud/eSimConfig` REST endpoint updates the eSIM profile state on the reader.

This endpoint allows you to configure:

- The eSIM operation to perform through `operation`
- The target profile nickname through `profileNickName`
- The activation code for provisioning a new profile through `activationID`

Use this endpoint to:

- Add (install) a new eSIM profile using its activation code
- Enable a specific eSIM carrier profile on the reader
- Disable a specific eSIM carrier profile on the reader
- Switch between installed eSIM profiles for different cellular network providers
- Delete an eSIM profile from the reader
- Apply eSIM provisioning changes from your carrier management system

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_eSimConfig` |
| Pattern Name | eSIM Configuration |
| REST Endpoint | `PUT /cloud/eSimConfig` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | **FXR90 only** (eSIM / cellular; not on FXR60) |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Supported Operations | `add`, `delete`, `enable`, `disable` |

## 3. Before You Begin

Use `GET /cloud/eSimConfig` first to retrieve the exact profile nickname available on the reader before sending this request.

| What You Need | Details |
|---|---|
| Operation | The eSIM operation to perform: `add` to provision a new profile, `delete` to remove one, `enable` to activate the selected profile, or `disable` to deactivate it. |
| Profile nickname | The exact nickname of the eSIM profile to apply the operation to, as returned by `GET /cloud/eSimConfig`. The nickname must match exactly - case-sensitive. |
| Activation code | Required only when `operation` is `add`: the activation code/ID (`activationID`) used to provision the new eSIM profile. Omit for `enable`, `disable`, and `delete`. |
| Active SIM setting | After enabling an eSIM profile, confirm the `wan0.activeSim` is set to `esim` in the network configuration (see `PUT /cloud/network`) for the profile to be used for data. |
