# Finding 12 — The batching/retention dependency runs one way only

**Endpoint** `PUT /cloud/config` (`READER-GATEWAY`)
**Type** Clarification of [[11-batching-retention-require-endpointconfig]]
**Status** Confirmed

Test 13 sends `endpointConfig` with **no** `batching` and **no** `retention`, and
is accepted.

So the dependency is asymmetric:

| Request contains | Result |
|---|---|
| `batching` / `retention` without `endpointConfig` | ❌ rejected |
| `endpointConfig` without `batching` / `retention` | ✅ accepted |

`batching`/`retention` **require** `endpointConfig`; `endpointConfig` does **not**
require them.

Worth stating explicitly, because the error message in
[[11-batching-retention-require-endpointconfig]] talks about object *counts*,
which might suggest the two must always be supplied together in matching numbers.
They need not be.

## Evidence

`request body/` + `response body/` — `rest/cloud-config-PUT/13-clear-data-endpoint-SUCCESS/`
