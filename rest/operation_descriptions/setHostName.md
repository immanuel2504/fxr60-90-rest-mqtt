## 1. Description

The `PUT /cloud/hostName` REST endpoint sets the network hostname of the reader.

This endpoint allows you to configure:

- The reader's network hostname through `hostname`

Use this endpoint to:

- Assign a recognizable hostname for network identification during provisioning
- Standardize hostname naming conventions across a fleet
- Update the hostname after a reader is relocated or re-provisioned

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_hostName` |
| Pattern Name | Hostname Configuration |
| REST Endpoint | `PUT /cloud/hostName` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `hostname` |

## 3. Before You Begin

Have the desired hostname ready before sending this request. Duplicate hostnames on the same network can cause resolution conflicts.

| What You Need | Details |
|---|---|
| Hostname string | The desired hostname (request body key: `hostname`). Must be a valid RFC 1123 hostname - lowercase alphanumeric characters and hyphens only; no underscores or spaces. |
| Network uniqueness | Verify the chosen hostname is not already in use on the network segment to avoid DNS or mDNS conflicts. |
