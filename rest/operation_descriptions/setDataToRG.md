## 1. Description

The `PUT /cloud/setdataToRG` REST endpoint passes user application data into the reader gateway so that it is delivered through the reader's configured cloud endpoints.

When no user application is running, tag data flows from the radio straight to the reader gateway and out to the cloud. When a user application is running, that data is routed into the application instead — the application processes it, and its output then needs a route back into the delivery pipeline. This endpoint is that handoff.

## 2. Before You Begin

Confirm that both the user application and the reader gateway are in place before calling this endpoint. With nothing supplying data, or no gateway configured, the call may succeed but have no effect.

| What You Need | Details |
|---|---|
| User application | The application supplying the data must be installed and running. Confirm with `GET /cloud/apps` (`runningStatus: true`). |
| Reader gateway | Valid endpoint settings, so the gateway has somewhere to deliver the data (see `GET /cloud/config`). |
| Empty body | The endpoint rejects any request field. Send `{}`. |

## 3. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_dataToRG` |
| REST Endpoint | `PUT /cloud/setdataToRG` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Request body | None (empty object `{}`) |
| Related Endpoints | `GET /cloud/apps`, `PUT /cloud/apps/{appname}/pass-through`, `GET /cloud/config` |
