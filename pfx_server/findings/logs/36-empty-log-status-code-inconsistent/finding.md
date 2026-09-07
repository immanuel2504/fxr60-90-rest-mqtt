# Finding 36 — ⚠️ `radioPacketLog` returns 422 when empty; `syslog` returns 200

**Endpoints** `GET /cloud/logs/radioPacketLog` vs `GET /cloud/logs/syslog`
**Type** Inconsistency between sibling endpoints
**Status** Confirmed, both immediately after their own `DELETE`

Two endpoints in the same family, both freshly purged by this same API, disagree
about how to report an empty log:

| After its `DELETE` | `GET` result |
|---|---|
| `syslog` | **200**, 396 B — archive with a 346-byte `messages` member |
| `radioPacketLog` | **422** `{"code":1,"message":"No radio packet logs available"}` |

## Why the 422 is the wrong choice

An empty log is a **legitimate, expected state** — especially straight after a
purge this API offers. A 4xx says the client did something wrong; nothing was
wrong.

The practical cost: a caller polling for logs must string-match
`"No radio packet logs available"` to distinguish "nothing to collect" from a
real failure. Any monitoring that treats 4xx as an alert will fire on a healthy
reader.

HTTP 200 with an empty archive — which is exactly what `syslog` does — or 204 No
Content would convey the same thing unambiguously.

## The two verbs also disagree with each other

On the *same* empty `radioPacketLog`:

| Verb | Response |
|---|---|
| `DELETE` (already empty) | **200** |
| `GET` (already empty) | **422** |

So "already empty" is fine for one verb and a client error for the other.

## Credit

The message itself is clear and specific — `"No radio packet logs available"`
says exactly what is going on. It is the status code and the inconsistency that
are the issue, not the wording.

## Ask

Make the two endpoints consistent, ideally 200 or 204, since an empty log is an
expected state after a purge this API provides.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-radiopacketlog-empty-422/` | `rest/cloud-logs-radioPacketLog-GET/02-empty-returns-422/` |
| `evidence-2-syslog-empty-200/` | `rest/cloud-logs-syslog-DELETE/01-purge-SUCCESS/` |

## Related

[[37-radiopacketlog-gates-generation-not-retrieval]] — the 422 means "empty", not "broken".
