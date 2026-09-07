# Finding 02 — Both `oneOf` branches work (a correction)

**Endpoint** `PUT /cloud/ntpServer`
**Status** ✅ Schema is accurate — this documents a **withdrawn** finding

## The claim that was wrong

An earlier version of the report named the documented `server1` ("legacy") key as
the cause of the NTP wipe in [[01-ntpserver-unresolvable-hostname-wipes-setting]].
That was **wrong**.

The original test alternated `server` and `server1` payloads and saw a clean
split, 5/5 runs. It looked conclusive. But it had confounded two variables:

| Key tested with | Hostname | Resolves? |
|---|---|---|
| `server` | `time1.google.com` | ✅ yes |
| `server1` | `timeA.google.com` | ❌ NXDOMAIN |
| `server1` | `solo.google.com` | ❌ NXDOMAIN |
| `server1` | `verify.google.com` | ❌ NXDOMAIN |

Every hostname that happened to be paired with `server1` was NXDOMAIN.

## Re-tested as a 2×2

| | `time.cloudflare.com` (resolves) | `nosuch.invalid.example` (NXDOMAIN) |
|---|---|---|
| `server` | `time.cloudflare.com` ✅ | `""` 🐛 |
| `server1` | `time.cloudflare.com` ✅ | `""` 🐛 |

The key makes no difference; resolvability decides.

## Conclusion

`server1` works correctly — 3/3 runs with a resolvable host. **The schema's
`oneOf` is accurate**: both conventions are honoured, and the response normalises
either one to `server` on read-back.

## The methodological lesson

When a split looks clean, check that only one variable actually differs between
the two arms. A 5/5 result is not evidence of the right cause if a second
variable moved with the first.

## Evidence

`request body/` + `response body/` — `rest/cloud-ntpServer-PUT/02-server1-legacy-SUCCESS/`
