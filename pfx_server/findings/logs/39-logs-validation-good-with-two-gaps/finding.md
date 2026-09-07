# Finding 39 — `PUT /cloud/logs` validation is mostly good, with one gap and one inconsistency

**Endpoint** `PUT /cloud/logs`
**Type** Mixed — mostly ✅, two issues
**Status** Nine probes

| Probe | Response |
|---|---|
| `{"components":[{"componentName":"nosuch","level":"INFO"}]}` | 422 `Unsupported component provided` |
| `{"components":[{"componentName":"reader_gateway","level":"VERBOSE"}]}` | 422 `Unsupported cloud_agent or reader_gateway level provided` |
| `{"components":[{"componentName":"reader_gateway"}]}` | 422 `Invalid payload fields` |
| `{"components":[{"level":"INFO"}]}` | 422 `Invalid payload fields` |
| `{"components":[{"componentName":"reader_gateway","level":"info"}]}` | 422 — **case-sensitive** |
| `{"radioPacketLog":"true"}` | 422 `Invalid payload fields` — type checked |
| `{"components":{...}}` (object, not array) | 422 `Invalid payload fields` |
| `{"components":[]}` | ✅ 200 — reasonable no-op |
| `{}` | ⚠️ **200** — and silently resets `radioPacketLog` |

## What works well

Required fields are enforced as the schema specifies (both `componentName` and
`level` are required inside each component), types are checked on both
`radioPacketLog` and `components`, and level matching is case-sensitive — the
same as `/cloud/timeZone`.

## Gap 1 — `{}` is accepted

It returns 200 rather than a "payload required" error, and its only effect is to
disable `radioPacketLog` ([[34-omitting-radiopacketlog-disables-it]]). Compare
`PUT /cloud/displayConfig`, which returns `payload must be a non-empty JSON
object` for the same input.

## Gap 2 — the messages are inconsistent with each other

The same endpoint produces:

- a **precise, enumerated** message for a bad `radio_control` level —
  `TRACE is not an acceptable value for level (acceptable values are: ERROR, WARNING, INFO, DEBUG)`
  ([[32-level-enum-is-per-component]])
- a **generic** `Invalid payload fields`, naming no field at all, for a missing
  `level`, a missing `componentName`, a wrong type on `radioPacketLog`, and a
  wrong type on `components` — four different problems, one message

For a two-field object the generic message is tolerable, but the endpoint already
demonstrates it can do better.

## A cosmetic bug

An unknown log path returns 404 with a missing space:

```json
{"message":"/logs/nosuchlogis not a valid URI.Request not valid"}
```

The same defect appears on `/connectionStatus`, so it is likely a shared
URI-error formatter rather than anything specific to Logs.

## Evidence

`request body/` + `response body/` — `rest/cloud-logs-PUT/08-validation-probes/`
