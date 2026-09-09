## 1. Description

The `PUT /cloud/config` REST endpoint updates GPIO/LED behavior and the data-plane reader-gateway configuration.

Send at least one of `GPIO-LED` or `READER-GATEWAY`. Both can be sent in the same request.

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

A misconfigured data endpoint can stop tag reporting. Read the current config with `GET /cloud/config` first — especially `GPIO-LED`, which is replaced wholesale.

| What You Need | Details |
|---|---|
| Configuration scope | At least one of `GPIO-LED` or `READER-GATEWAY`. |
| GPIO/LED | The full desired `GPIO-LED` object. GPO defaults are `HIGH`/`LOW`. LED colors are `GREEN`/`RED`/`AMBER`. |
| Data endpoint | Connection type, host/port or URL, and TLS material if needed (see `GET /cloud/certificates`). |
| Batching / retention | Send as arrays, and only together with `endpointConfig`. |
