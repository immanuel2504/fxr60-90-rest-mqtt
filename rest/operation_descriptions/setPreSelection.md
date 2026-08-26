## 1. Description

The `PUT /cloud/preSelection` REST endpoint enables or disables the rxSawFilter pre-selection feature on the reader.

This endpoint allows you to configure:

- The rxSawFilter (receive SAW filter pre-selection) state through `preSelection`

Use this endpoint to:

- Enable rxSawFilter to improve receiver selectivity in noisy RF environments
- Disable rxSawFilter when operating in clean RF environments where sensitivity is the priority
- Tune receiver filtering behavior before starting RFID inventory

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_preSelection` |
| Pattern Name | rxSawFilter Configuration |
| REST Endpoint | `PUT /cloud/preSelection` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Request Fields | `preSelection` |

## 3. Before You Begin

Determine the appropriate rxSawFilter state for the deployment environment before sending this request. Use `GET /cloud/preSelection` to check the current state before changing it.

| What You Need | Details |
|---|---|
| Filter state | `true` to enable rxSawFilter (better selectivity in noisy environments), or `false` to disable it (better sensitivity in clean environments). |
| Deployment RF environment | Consider enabling the filter when the reader operates near other UHF RFID systems or dense RF infrastructure. Disable it in quiet, isolated RF environments to maximize read range. |
