## 1. Description

The `GET /cloud/localRestLogin` REST endpoint returns a bearer token.

This endpoint returns:

- `code` — `0` on success
- `message` — the bearer token

No request body.

Send the token as `Authorization: Bearer <token>` on other REST calls.

## 2. Endpoint Details

| Property | Value |
|---|---|
| REST Endpoint | `GET /cloud/localRestLogin` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | HTTP Basic Auth (admin reader credentials) |

## 3. Before You Begin

Use HTTP Basic Auth with the reader admin username and password.
