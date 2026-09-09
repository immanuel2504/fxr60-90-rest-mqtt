## 1. Description

The `PUT /cloud/pass-through` REST endpoint sends a command to a reader component, bypassing the standard API layer.

This endpoint sends:

- The target component through `component`
- The command string for that component through `payload`

Use this endpoint to:

- Query Radio Control status (`payload`: `status`)
- Read the Radio Control mode (`payload`: `mode`)

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_passthru` |
| Pattern Name | Pass-Through Command |
| REST Endpoint | `PUT /cloud/pass-through` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `component`, `payload` |
| Supported Components | `RC` (Radio Control) |

## 3. Before You Begin

| What You Need | Details |
|---|---|
| Component | Currently `RC` (Radio Control). |
| Payload | For `RC`: `mode` or `status`. |
