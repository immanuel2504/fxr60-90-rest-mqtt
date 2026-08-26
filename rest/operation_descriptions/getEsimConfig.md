## 1. Description

**Product note:** `eSimConfig` is supported on **FXR90 only**. It is not available on FXR60 (no eSIM / cellular modem).

The `GET /cloud/eSimConfig` REST endpoint retrieves eSIM identity and profile information from the reader.

This endpoint returns:

- The reader EID (eSIM identifier) and IMEI
- Installed eSIM profiles, including nickname (`profileNickName`), provider, ICCID (`iccid`), and activation state (`enabled`)

No request body is required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_eSimConfig` |
| Pattern Name | eSIM Configuration Query |
| REST Endpoint | `GET /cloud/eSimConfig` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | **FXR90 only** (eSIM / cellular; not on FXR60) |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve eSIM identity and installed profile details |

## 3. When to Use This Endpoint

Use `GET /cloud/eSimConfig` to:

- Audit cellular or eSIM provisioning status on the reader
- Check the EID and IMEI values for SIM registration or support cases
- Review installed eSIM profiles before enabling or switching a profile with `PUT /cloud/eSimConfig`

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `eid` | Is the EID correct for this SIM profile? | The EID uniquely identifies the eSIM hardware and is required for carrier provisioning. |
| `imei` | Is the IMEI registered with the carrier? | An unregistered IMEI cannot establish a cellular data connection. |
| `profiles` | Which profiles are installed and which is active? | Only one profile can be active at a time; use this to confirm the correct carrier profile is enabled. |
