## 1. Description

The `GET /cloud/localRestLogin` REST endpoint authenticates to the reader and returns a bearer token for all other REST API calls.

On success, the response contains `code` (`0` = success) and `message` (the bearer token). No request body is required.

## 2. Authentication

If a bearer token has already been copied from the dashboard page, use it in **Authorize → bearerAuth**.

If not, enter Admin login credentials in **Authorize → basicAuth**, execute `GET /cloud/localRestLogin`, and copy the bearer token from the response into **Authorize → bearerAuth**.

| Scenario | Swagger UI steps |
|---|---|
| Already have a token | **Authorize → bearerAuth** → paste token → call other endpoints |
| Need a token | **Authorize → basicAuth** → run this endpoint → copy `message` → **Authorize → bearerAuth** |

This endpoint requires **HTTP Basic Auth** (admin credentials). All other `/cloud/*` endpoints require **bearerAuth**.

## 3. Endpoint Details

| Property | Value |
|---|---|
| REST Endpoint | `GET /cloud/localRestLogin` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | HTTP Basic Auth (admin reader credentials) |
