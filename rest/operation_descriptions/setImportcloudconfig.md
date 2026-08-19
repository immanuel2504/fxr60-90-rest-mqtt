## 1. Description

The `PUT /cloud/cloudConfig` REST endpoint imports a full cloud endpoint configuration onto the reader, defining how tag data, control responses, and management events are delivered to cloud systems.

This endpoint allows you to configure:

- Data event delivery endpoints through `endpointConfig.data.event`
- Control command-response channels through `endpointConfig.control.commandResponse`
- Management event channels through `endpointConfig.management.event`
- Management command-response channels through `endpointConfig.management.commandResponse`
- Batching and retention options per connection through `additionalOptions`

Use this endpoint to:

- Provision MQTT, HTTP POST, WebSocket, TCP/IP, Azure IoT Hub, or AWS IoT Core endpoints in a single request
- Configure control and management command channels alongside data delivery channels
- Set tag data retention and batching behavior
- Restore a full endpoint configuration from a saved profile during fleet provisioning

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Cloud Endpoint Configuration Import |
| REST Endpoint | `PUT /cloud/cloudConfig` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `endpointConfig` |
| Supported Connection Types | `mqtt`, `mqtt-AWS`, `mqtt-Azure`, `httpPost`, `WEBSOCKET`, `tcpip-server` |

## 3. Before You Begin

Gather all endpoint details before sending this request. An incorrect hostname, port, certificate reference, or topic will prevent the reader from connecting to your cloud backend.

| What You Need | Details |
|---|---|
| Endpoint channels | Decide which channels to configure: `data.event`, `control.commandResponse`, `management.event`, and/or `management.commandResponse`. Only include channels you are provisioning. |
| Connection type | Per connection, choose the transport type: `mqtt`, `mqtt-AWS`, `mqtt-Azure`, `httpPost`, `WEBSOCKET`, or `tcpip-server`. |
| Host, port, and topics | For MQTT connections: `hostName`, `port`, `protocol`, publish topics (`publishTopic`), and subscribe topics (`subscribeTopic` for command-response channels). |
| TLS and certificates | For secure connections: reference an installed certificate by name and type, or enable security and provide the CA certificate path. |
| MQTT client settings | `clientId`, `keepAlive`, `qos`, `cleanSession`, `reconnectDelay`, and `reconnectDelayMax` for each MQTT connection. |
| Retention and batching | For data event connections: configure `retention.maxNumEvents`, `retention.maxEventRetentionTimeInMin`, and `retention.throttle` as needed. |
| Local REST | For control channels: set `enableLocalRest: true` to allow local REST API access alongside cloud connectivity. |

## 4. Connection Types

| Type | Description |
|---|---|
| `mqtt` | Standard MQTT broker connection. |
| `mqtt-AWS` | AWS IoT Core MQTT connection. |
| `mqtt-Azure` | Azure IoT Hub MQTT connection. |
| `httpPost` | HTTP POST delivery for data events. |
| `WEBSOCKET` | WebSocket endpoint connection. |
| `tcpip-server` | TCP/IP server socket endpoint. |
