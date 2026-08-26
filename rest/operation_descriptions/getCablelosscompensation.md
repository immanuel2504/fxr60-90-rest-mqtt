## 1. Description

The `GET /cloud/cableLossCompensation` REST endpoint retrieves the cable loss compensation values configured on the reader for each configured read point.

This endpoint returns:

- Cable length per read point
- Cable loss per hundred feet per read point

No request body is required. Values are returned using read-point keys `1` through `8` (only configured read points are included).

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `get_cableLossCompensation` |
| Pattern Name | Cable Loss Compensation Query |
| REST Endpoint | `GET /cloud/cableLossCompensation` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Supported Operations | Retrieve per-read-point cable loss compensation values |

## 3. When to Use This Endpoint

Use `GET /cloud/cableLossCompensation` to:

- Review compensation values before adjusting transmit power settings
- Verify cabling assumptions per antenna or read point
- Audit RF link budgets across all read points
- Confirm settings after replacing antenna cabling or after a prior `PUT /cloud/cableLossCompensation` call

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `1.cableLength` | What cable length is configured for read point 1? | Cable length feeds into the loss calculation that adjusts effective transmit power. |
| `1.cableLossPerHundredFt` | What loss per 100 ft is configured for read point 1? | Higher cable loss requires the reader to transmit at a higher power to compensate. |
| Per-port consistency | Are all active read points configured? | Unconfigured ports default to zero compensation, which may underpower long cable runs. |
