## 1. Description

The `PUT /cloud/gpo` REST endpoint sets the output state of a single General Purpose Output (GPO) pin on the reader.

This endpoint allows you to configure:

- The target GPO port number through `port`
- The desired output state through `state` (boolean: `true` = HIGH, `false` = LOW)

Use this endpoint to:

- Drive an external device such as a light stack, horn, or gate via a GPO pin
- Signal application logic results on physical outputs
- Toggle a GPO pin in response to tag read events or inventory state changes

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_gpo` |
| Pattern Name | GPO Control |
| REST Endpoint | `PUT /cloud/gpo` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `port`, `state` |
| Supported Port Values | 1-4 (varies by reader model - see `GET /cloud/readerCapabilities`) |

## 3. Before You Begin

Know the port number and desired output state before sending this request. Setting a port beyond the reader's capacity will result in an error.

| What You Need | Details |
|---|---|
| Port number | The GPO port to target (integer, 1-4). Use `GET /cloud/readerCapabilities` to confirm the maximum number of GPO pins available on this reader model. |
| Output state | `state` (boolean): `true` to drive the pin HIGH (active), `false` to drive the pin LOW (inactive). |
| External device wiring | Confirm the wired device is rated for the GPO pin's voltage and current output before asserting a HIGH state. |
