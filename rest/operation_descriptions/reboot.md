## 1. Description

The `PUT /cloud/reboot` REST endpoint restarts the reader. All in-progress operations stop and the reader disconnects until boot completes.

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

The reader disconnects until it finishes booting. Inventory and active connections stop.

| What You Need | Details |
|---|---|
| Downtime window | Wait until the reader is reachable again before sending further commands. |
