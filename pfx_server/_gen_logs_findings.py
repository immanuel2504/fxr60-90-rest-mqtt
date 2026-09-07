#!/usr/bin/env python3
"""Build findings/logs/ - one folder per tested finding from the Logs group."""
import os
import shutil

ROOT = "/home/altautoadmin/pfx_server"
REST = os.path.join(ROOT, "rest")


def build(num, slug, evidence, md):
    d = os.path.join(ROOT, "findings", "logs", f"{num}-{slug}")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "finding.md"), "w").write(md)
    for i, (src, label) in enumerate(evidence):
        base = d if len(evidence) == 1 else os.path.join(d, f"evidence-{i+1}-{label}")
        for sub in ("request body", "response body"):
            s = os.path.join(src, sub)
            if not os.path.isdir(s):
                continue
            t = os.path.join(base, sub)
            shutil.rmtree(t, ignore_errors=True)
            shutil.copytree(s, t)
        open(os.path.join(base, "SOURCE.txt"), "w").write(
            f"Copied verbatim from:\n  {os.path.relpath(src, ROOT)}\n\n"
            "That folder is the canonical record of this test; this is a copy kept\n"
            "beside the finding so the evidence travels with it.\n")


def t(ep, n):
    p = os.path.join(REST, ep)
    for f in sorted(os.listdir(p)):
        if f.startswith(n + "-") and os.path.isdir(os.path.join(p, f)):
            return os.path.join(p, f)
    raise SystemExit(f"no {ep} test {n}")


build("30", "radio-control-level-cannot-be-set",
      [(t("cloud-logs-PUT", "03"), "level-never-changes"),
       (t("cloud-logs-PUT", "05"), "reader-gateway-works-positive-control")],
"""# Finding 30 — 🐛 `radio_control`'s log level cannot be set

**Endpoint** `PUT /cloud/logs`
**Severity** High — the field validates, returns 200, then discards the value
**Status** Confirmed across every level the reader itself accepts

## What happens

```
PUT {"components":[{"componentName":"radio_control","level":"DEBUG"}]}
→ 200
GET → {"components":[{"componentName":"radio_control","level":"INFO"}, …]}
```

Tested with all four levels the reader validates as acceptable for
`radio_control`, each sent alone with a settle and a read-back:

| Sent | Response | `radio_control` after |
|---|---|---|
| `ERROR` | 200 | `INFO` |
| `WARNING` | 200 | `INFO` |
| `DEBUG` | 200 | `INFO` |
| `INFO` | 200 | `INFO` (no-op) |

Also with both components in one request:

```
PUT {"components":[{"componentName":"radio_control","level":"DEBUG"},
                   {"componentName":"reader_gateway","level":"ERROR"}]}
→ 200,  read back: radio_control=INFO   reader_gateway=ERROR
```

The `reader_gateway` half applied. The `radio_control` half did not.

## Why this is more than a no-op

The endpoint **validates this field specifically for this component**. An invalid
level for `radio_control` is rejected with a precise, component-specific error
naming its real enum (see
[[33-log-level-enum-is-per-component]]) — which proves the value reaches the
`radio_control` validator. It is then accepted and dropped.

Validating a field and then ignoring it is worse than either rejecting it or
honouring it: the specific error message is positive evidence to the caller that
the field is live.

## Positive control

`reader_gateway` honours **all eight** documented levels, each verified by
read-back. So the endpoint, the level enum and the read-back all work — the
failure is specific to `radio_control`, not to the test method.

## Not established

Whether the level is genuinely applied internally and merely mis-reported by
`GET /cloud/logs`. Distinguishing those needs a log-volume comparison at `ERROR`
vs `DEBUG`, which was not run. Either way the API is unusable for this purpose:
a caller has no way to confirm the setting took.

## Ask

If `radio_control`'s level is fixed, reject the request. If it is settable, make
`GET /cloud/logs` report the value that was set.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-level-never-changes/` | `rest/cloud-logs-PUT/03-radio-control-level-never-changes/` |
| `evidence-2-reader-gateway-works-positive-control/` | `rest/cloud-logs-PUT/05-all-eight-levels-on-reader-gateway-SUCCESS/` |

## Related

[[31-component-names-silently-redirected]] · [[33-log-level-enum-is-per-component]]
""")

build("31", "component-names-silently-redirected",
      [(t("cloud-logs-PUT", "02"), "all-five-names-probed"),
       (t("cloud-logs-PUT", "01"), "spec-example-half-ignored")],
"""# Finding 31 — 🐛 Three of the five documented `componentName` values are silently redirected

**Endpoint** `PUT /cloud/logs`
**Severity** High — silent, and the spec's own example is affected
**Status** Confirmed by sending each name alone with a distinctive level

## What the schema documents

Five accepted values, described as:

> Supported canonical names are `radio_control` and `cloud_agent`. Supported
> aliases are `RC` for `radio_control` and `RG` for `reader_gateway`.

So the documented mapping is:

| Documented target | Names |
|---|---|
| `radio_control` | `radio_control`, `RC` |
| `reader_gateway` | `reader_gateway`, `RG` |
| `cloud_agent` | `cloud_agent` |

## What actually happens

Each name sent alone, with a distinctive level, then read back:

| Sent | Response | Landed on | Correct? |
|---|---|---|---|
| `radio_control: DEBUG` | 200 | **`reader_gateway`** | ❌ |
| `RC: DEBUG` | 200 | **`reader_gateway`** | ❌ |
| `cloud_agent: ERROR` | 200 | **`reader_gateway`** | ❌ |
| `reader_gateway: TRACE` | 200 | `reader_gateway` | ✅ |
| `RG: WARNING` | 200 | `reader_gateway` | ✅ |

**All five names write to `reader_gateway`.** Three of them are documented to go
somewhere else.

## Two consequences

1. **`radio_control` and `RC` do not set `radio_control`.** The documented alias
   mapping is wrong, or the implementation is. (`radio_control`'s level is also
   unsettable by any route — [[30-radio-control-level-cannot-be-set]].)

2. **`cloud_agent` is not a distinct component here.** It writes to
   `reader_gateway`, and the name never appears in any `GET /cloud/logs`
   response. Either it *is* `reader_gateway` under another name — in which case
   the schema is misleading, since it presents them as separate — or the
   component does not exist on this firmware.

   Supporting evidence: the validation error for a bad level reads
   `"Unsupported cloud_agent or reader_gateway level provided"`, naming the two
   together as if they share one setting.

`GET /cloud/logs` only ever reports **two** components: `radio_control` and
`reader_gateway`.

## The spec's own example is affected

```json
{"components":[{"componentName":"radio_control","level":"DEBUG"},
               {"componentName":"cloud_agent","level":"DEBUG"}],
 "radioPacketLog":true}
```

Returns 200. Of the three things it asks for, only `radioPacketLog: true` is
applied as written — `cloud_agent`'s level lands on `reader_gateway`, and
`radio_control`'s is discarded. Nothing in the response indicates this.

## Ask

Correct either the schema's name mapping or the implementation, and make the
spec's example one that works as written. If `cloud_agent` and `reader_gateway`
are the same component, document them as aliases.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-all-five-names-probed/` | `rest/cloud-logs-PUT/02-all-component-names-write-to-reader-gateway/` |
| `evidence-2-spec-example-half-ignored/` | `rest/cloud-logs-PUT/01-spec-example-PARTIALLY-SILENTLY-IGNORED/` |
""")

build("32", "omitting-radiopacketlog-disables-it",
      [(t("cloud-logs-PUT", "07"), "omission-resets-to-false"),
       (t("cloud-logs-PUT", "06"), "toggle-works-when-sent")],
"""# Finding 32 — Omitting `radioPacketLog` silently disables it

**Endpoint** `PUT /cloud/logs`
**Type** Mixed merge semantics, undocumented
**Status** Confirmed, including via the empty body

Changing a component's log level **silently turns off the radio packet log**:

```
before  {"components":[…reader_gateway=TRACE…], "radioPacketLog":true}
PUT     {"components":[{"componentName":"reader_gateway","level":"INFO"}]}   → 200
after   {"components":[…reader_gateway=INFO…],  "radioPacketLog":false}   ← reset
```

The empty body does the same:

```
before  {…, "radioPacketLog":true}
PUT     {}                                                    → 200
after   {…, "radioPacketLog":false}   ← reset, levels untouched
```

Note `{}` returns 200 rather than a "payload required" error, and its **only**
effect is to disable packet logging.

## The semantics are mixed, per field

| Field | Omitted from request |
|---|---|
| `components` | **preserved** — levels survive |
| `radioPacketLog` | **reset to default** — reverts to `false` |

A caller cannot reason about this endpoint as either "merge" or "replace". It is
one of each, and neither is documented.

## Why it matters

`radioPacketLog` is a real functional switch, not a stored flag — it gates packet
log *generation* ([[36-radiopacketlog-lifecycle-works]]). So a PUT that changes
only a log level stops packet capture, with HTTP 200 and no indication. Anyone
raising a log level to investigate a radio problem would disable the most
relevant log in the same request.

## Practical guidance

**Always send `radioPacketLog` explicitly on every `PUT /cloud/logs`**, even when
only changing a level.

## Three endpoints, three semantics

| Endpoint | Partial update |
|---|---|
| `PUT /cloud/logs` | **mixed** — `components` merge, `radioPacketLog` resets |
| `PUT /cloud/displayConfig` | merges every field |
| `PUT /cloud/config` → `GPIO-LED` | replaces wholesale |

None documented. See [[08-displayconfig-merges-partial-updates]] and
[[13-gpio-led-replaces-wholesale]].

## Ask

Document the per-field semantics, and preserve `radioPacketLog` when it is
omitted.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-omission-resets-to-false/` | `rest/cloud-logs-PUT/07-omitting-radiopacketlog-resets-it-to-false/` |
| `evidence-2-toggle-works-when-sent/` | `rest/cloud-logs-PUT/06-radiopacketlog-toggle-SUCCESS/` |
""")

build("33", "log-level-enum-is-per-component",
      [(t("cloud-logs-PUT", "04"), "radio-control-rejects-four-levels"),
       (t("cloud-logs-PUT", "05"), "reader-gateway-accepts-all-eight")],
"""# Finding 33 — The log level enum is per-component, but the schema declares one shared enum

**Endpoint** `PUT /cloud/logs`
**Type** Spec-vs-firmware mismatch
**Status** Confirmed by testing all 8 levels against both components

The schema declares **one** `level` enum, shared by every component, with 8
values:

```
OFF  FATAL  ERROR  WARNING  DEBUG  INFO  TRACE  EXTRA
```

The firmware enforces a different set per component. All 8 sent to each:

| Level | `reader_gateway` | `radio_control` |
|---|---|---|
| `OFF` | ✅ 200 | ❌ 422 |
| `FATAL` | ✅ 200 | ❌ 422 |
| `ERROR` | ✅ 200 | ✅ 200 |
| `WARNING` | ✅ 200 | ✅ 200 |
| `DEBUG` | ✅ 200 | ✅ 200 |
| `INFO` | ✅ 200 | ✅ 200 |
| `TRACE` | ✅ 200 | ❌ 422 |
| `EXTRA` | ✅ 200 | ❌ 422 |

So:

| Component | Levels supported |
|---|---|
| `reader_gateway` | **8** — the full documented enum |
| `radio_control` | **4** — `ERROR`, `WARNING`, `INFO`, `DEBUG` |

## The reader names its own enum

```json
{"code":3,"message":"\\"set_logs\\" Failed to apply. Description: unsuccessful rc response: Failure: TRACE is not an acceptable value for level (acceptable values are: ERROR, WARNING, INFO, DEBUG)"}
```

**This is the best error message on the endpoint** — it names the offending value
*and* lists the acceptable ones, which is how the real enum was discovered.
Compare the generic `"Unsupported cloud_agent or reader_gateway level provided"`
returned for a bad `reader_gateway` level, which lists nothing.

## Why it matters

A client sending a documented level to a documented component receives a 422 with
no way to have predicted it from the spec. A single shared enum cannot express
this.

## Caveat

The four levels `radio_control` *does* accept still have no visible effect — see
[[30-radio-control-level-cannot-be-set]]. So in practice `radio_control` accepts
four levels at the validator and honours none of them.

## Ask

Document the per-component level sets, or accept all eight for both. And apply
the `radio_control` error message's style — value plus acceptable list —
everywhere.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-radio-control-rejects-four-levels/` | `rest/cloud-logs-PUT/04-radio-control-rejects-four-documented-levels/` |
| `evidence-2-reader-gateway-accepts-all-eight/` | `rest/cloud-logs-PUT/05-all-eight-levels-on-reader-gateway-SUCCESS/` |
""")

build("34", "log-retrieval-response-shape-undocumented",
      [(t("cloud-logs-syslog-GET", "01"), "syslog"),
       (t("cloud-logs-RcLog-GET", "01"), "rclog")],
"""# Finding 34 — The log retrieval response shape is undocumented

**Endpoints** `GET /cloud/logs/{syslog,RcLog,RgWarningLog,RgErrorLog,radioPacketLog}`
**Type** Documentation gap
**Status** All five confirmed working; shape identical across all of them

All five log GETs return HTTP 200 with the same envelope:

```json
{"binary": "<base64 of a gzipped tar>", "filename": "syslog.tar.gz"}
```

**The spec defines no response schema for any of them** — only the path, the
`operationId` and a one-line summary. A client has no documented way to know the
payload is base64, that it is gzip, that it is a tar, or that `filename` exists.

## Verified content

Every response decodes to a valid gzip (magic `1f8b`) and opens as a tar:

| Endpoint | Response | Archive | Members |
|---|---|---|---|
| `syslog` | 13 KB | `syslog.tar.gz` | `messages` (72 KB) |
| `RcLog` | 608 KB | `rcLog.tar.gz` | live log + 2 rotations, ~5 MB each |
| `RgWarningLog` | 426 B | `rgWarningLog.tar.gz` | 6 files, one per gateway restart |
| `RgErrorLog` | 3.8 KB | `rgErrorLog.tar.gz` | 6 files, 184 B – 8.9 KB |
| `radioPacketLog` | 602 KB | `radioPktLog.tar.gz` | 4 × ~1 MiB packet logs |

Rotation sizes are inferable from the members: `radio_control.log.N` at ~5 MB,
`packet_log-N.txt` at exactly 1 MiB.

`RgWarningLog` and `RgErrorLog` use one file per reader-gateway restart, named
`warning-<ISO8601>-0.txt` / `error-<ISO8601>-0.txt`. The six timestamps
(14:55, 14:58, 15:00, 15:08, 15:20, 16:03) line up with the gateway restarts
caused by the endpoint reconfiguration testing in `cloud-config-PUT/` and
`cloud-cloudConfig-PUT/` — which makes `RgErrorLog` the natural place to look for
the reader side of the error-255 connection failures in
[[16-cloud-connect-fires-on-failed-attempt]].

Every warning file contains only a date line and no warnings.

## No parameters of any kind

None of the five declares a parameter, and none was found. There is no way to:

- filter by time range or severity
- limit the number of lines
- page through a large log

`RcLog` returns ~10.5 MB uncompressed in a single response. On a constrained link
that is the only option available.

## How to extract

```bash
curl -sk -H "Authorization: Bearer $TOKEN" \\
  https://10.233.48.36/cloud/logs/syslog \\
| python3 -c "
import sys,json,base64
d=json.load(sys.stdin)
open(d['filename'],'wb').write(base64.b64decode(d['binary']))
print('wrote', d['filename'])"
tar tzf syslog.tar.gz
```

## Ask

1. Document the response schema — `binary` (base64 gzip tar) and `filename`.
2. Consider a time-range or line-limit parameter, and/or `Content-Type:
   application/gzip` with the raw bytes instead of base64-in-JSON, which costs
   33% overhead on a 10 MB log.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-syslog/` | `rest/cloud-logs-syslog-GET/01-retrieve-SUCCESS/` |
| `evidence-2-rclog/` | `rest/cloud-logs-RcLog-GET/01-retrieve-SUCCESS/` |

Both carry the **complete** response including the full base64, plus the decoded
archive and its extracted members under `response body/decoded/`.
""")

build("35", "empty-log-returns-422-inconsistently",
      [(t("cloud-logs-radioPacketLog-GET", "02"), "radiopacketlog-empty-422"),
       (t("cloud-logs-syslog-DELETE", "01"), "syslog-empty-200")],
"""# Finding 35 — An empty log returns 422 on one endpoint and 200 on its sibling

**Endpoints** `GET /cloud/logs/radioPacketLog` vs `GET /cloud/logs/syslog`
**Type** Inconsistency + questionable status code
**Status** Confirmed; both observed immediately after a successful purge

Two endpoints in the same family, both freshly purged by this same API, disagree
about what an empty log is:

| After `DELETE` | `GET` response |
|---|---|
| `/cloud/logs/syslog` | **200**, 396 bytes, archive with a 346-byte `messages` |
| `/cloud/logs/radioPacketLog` | **422** `{"code":1,"message":"No radio packet logs available"}` |

## Why 422 is the wrong answer

An empty log is a **legitimate, expected state** — especially straight after a
purge this API offers. 422 Unprocessable Entity says the client sent something
wrong; the client sent a valid GET with no parameters.

A caller polling for logs must special-case this message string to tell
"nothing to collect" from a real failure. HTTP 200 with an empty archive — what
`syslog` already does — or 204 No Content would say the same thing unambiguously.

## The two verbs also disagree with each other

On the *same* endpoint, in the *same* empty state:

| Request | Response |
|---|---|
| `GET /cloud/logs/radioPacketLog` | **422** — "no logs available" |
| `DELETE /cloud/logs/radioPacketLog` | **200** — idempotent, no complaint |

So DELETE treats "already empty" as fine, while GET treats it as a client error.

## The message itself is good

`"No radio packet logs available"` is clear and specific. The status code and the
inconsistency with `syslog` are the issues, not the wording.

## Ask

Return 200 with an empty archive (matching `syslog`), or 204. Whichever is
chosen, make the two endpoints agree.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-radiopacketlog-empty-422/` | `rest/cloud-logs-radioPacketLog-GET/02-empty-returns-422/` |
| `evidence-2-syslog-empty-200/` | `rest/cloud-logs-syslog-DELETE/01-purge-SUCCESS/` |

The syslog evidence includes `after-purge-proof/` with the full before and after
responses and both archives decoded.
""")

build("36", "radiopacketlog-lifecycle-works",
      [(t("cloud-logs-radioPacketLog-GET", "03"), "repopulates-after-enable")],
"""# Finding 36 — `radioPacketLog` full lifecycle works — purge, enable, regenerate

**Endpoints** `PUT /cloud/logs` + `GET`/`DELETE /cloud/logs/radioPacketLog`
**Type** Positive finding
**Status** Confirmed end to end

The complete cycle, from the empty state left by a purge:

| Step | Request | Result |
|---|---|---|
| 1 | `GET /cloud/logs/radioPacketLog` | 422 — "No radio packet logs available" |
| 2 | `PUT /cloud/logs {"radioPacketLog":true}` | 200 |
| 3 | `PUT /cloud/start` (begin inventory) | 200 |
| 4 | wait 20 s | — |
| 5 | `PUT /cloud/stop` | 200 |
| 6 | `GET /cloud/logs/radioPacketLog` | **200, 65201 bytes** |

## What this establishes

1. **The 422 means "empty", not "broken"** — it recovers cleanly once there is
   something to return. See [[35-empty-log-returns-422-inconsistently]].

2. **`radioPacketLog` is a real functional switch**, not just a stored boolean.
   It gates actual packet log generation.

3. **The flag's precise meaning is "generate new packet log data"**, not "expose
   the packet log". Evidence: a full 602 KB packet log was retrievable while
   `GET /cloud/logs` reported `radioPacketLog: false` — data captured during an
   earlier period when the flag was on remained readable after it was turned off.

Point 3 is what makes [[32-omitting-radiopacketlog-disables-it]] consequential: a
PUT that changes only a log level silently stops capture, and the effect is
invisible until you notice the log has stopped growing.

## Evidence

`request body/` + `response body/` — `rest/cloud-logs-radioPacketLog-GET/03-repopulates-after-enable/`

Carries the complete 65 KB response including the full base64, plus the decoded
archive.
""")

build("37", "only-two-of-five-logs-are-purgeable",
      [(t("cloud-logs-radioPacketLog-DELETE", "01"), "purge-succeeds")],
"""# Finding 37 — Only two of the five logs are purgeable, and method handling is correct

**Endpoints** the Logs group
**Type** Positive finding — behaviour matches the spec
**Status** Confirmed

The spec documents `DELETE` for only two of the five log paths, and the firmware
matches exactly:

| Path | `DELETE` | Result |
|---|---|---|
| `/cloud/logs/syslog` | documented | ✅ 200, purge confirmed |
| `/cloud/logs/radioPacketLog` | documented | ✅ 200, purge confirmed |
| `/cloud/logs/RcLog` | not documented | 405 `"DELETE not a valid METHOD for Req :/logs/RcLog"` |
| `/cloud/logs/RgWarningLog` | not documented | 405 |
| `/cloud/logs/RgErrorLog` | not documented | 405 |
| `/cloud/logs` | not documented | 405 `"DELETE not a valid METHOD for Req :/logs"` |

Other method and path checks:

| Request | Response |
|---|---|
| `PUT /cloud/logs/syslog` | 405 `"PUT not a valid METHOD for Req :/logs/syslog"` |
| `GET /cloud/logs/nosuchlog` | 404 `"/logs/nosuchlogis not a valid URI.Request not valid"` |

Method handling is correct throughout and the messages name both the method and
the path — good error reporting.

## Both DELETEs are idempotent

A second `DELETE` on an already-purged log returns 200 rather than an error. That
is the right choice for a purge.

## One cosmetic bug

The 404 message is missing a space:

```
"/logs/nosuchlogis not a valid URI.Request not valid"
                ^^ path and "is" run together
```

Same defect seen earlier on `/cloud/connectionStatus`, so it is in shared
URI-error formatting rather than specific to this group.

## Auth is enforced

Without a bearer token, all four representative operations return **401
Unauthorized**:

```
GET    /cloud/logs           → 401
PUT    /cloud/logs           → 401
GET    /cloud/logs/syslog    → 401
DELETE /cloud/logs/syslog    → 401
```

For the DELETEs this is the only guard that exists — see
[[38-purges-work-but-have-no-confirmation-step]].

## Evidence

`request body/` + `response body/` — `rest/cloud-logs-radioPacketLog-DELETE/01-purge-SUCCESS/`
""")

build("38", "purges-work-but-have-no-confirmation-step",
      [(t("cloud-logs-syslog-DELETE", "01"), "syslog-purge-with-before-after-proof"),
       (t("cloud-logs-radioPacketLog-DELETE", "01"), "radiopacketlog-purge")],
"""# Finding 38 — ⚠️ Log purges work correctly, but have no confirmation step

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
""")

build("39", "logs-validation-is-mostly-solid",
      [(t("cloud-logs-PUT", "08"), "nine-validation-probes")],
"""# Finding 39 — `PUT /cloud/logs` validation is mostly solid, with generic messages

**Endpoint** `PUT /cloud/logs`
**Type** Mixed — mostly positive
**Status** Nine probes

Seven of nine bad payloads correctly rejected:

| Probe | Response |
|---|---|
| `{"components":[{"componentName":"nosuch","level":"INFO"}]}` | 422 `Unsupported component provided` |
| `{"components":[{"componentName":"reader_gateway","level":"VERBOSE"}]}` | 422 `Unsupported cloud_agent or reader_gateway level provided` |
| `{"components":[{"componentName":"reader_gateway"}]}` | 422 `Invalid payload fields` |
| `{"components":[{"level":"INFO"}]}` | 422 `Invalid payload fields` |
| `{"components":[{"componentName":"reader_gateway","level":"info"}]}` | 422 — **case-sensitive** |
| `{"radioPacketLog":"true"}` (string) | 422 `Invalid payload fields` |
| `{"components":{…}}` (object, not array) | 422 `Invalid payload fields` |

Type checking works on both fields, the required pair matches the schema, and
level matching is case-sensitive (same as `/cloud/timeZone`).

## Two accepted

| Probe | Response | Note |
|---|---|---|
| `{"components":[]}` | 200 | Reasonable — a no-op on components |
| `{}` | 200 | **Resets `radioPacketLog`** — see [[32-omitting-radiopacketlog-disables-it]] |

`{}` arguably should be rejected. Compare `PUT /cloud/displayConfig`, which
returns `"payload must be a non-empty JSON object"` for the same input.

## The weakness: generic messages

Three distinct problems all return `"Invalid payload fields"` without naming the
field:

- missing `level`
- missing `componentName`
- wrong type on `radioPacketLog` or `components`

The endpoint is **inconsistent with itself** — it produces a precise, enumerated
message for a bad `radio_control` level ([[33-log-level-enum-is-per-component]])
and a generic one for everything else. And the level error names
`"cloud_agent or reader_gateway"` together, which is further evidence they are
one component internally ([[31-component-names-silently-redirected]]).

## Ask

Name the offending field in `Invalid payload fields`, and reject `{}`.

## Evidence

`request body/` + `response body/` — `rest/cloud-logs-PUT/08-validation-probes/`
""")

print("logs findings written")
