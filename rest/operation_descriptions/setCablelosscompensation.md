## 1. Description

The `PUT /cloud/cableLossCompensation` REST endpoint sets cable length and cable loss per hundred feet for antenna read points.

Send one of these body shapes:

- **All read points** — top-level `cableLength` and `cableLossPerHundredFt` (applied to every available read point)
- **Per read point** — keys `"1"` through `"8"`, each with `cableLength` and `cableLossPerHundredFt`

Use this endpoint to:

- Compensate for signal attenuation on long antenna cable runs
- Set different length and loss values per port
- Apply the same length and loss to all ports in one request

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_cableLossCompensation` |
| Pattern Name | Cable Loss Compensation Configuration |
| REST Endpoint | `PUT /cloud/cableLossCompensation` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Supported Read Point Keys | `"1"` through `"8"` |

## 3. Before You Begin

| What You Need | Details |
|---|---|
| Body shape | All-ports object, or per-port keys `"1"`–`"8"`. Include only ports that have cables attached. |
| Cable length | Antenna cable length in feet. |
| Cable loss per hundred feet | Cable attenuation in dB per 100 feet (from the cable manufacturer). |
| Available read points | Use `GET /cloud/readPoints` to see which read point IDs this reader has. |
