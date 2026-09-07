# Finding 11 — `batching` and `retention` cannot be sent without `endpointConfig`

**Endpoint** `PUT /cloud/config` (`READER-GATEWAY`)
**Type** Spec-vs-firmware mismatch + misleading error
**Status** Confirmed both ways

The schema says `READER-GATEWAY` needs "at least one of" four keys. In practice
`batching` and `retention` are rejected unless `endpointConfig` accompanies them.

```json
READER-GATEWAY with batching + retention only
→ {"code":1,"message":"Invalid global batching payload fields: Batching configuration error: Incorrect number of batching objects for the given endpoints"}
```

Retried with `retention` alone — same class of error:

```
"retention configuration error: Incorrect number of retention objects for the given endpoints"
```

## The count was not the problem

At the time of the test the reader had exactly **one** data endpoint
(`DATA_HTTP`), its stored batching had exactly **one** object, and exactly **one**
was sent. The counts matched.

**Root cause:** the reader counts `batching`/`retention` objects against the
endpoints *present in the same request*, not against the endpoints already
configured. With no `endpointConfig` in the request the endpoint count is zero,
so any number of batching objects is "incorrect".

## The error message points at the wrong thing

It blames the object count when the real problem is a missing `endpointConfig`.
Something like *"batching requires endpointConfig in the same request"* would
have been far faster to act on.

## Ask

Correct the schema (or the validator), and fix the message.

## Related

[[12-batching-dependency-is-one-way]] — the dependency does not run in reverse.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-rejected-alone/` | `rest/cloud-config-PUT/02b-batching-retention-alone-REJECTED/` |
| `evidence-2-accepted-with-endpointconfig/` | `rest/cloud-config-PUT/02-batching-retention-with-endpointConfig/` |
