## 1. Description

The `PUT /cloud/hostName` REST endpoint sets the reader's network hostname.

This endpoint sends:

- `hostname` — the hostname to assign

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
| Request field | `hostname` |

## 3. Before You Begin

| What You Need | Details |
|---|---|
| Hostname | The value to assign. |
