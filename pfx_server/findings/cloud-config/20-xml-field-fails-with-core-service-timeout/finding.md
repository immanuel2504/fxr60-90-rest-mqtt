# Finding 20 — The `xml` field fails with a Core Service timeout

**Endpoint** `PUT /cloud/config` (`xml`)
**Type** Unresolved — and a documentation gap
**Status** Failed, but **not** attributable to the field

Sending the spec's `xml` example verbatim:

```json
→ 422 {"code":6,"message":"Profile configuration failed: Timeout: failed to receive Core Service response"}
```

Note **code 6** and the timeout wording — a different failure class from the
`code 1` / `code 3` schema errors seen everywhere else. The request reached the
Core Service and no reply came back.

## This does not prove the field is broken

The spec's only `xml` example is a **55-character placeholder** containing
nothing but a comment:

```xml
<RFID><!-- Cloud Connect operational profile --></RFID>
```

An empty profile may simply be unprocessable, in which case a timeout is a poor
response but the field itself may be fine.

## The real blocker

Testing this properly needs a **real RFID operational profile document**, and the
spec does not provide one — which is itself worth raising. There is no way for an
integrator to exercise this field from the documentation alone.

## Ask

1. Ship a complete, valid `xml` operational profile example.
2. Should an empty or invalid profile time out, or be rejected with a schema
   error? A timeout gives the caller nothing to act on.

## Evidence

`request body/` + `response body/` — `rest/cloud-config-PUT/14-xml-operational-profile-FAILED/`
