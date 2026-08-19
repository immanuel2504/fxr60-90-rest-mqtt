## 1. Description

The `GET /cloud/version` REST endpoint retrieves detailed hardware and software component version information from the reader's software stack.

This endpoint returns:

- Reader application, radio firmware, and cloud agent versions
- Radio control application version
- Reader model and serial number
- Available OS upgrade paths (`availableOsUpgrades`; empty when none). The backup OS version is not returned.

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Version Query |
| REST Endpoint | `GET /cloud/version` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve firmware, model, serial number, and upgrade details |

## 3. When to Use This Endpoint

Use `GET /cloud/version` to:

- Confirm the installed firmware versions before or after a system update
- Verify the exact reader model when applying model-specific configuration
- Capture the serial number for asset tracking, remote fleet management, or support cases
- Audit whether a downloaded OS upgrade is waiting (`availableOsUpgrades`)

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `readerApplication` | Current reader software version | Determines which features and API operations are available. |
| `radioFirmware` | Firmware running on the radio module | Affects RF behavior, read performance, and hardware compatibility. |
| `cloudAgentApplication` | Cloud agent version | Governs device-to-cloud messaging behavior and cloud connectivity. |
| `model` | Reader model identifier | Drives physical capabilities, antenna limits, and model-specific settings. |
| `serialNumber` | Unique reader serial number | Identifies the device for support cases and asset records. |
| `availableOsUpgrades` | Is the object empty or populated? | A populated object means a downloaded OS upgrade is ready to install. An empty object `{}` means none is waiting. |
| `revertBackFirmware` | Typically `{}` | FXR60 / FXR90 do not report the backup OS version through this field. |
