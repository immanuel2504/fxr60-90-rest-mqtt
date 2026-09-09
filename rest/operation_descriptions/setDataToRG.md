## 1. Description

The `PUT /cloud/setdataToRG` REST endpoint sends user-application output into the reader gateway.

Send `{}`.

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_dataToRG` |
| Pattern Name | User Application Data to Gateway |
| REST Endpoint | `PUT /cloud/setdataToRG` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Request Body | None |
