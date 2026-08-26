## 1. Description

The `PUT /cloud/reboot` REST endpoint restarts the reader. All in-progress operations stop and the reader briefly disconnects until boot completes.

This endpoint requires:

- No request body — the endpoint takes no parameters

Use this endpoint to:

- Apply configuration changes that require a restart
- Recover from an unhealthy reader state
- Complete a firmware update cycle (the reader may reboot automatically after `PUT /cloud/os`)

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `reboot` |
| Pattern Name | Reader Restart |
| REST Endpoint | `PUT /cloud/reboot` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Request Body | None |

## 3. Before You Begin

Plan for downtime — the reader will disconnect until it finishes booting. In-flight inventory and active connections will be interrupted.

| What You Need | Details |
|---|---|
| Downtime window | Allow 1–3 minutes for reboot and reconnect |
