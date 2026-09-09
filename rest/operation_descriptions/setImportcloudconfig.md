## 1. Description

The `PUT /cloud/cloudConfig` REST endpoint imports cloud endpoint configuration onto the reader: data events, control command-response, and management channels.

Send `endpointConfig`. Only the sections you include are updated; omitted sections are left unchanged. This call does not set GPIO-LED or `managementEventConfig` — use `PUT /cloud/config` for those.

This endpoint allows you to configure:

- Data event delivery through `endpointConfig.data.event`
- Control command-response through `endpointConfig.control.commandResponse`
- Management events through `endpointConfig.management.event`
- Management command-response through `endpointConfig.management.commandResponse`
- Batching and retention per connection through `additionalOptions`

Use this endpoint to:

- Provision MQTT, HTTP POST, WebSocket, TCP/IP, Azure IoT Hub, or AWS IoT Core endpoints
- Configure control and management channels alongside data delivery
- Set tag-data retention and batching
- Clear data connections with an empty `connections` array

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_importCloudConfig` |
| Pattern Name | Cloud Endpoint Configuration Import |
| REST Endpoint | `PUT /cloud/cloudConfig` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `endpointConfig` |
| Supported Connection Types | `mqtt`, `mqtt-GCP`, `mqtt-AWS`, `mqtt-Azure`, `httpPost`, `WEBSOCKET`, `tcpip-server`, `keyboard-emulation` |

## 3. Before You Begin

Gather endpoint details before sending this request. An incorrect hostname, port, certificate, or topic will prevent the reader from connecting.

| What You Need | Details |
|---|---|
| Endpoint channels | `data.event`, `control.commandResponse`, `management.event`, and/or `management.commandResponse`. Include only the channels you are changing. |
| Connection type | Per connection: `mqtt`, `mqtt-GCP`, `mqtt-AWS`, `mqtt-Azure`, `httpPost`, `WEBSOCKET`, `tcpip-server`, or `keyboard-emulation`. |
| Host, port, and topics | For MQTT: `hostName`, `port`, `protocol`, `publishTopic`, and `subscribeTopic` (command-response channels). |
| TLS and certificates | Reference an installed certificate, or provide certificate file paths (see `GET /cloud/certificates`). |
| MQTT client settings | `clientId`, `keepAlive`, `qos`, `cleanSession`, `reconnectDelay`, and `reconnectDelayMax`. |
| Retention and batching | For data events: `retention.maxNumEvents`, `retention.maxEventRetentionTimeInMin`, and `retention.throttle`. |
| Local REST | For control channels: `enableLocalRest: true` keeps local REST available alongside cloud connectivity. |
