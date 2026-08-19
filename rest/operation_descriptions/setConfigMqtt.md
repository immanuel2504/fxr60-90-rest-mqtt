## 1. Description

The `PUT /cloud/config` REST endpoint updates the reader's full configuration, including RF settings, GPIO and LED defaults, and reader-gateway endpoint configuration.

Use this endpoint to:

- Configure GPIO/LED default states and event-triggered actions
- Set tag-data retention, batching, and data/management endpoint connections

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Reader Configuration Update |
| REST Endpoint | `PUT /cloud/config` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Supported Operations | Update reader configuration |

## 3. Before You Begin

Gather these details before sending the request. A misconfigured endpoint can disrupt tag reporting and management events.

| What You Need | Details |
|---|---|
| Configuration scope | Partial or full `GPIO-LED` and/or `READER-GATEWAY` objects. |
| GPIO/LED defaults | Desired GPO pin defaults (`HIGH`/`LOW`) and LED colors per pin. |
| Endpoint connections | Data and management channel types (`mqtt`, `httpPost`, `tcpip-server`, etc.) with host, port, and security. |
| Certificates | Pre-installed or inline PEM content for TLS endpoints (see `GET /cloud/certificates`). |
