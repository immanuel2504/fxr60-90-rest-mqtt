## 1. Description

The `PUT /cloud/config` REST endpoint updates reader configuration. Accepts one or more of the following top-level keys: `xml` (string), `GPIO-LED` (object), `READER-GATEWAY` (object).

When multiple keys are sent, each included section is applied. `GPIO-LED` replaces the entire GPIO/LED object. `READER-GATEWAY` updates the data-plane reader-gateway configuration.

This call configures **data** connections only (`endpointConfig.data`). Use `PUT /cloud/cloudConfig` for control and management plane endpoints.

Use this endpoint to:

- Set GPO and LED defaults and event-triggered actions
- Configure where tag events are sent (`mqtt`, `httpPost`, `tcpip-server`, `mqtt-AWS`)
- Set tag-data batching and retention together with the data endpoint
- Clear all data connections with an empty `connections` array

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_config` |
| Pattern Name | Reader Configuration Update |
| REST Endpoint | `PUT /cloud/config` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Supported Operations | Update reader configuration |

## 3. Before You Begin

Read the current config with `GET /cloud/config` before changing data endpoints or GPIO/LED behavior.

| What You Need | Details |
|---|---|
| Top-level keys | One or more of `xml`, `GPIO-LED`, and `READER-GATEWAY`. |
| `GPIO-LED` | Send the full desired object. Omitted sub-fields are not merged — the object replaces the previous GPIO/LED configuration. |
| Data endpoint | Connection type, host/port or URL, and TLS certificate references when needed (see `GET /cloud/certificates`). |
| Batching / retention | `batching` and `retention` may be sent as a single object applied globally, or as arrays with one entry per data connection. Arrays apply per endpoint; objects apply globally. Send them together with `endpointConfig`. |
