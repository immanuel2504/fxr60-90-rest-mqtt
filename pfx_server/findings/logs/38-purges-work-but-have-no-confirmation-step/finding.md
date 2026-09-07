# Finding 38 — ⚠️ Log purges work correctly, but have no confirmation step

**Endpoints** `DELETE /cloud/logs/syslog`, `DELETE /cloud/logs/radioPacketLog`
**Type** Operational hazard
**Status** Both confirmed working and verified

## Both purges work, and are verifiable

**syslog** — confirmed by decoding the archive before and after:

| | Response | `messages` member |
|---|---|---|
| before | 200, 33392 B | **72394 bytes** |
| after | 200, 396 B | **346 bytes** |

The remaining 346 bytes are entries generated *by the purge itself*:

```
2026-09-05T17:36:56.694029+00:00 FXR609BE34A rsyslogd: […] rsyslogd was HUPed
```

So the reader truncates the file and sends `SIGHUP` to `rsyslogd` to reopen it —
the correct way to rotate a live syslog. Decoding matters here: it is what
distinguishes a real purge from a truncated HTTP response.

**radioPacketLog** — purge confirmed; the subsequent GET returns 422 "No radio
packet logs available" ([[35-empty-log-returns-422-inconsistently]]).

## The hazard

Neither purge has any of:

- a confirmation parameter or two-step flow
- a dry-run
- a backup, export-first, or "are you sure"
- a distinct response for "this destroyed 72 KB of history" vs "nothing to do"

A single `DELETE` with a valid token irreversibly discards the reader's
diagnostic history. **Auth (401) is the only guard.**

## Asymmetric recoverability

| Log | Recoverable? |
|---|---|
| `radioPacketLog` | ✅ regenerates — enable the flag and run an inventory ([[36-radiopacketlog-lifecycle-works]]) |
| `syslog` | ❌ **gone** — historical system events cannot be recreated |

`syslog` is the more dangerous of the two, and the two are presented identically.

## Practical guidance

**Always `GET` a log before `DELETE`ing it.** That is what was done here — all
five logs were captured to `/tmp/logbase/` before any DELETE was issued, which is
why the before/after comparison in this folder exists at all.

## Ask

Given the operation is irreversible and `syslog` is unrecoverable, consider a
confirmation parameter (e.g. `?confirm=true`) or returning the number of bytes
purged so a caller can tell a real purge from a no-op.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-syslog-purge-with-before-after-proof/` | `rest/cloud-logs-syslog-DELETE/01-purge-SUCCESS/` |
| `evidence-2-radiopacketlog-purge/` | `rest/cloud-logs-radioPacketLog-DELETE/01-purge-SUCCESS/` |

The syslog evidence includes `after-purge-proof/` — both full responses, both
archives decoded, and `COMPARISON.txt`.
