## 1. Description

The `PUT /cloud/caCertificates/{caname}` REST endpoint installs a CA (Certificate Authority) root certificate on the reader by providing the PEM-encoded certificate content in the request body.

This endpoint allows you to configure:

- The CA certificate name through the `{caname}` path parameter
- The PEM-encoded certificate content through `content`

Use this endpoint to:

- Trust a private CA so the reader can validate TLS connections to your MQTT or HTTPS endpoints
- Add a CA root certificate required for chain validation before mutual TLS is configured
- Support your organization's PKI for both client and server TLS certificate validation

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | CA Certificate Installation |
| REST Endpoint | `PUT /cloud/caCertificates/{caname}` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Path Parameter | `caname` (the CA certificate name to install) |
| Required Request Fields | `content` |

## 3. Before You Begin

Have the CA certificate's PEM content ready before sending this request. Invalid PEM content will be rejected and the CA will not be installed.

| What You Need | Details |
|---|---|
| CA certificate name | A unique name to assign this CA certificate on the reader, supplied as the `{caname}` path parameter. If a CA with this name already exists, it will be replaced. |
| PEM content | The full PEM-encoded CA certificate string (`content`), including the `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----` headers and footers. |
| Certificate validity | Confirm the CA certificate is not expired before installing it. An expired CA root will still install but will fail to validate any certificates it issued. |
| Intended use | Know which MQTT broker or HTTP endpoint TLS certificate is issued by this CA, so you can verify the chain after installation with `GET /cloud/caCertificates`. |
