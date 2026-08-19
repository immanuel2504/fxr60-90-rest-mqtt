## 1. Description

The `GET /cloud/readerCapabilities` REST endpoint retrieves the static hardware and software capabilities of the reader.

This endpoint returns (all fields nested under a top-level `capabilities` object):

- GPIO capacity (number of GPIs and GPOs available)
- Whether LLRP is supported
- Supported endpoint types for data and management
- API versions accepted by the reader

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Reader Capability Query |
| REST Endpoint | `GET /cloud/readerCapabilities` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve static reader hardware and software capabilities |

## 3. When to Use This Endpoint

Use `GET /cloud/readerCapabilities` to:

- Discover how many GPI and GPO pins are available before wiring logic
- Confirm whether LLRP is supported on this reader model
- Determine which endpoint types can be configured for data and management
- Verify which API versions the reader accepts before sending requests
- Audit hardware capabilities across a mixed fleet

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `capabilities.numGPIs` | How many GPI pins are available? | Limits how many external input triggers (sensors, beam breaks) can be wired. |
| `capabilities.numGPOs` | How many GPO pins are available? | Limits how many external output devices (lights, gates) can be driven. |
| `capabilities.llrpSupported` | Is LLRP supported? | Determines whether the reader can be managed via LLRP-based tools. |
| `capabilities.endpointTypesSupported` | Which endpoint types are supported? | Governs which data delivery options can be configured in `PUT /cloud/config`. |
| `capabilities.apiSupported.versions` | Which API versions are accepted? | Ensures the management application targets a compatible API version. |
