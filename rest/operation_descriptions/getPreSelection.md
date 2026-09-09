## 1. Description

The `GET /cloud/preSelection` REST endpoint retrieves the current rxSawFilter pre-selection state from the reader.

The response is a string, not a boolean:

```json
{ "preSelection": "disabled" }
```

| Field | Type | Values |
|---|---|---|
| `preSelection` | string | `enabled` or `disabled` |

To change the filter, use `PUT /cloud/preSelection` with a **boolean** (`true` / `false`). `GET /cloud/preSelection` always returns the string form.

No additional fields are required.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_preSelection` |
| Pattern Name | rxSawFilter Status Query |
| REST Endpoint | `GET /cloud/preSelection` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Response field | `preSelection`: `enabled` \| `disabled` |

## 3. When to Use This Endpoint

Use `GET /cloud/preSelection` to:

- Check whether rxSawFilter is enabled or disabled before starting inventory
- Verify the RF pre-selection state in deployments where receiver filtering matters
- Confirm the effect of a prior `PUT /cloud/preSelection` call

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `preSelection` | Is the value `enabled` or `disabled`? | Enabling the SAW filter improves receiver selectivity in noisy RF environments but may reduce sensitivity in clean environments. |
