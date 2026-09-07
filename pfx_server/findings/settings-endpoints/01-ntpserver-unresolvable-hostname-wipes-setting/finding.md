# Finding 01 — 🐛 An unresolvable NTP hostname returns HTTP 200 and wipes the setting

**Endpoint** `PUT /cloud/ntpServer`
**Severity** High — silent, destructive, and delayed in its effects
**Status** Reproduced 3/3 runs per key, on both `server` and `server1`

## What happens

```
before: {"server":"pool.ntp.org"}
PUT     {"server":"nosuch1.invalid.example"}   → HTTP 200, empty body
after:  {"server":""}
```

The reader is left with **no NTP server configured**, and the caller is told the
request succeeded.

| Key | Runs | Before | Response | After |
|---|---|---|---|---|
| `server` | 3/3 | `pool.ntp.org` | **200** | `""` 🐛 |
| `server1` | 3/3 | `pool.ntp.org` | **200** | `""` 🐛 |

Each run used a different unresolvable name, resetting to a known-good value
first.

## The endpoint already gets this right for other bad input

A *malformed* hostname is rejected, and the previous value survives:

```json
PUT {"server":"not..a..host"}
→ 422 {"code":3,"message":"CS:'setNTPServerRsp' failed,Reason: SNTP_INVALID_SERVER_FORMAT"}
GET → {"server":"pool.ntp.org"}     previous value INTACT ✅
```

So the correct behaviour exists in the endpoint. It simply is not applied to
names that are syntactically valid but do not resolve.

## Two separable problems

1. **The response is wrong.** An input the reader cannot use should be a 4xx, as
   the malformed case already is — not HTTP 200.
2. **The failure is destructive.** Whether or not the new value is accepted, a
   failed update should leave the previous working value in place. Wiping to `""`
   is worse than either accepting or rejecting it.

## Why it matters

Silent and delayed. The caller has no reason to re-check, and the consequence —
a reader that cannot synchronise its clock — surfaces later as certificate
validity failures and wrong event timestamps, far from the cause. A single typo
in a hostname is enough to trigger it.

## Ask

Return a 4xx for a hostname the reader cannot use, and never destroy the previous
working value on a failed update.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-unresolvable-hostname/` | `rest/cloud-ntpServer-PUT/07-unresolvable-hostname-BUG-silently-wipes/` |
| `evidence-2-malformed-hostname-correctly-rejected/` | `rest/cloud-ntpServer-PUT/06-invalid-hostname-REJECTED/` |

## Related

[[02-oneof-branches-both-work]] — the correction that isolated this finding's real cause.
