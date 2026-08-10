## 1. Description

The `PUT /cloud/cableLossCompensation` REST endpoint configures cable loss compensation values for each antenna read point on the reader.

This endpoint allows you to configure:

- Cable length and loss-per-hundred-feet for read points `1` through `8`

Use this endpoint to:

- Compensate for signal attenuation caused by long antenna cable runs
- Tune compensation independently per port for multi-antenna deployments with different cable lengths
- Improve read range accuracy by accounting for passive cable loss in the RF path

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Cable Loss Compensation Configuration |
| REST Endpoint | `PUT /cloud/cableLossCompensation` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Supported Read Point Keys | `"1"` through `"8"` |

## 3. Before You Begin

Measure the physical cable runs for each antenna port before sending this request. Incorrect values will produce inaccurate compensation and may reduce read range.

| What You Need | Details |
|---|---|
| Read point keys | Use numeric string keys `"1"` through `"8"` in the request body. Only include keys for ports that have physical cables attached. |
| Cable length | The length of the antenna cable in the unit expected by the reader (feet). Measure the actual cable run from the reader port to the antenna. |
| Cable loss per hundred feet | The attenuation rating of the cable type in dB per 100 feet. This value is specified by the cable manufacturer. |
| Available read points | Use `GET /cloud/readPoints` to confirm which read point IDs are available on this reader before sending. |
