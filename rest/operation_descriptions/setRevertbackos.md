## 1. Description

The `PUT /cloud/revertbackOS` REST endpoint reverts the reader firmware to the previous OS version on the secondary partition.

Use this endpoint to:

- Roll back after a failed or unwanted `PUT /cloud/os` upgrade
- Restore the last known-good firmware
- Recover from compatibility issues with a new OS build

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Firmware Rollback |
| REST Endpoint | `PUT /cloud/revertbackOS` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Request Body | None |

## 3. Before You Begin

Plan for downtime — the reader reboots to the secondary partition to activate the previous firmware.

| What You Need | Details |
|---|---|
| Current firmware version | Use `GET /cloud/version` to confirm the current OS build (`readerApplication`). This endpoint does not return the backup OS version on the secondary partition. |
| Downtime window | The reader reboots to the secondary partition; allow time for the reboot and reconnect. |
