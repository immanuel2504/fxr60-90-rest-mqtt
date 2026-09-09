## 1. Description

The `PUT /cloud/updatePassword` REST endpoint changes the reader login password for `admin` or `rfidadm`.

`userName` selects which of those two accounts to update. It does not rename an account, and it cannot create one.

This endpoint requires:

- `userName` — `admin` or `rfidadm`
- `currentPassword` — the account's existing password
- `newPassword` — the password to set

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_password` |
| Pattern Name | Password Change |
| REST Endpoint | `PUT /cloud/updatePassword` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `userName`, `currentPassword`, `newPassword` |

## 3. Before You Begin

The current password must be correct or the request fails.

| What You Need | Details |
|---|---|
| Account | `admin` or `rfidadm`. |
| Current password | The account's existing password. |
| New password | The password to set. |
