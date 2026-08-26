## 1. Description

The `PUT /cloud/updatePassword` REST endpoint allows you to edit the `admin` and `rfidadm` password.

Only the password is changed. `userName` selects **which** of the two accounts to update — it does not rename an account, and it cannot create one.

This endpoint allows you to configure:

- Which account to change through `userName` (`admin` or `rfidadm`)
- That account's existing password through `currentPassword`
- The new password to set through `newPassword`

Use this endpoint to:

- Rotate reader credentials as part of a security policy
- Set a new password during initial reader provisioning
- Respond to a credential exposure or security incident

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

Confirm the current password and the target account before sending this request. Using the wrong current password will cause the request to fail.

| What You Need | Details |
|---|---|
| Account | Which account to change, supplied in `userName`: `admin` or `rfidadm`. This selects the account only — the account itself is not renamed. |
| Current password | The account's existing password. Required for authentication - the request will fail if this is incorrect. |
| New password | The new password to set. Apply your organization's password policy (minimum length, complexity requirements). |
