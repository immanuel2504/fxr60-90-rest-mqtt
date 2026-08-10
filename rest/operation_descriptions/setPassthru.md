## 1. Description

The `PUT /cloud/pass-through` REST endpoint sends a pass-through payload directly to a specific reader component, bypassing the standard API layer.

This endpoint allows you to configure:

- The target component through `component`
- The raw command or query string to send to that component through `payload`

Use this endpoint to:

- Forward component-specific commands not covered by standard REST API operations
- Query or control low-level reader component behavior for diagnostics
- Support vendor-specific or advanced troubleshooting workflows

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Pass-Through Command |
| REST Endpoint | `PUT /cloud/pass-through` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `component`, `payload` (inner) |
| Supported Components | `RC` (Radio Control) |

## 3. Before You Begin

Know the target component and the exact payload string it expects before sending this request. Invalid pass-through commands may produce component-specific errors that are not surfaced through standard error codes.

| What You Need | Details |
|---|---|
| Component name | The reader component to target. Currently supported: `RC` (Radio Control). |
| Payload string | The command or query string expected by the target component (for the `RC` component, common values include `mode` and `status`). The format is component-specific and must be obtained from the component's low-level documentation. |
