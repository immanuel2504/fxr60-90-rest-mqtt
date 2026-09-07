# Finding 04 — `timeZone` accepts an undocumented input vocabulary, and returns it

**Endpoint** `PUT /cloud/timeZone`
**Type** Spec-vs-firmware mismatch
**Status** Confirmed, and the changes verified against the reader's clock

The schema defines `timeZone` as a **closed enum** of 100+ display names
(`"Kolkata"`, `"Pacific Time (US & Canada)"`, `"London"`, …).

The reader accepts those — and also accepts IANA identifiers, which appear
nowhere in the enum:

| Sent | Accepted | `GET` returns |
|---|---|---|
| `"Kolkata"` (documented) | ✅ | `"Asia/Kolkata"` |
| `"Pacific Time (US & Canada)"` (documented) | ✅ | `"America/Los_Angeles"` |
| `"Asia/Kolkata"` (**not** in enum) | ✅ | `"Asia/Kolkata"` |
| `"UTC"` (documented) | ✅ | `"UTC"` |

## The problem

`GET` returns a form the schema does not document as valid input. A client
written strictly to the spec would treat the value it just read back as invalid.
Round-tripping `GET → PUT` does work, but only by relying on undocumented
behaviour.

`"UTC"` is the one case where input and output forms coincide, because it is
spelled the same in both vocabularies — which is exactly why testing only `UTC`
would have hidden this.

## The changes are real, not merely stored

`GET /cloud/status` `systemTime` moved correctly each time:

| Zone | `systemTime` | Offset |
|---|---|---|
| UTC | 16:49 | — |
| Asia/Kolkata | 22:18 | +5:30 ✅ |
| America/Los_Angeles | 09:48 | −7:00 ✅ |

## Case sensitivity

Matching is **case-sensitive** — `{"timeZone":"utc"}` is rejected. The error is
identical to the one for a wholly non-existent zone
(`Invalid Time Zone specified.`), so it gives no hint that case is the problem.

## Ask

Either document the IANA forms as accepted input, or have `GET` return the
documented display name. And consider distinguishing a casing mistake from an
unknown zone in the error.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-iana-name-accepted/` | `rest/cloud-timeZone-PUT/04-iana-roundtrip-SUCCESS/` |
| `evidence-2-documented-name-returns-iana/` | `rest/cloud-timeZone-PUT/01-kolkata-SUCCESS/` |
