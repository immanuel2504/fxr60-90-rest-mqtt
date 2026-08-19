## 1. Description

The `DELETE /cloud/logs/syslog` REST endpoint purges system log files stored on the reader. When you call this endpoint, all accumulated syslog data is permanently deleted from the reader's storage.

Use this endpoint to:

- Clear syslog archives after downloading them with `GET /cloud/logs/syslog`
- Free flash storage consumed by accumulated system log data
- Reset the syslog before a diagnostic test run to ensure a clean capture

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Syslog Purge |
| REST Endpoint | `DELETE /cloud/logs/syslog` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Request Body | None |

## 3. Before You Begin

Archive the syslog files with `GET /cloud/logs/syslog` before sending this request if you need to retain them for support cases or post-incident analysis.

| What You Need | Details |
|---|---|
| Log retrieval | Confirm you have downloaded the syslog using `GET /cloud/logs/syslog` before purging. Deletion is permanent and cannot be undone. |
| Diagnostic baseline | If you plan to run a diagnostic session after purging, ensure all relevant services are in a known state before the purge so the new logs capture only the events of interest. |
