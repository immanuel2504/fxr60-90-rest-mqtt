# FXR60 Logs endpoints — test report

All nine operations in the spec's **Logs** group, tested against a live reader.
Every request and response in this report is verbatim from a real call; the
numbered folders beside each endpoint hold them individually.

## Scope

| | |
|---|---|
| Reader | `10.233.48.36`, reader app 5.0.7 |
| Date | 2026-09-05 |
| Operations | 9 — all of them |
| Tests | 18 |
| Auth | `GET /cloud/localRestLogin` with `admin:Zebra@123`; tokens not stored |

All five logs were **captured to `/tmp/logbase/` before any DELETE was issued**,
and the log configuration was restored byte-identically afterwards.

---

## Results

| Operation | Folder | Result |
|---|---|---|
| `GET /cloud/logs` | [`cloud-logs-GET/`](cloud-logs-GET/) | ✅ Working |
| `PUT /cloud/logs` | [`cloud-logs-PUT/`](cloud-logs-PUT/) | 🐛 **Two defects** — see findings 1–3 |
| `GET /cloud/logs/syslog` | [`cloud-logs-syslog-GET/`](cloud-logs-syslog-GET/) | ✅ Working, archive verified |
| `DELETE /cloud/logs/syslog` | [`cloud-logs-syslog-DELETE/`](cloud-logs-syslog-DELETE/) | ✅ Working, purge confirmed |
| `GET /cloud/logs/RcLog` | [`cloud-logs-RcLog-GET/`](cloud-logs-RcLog-GET/) | ✅ Working, archive verified |
| `GET /cloud/logs/RgWarningLog` | [`cloud-logs-RgWarningLog-GET/`](cloud-logs-RgWarningLog-GET/) | ✅ Working, archive verified |
| `GET /cloud/logs/RgErrorLog` | [`cloud-logs-RgErrorLog-GET/`](cloud-logs-RgErrorLog-GET/) | ✅ Working, archive verified |
| `GET /cloud/logs/radioPacketLog` | [`cloud-logs-radioPacketLog-GET/`](cloud-logs-radioPacketLog-GET/) | ⚠️ Working — **422 when empty** |
| `DELETE /cloud/logs/radioPacketLog` | [`cloud-logs-radioPacketLog-DELETE/`](cloud-logs-radioPacketLog-DELETE/) | ✅ Working, purge confirmed |

**All nine operations function.** The four log retrievals and both purges work
correctly and were verified by decoding the archives and comparing sizes. The
problems are concentrated in `PUT /cloud/logs`, where **three of five documented
`componentName` values are silently redirected** and one component's level cannot
be set at all.

---

## Findings

### 1. 🐛 `radio_control`'s log level cannot be set — HTTP 200, value discarded

The level for `radio_control` never changes, whatever is sent:

```
PUT {"components":[{"componentName":"radio_control","level":"ERROR"}]}    → 200,  read back INFO
PUT {"components":[{"componentName":"radio_control","level":"WARNING"}]}  → 200,  read back INFO
PUT {"components":[{"componentName":"radio_control","level":"DEBUG"}]}    → 200,  read back INFO
```

Also tested with both components in one request:

```
PUT {"components":[{"componentName":"radio_control","level":"DEBUG"},
                   {"componentName":"reader_gateway","level":"ERROR"}]}
→ 200,  read back  rc=INFO  rg=ERROR
```

The `reader_gateway` half applied; the `radio_control` half did not.

**The awkward part is that the value is validated first.** An invalid level for
`radio_control` *is* rejected, with a component-specific error (finding 3) — so
the value demonstrably reaches the `radio_control` validator, passes, and is then
discarded. If the level is fixed, the request should be rejected rather than
accepted.

Not established: whether the level is applied internally and merely mis-reported
by `GET /cloud/logs`. Distinguishing those needs a log-volume comparison at
`ERROR` vs `DEBUG`, which was not run.

### 2. 🐛 Three of five documented `componentName` values are silently redirected

The schema documents five accepted values, with this mapping:

> Supported canonical names are `radio_control` and `cloud_agent`. Supported
> aliases are `RC` for `radio_control` and `RG` for `reader_gateway`.

Each was sent alone with a distinctive level, and the config read back:

| Sent `componentName` | Documented target | Actually written to | |
|---|---|---|---|
| `reader_gateway` | `reader_gateway` | `reader_gateway` | ✅ |
| `RG` | `reader_gateway` | `reader_gateway` | ✅ |
| `radio_control` | `radio_control` | **`reader_gateway`** | 🐛 |
| `RC` | `radio_control` | **`reader_gateway`** | 🐛 |
| `cloud_agent` | `cloud_agent` | **`reader_gateway`** | 🐛 |

All five returned HTTP 200, with nothing to indicate a redirect had occurred.

Two consequences:

- **`radio_control` and `RC` do not address `radio_control`.** Their level lands
  on `reader_gateway`. Either the documented alias mapping is wrong or the
  implementation is.
- **`cloud_agent` is not a separate component here.** It also writes to
  `reader_gateway` and never appears in any `GET` response. Either it *is*
  `reader_gateway` under another name — in which case the schema's description is
  misleading, since it presents them as distinct — or the component does not
  exist on this firmware.

`GET /cloud/logs` only ever reports two components: `radio_control` and
`reader_gateway`.

A supporting hint from the validator: a bad level returns *"Unsupported
**cloud_agent or reader_gateway** level provided"* — naming the two together, as
though they share one implementation.

### 3. The level enum is per-component; the schema declares one shared enum

The schema declares a single `level` enum of 8 values, applying to every
component:

```
OFF  FATAL  ERROR  WARNING  DEBUG  INFO  TRACE  EXTRA
```

The reader disagrees for `radio_control`, and says so explicitly:

```json
{"code":3,"message":"\"set_logs\" Failed to apply. Description: unsuccessful rc response: Failure: TRACE is not an acceptable value for level (acceptable values are: ERROR, WARNING, INFO, DEBUG)"}
```

All eight levels were sent to each component:

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

So `reader_gateway` supports **8** levels and `radio_control` supports **4**. The
schema cannot express this, and a client sending a documented level to a
documented component gets a 422 it had no way to predict.

**Credit where due:** this error message is one of the best on the API — it names
the offending value *and* lists the acceptable ones, which is how the real enum
was discovered. Compare the generic *"Unsupported cloud_agent or reader_gateway
level provided"* returned for a bad `reader_gateway` level, which lists nothing.

### 4. The spec's own `PUT` example is half-ignored

Sent verbatim, it returns HTTP 200 and applies **one of its three requests**:

```json
{"components":[{"componentName":"radio_control","level":"DEBUG"},
               {"componentName":"cloud_agent","level":"DEBUG"}],
 "radioPacketLog":true}
```

| Requested | Outcome |
|---|---|
| `radioPacketLog: true` | ✅ applied |
| `cloud_agent: DEBUG` | ⚠️ landed on `reader_gateway` (finding 2) |
| `radio_control: DEBUG` | 🐛 ignored — still `INFO` (finding 1) |

The documented example is the most likely thing an integrator will copy, so both
defects above are hit on first contact.

### 5. Omitting `radioPacketLog` silently turns it off

```
before  {"components":[...rg=TRACE...], "radioPacketLog":true}
PUT     {"components":[{"componentName":"reader_gateway","level":"INFO"}]}   → 200
after   {"components":[...rg=INFO...],  "radioPacketLog":false}   ← reset
```

**Changing a log level silently disables the radio packet log.** An empty body
does the same:

```
PUT {}  → 200,  and radioPacketLog goes true → false
```

So the merge semantics are **mixed, per field**:

| Field | Omitted from request |
|---|---|
| `components` | **merged** — existing levels survive |
| `radioPacketLog` | **reset to default** — reverts to `false` |

A caller cannot reason about this endpoint as either "merge" or "replace" — it is
one of each, and neither is documented.

**Practical guidance:** always send `radioPacketLog` explicitly on every
`PUT /cloud/logs`, even when only changing a level.

This matters because the flag is a real functional switch, not a stored boolean —
see finding 8. Three endpoints on this API now show three different update
semantics:

| Endpoint | Partial update |
|---|---|
| `PUT /cloud/displayConfig` | merges every field |
| `PUT /cloud/config` → `GPIO-LED` | replaces wholesale |
| `PUT /cloud/logs` | **merges `components`, resets `radioPacketLog`** |

### 6. All four log GETs return an undocumented envelope

The spec defines **no response schema** for any of the four retrievals — only a
path, an `operationId` and a summary. All four return the same shape:

```json
{"binary": "<base64 of a gzipped tar>", "filename": "<name>.tar.gz"}
```

Verified for each: the base64 decodes to valid gzip (magic `1f8b`) and opens as a
tar archive with real log content.

| Operation | Response | `filename` | Archive contents |
|---|---|---|---|
| `syslog` | 13,364 B | `syslog.tar.gz` | 1 member — `messages`, 72 KB |
| `RcLog` | 621,823 B | `rcLog.tar.gz` | 3 members — live + 2 rotated, ~5 MB each |
| `RgWarningLog` | 426 B | `rgWarningLog.tar.gz` | 6 members, 26 B each — **header only** |
| `RgErrorLog` | 3,856 B | `rgErrorLog.tar.gz` | 6 members, 184–8,886 B — real content |
| `radioPacketLog` | 602,317 B | `radioPktLog.tar.gz` | 4 members, ~1 MiB each |

Extracting one:

```bash
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://10.233.48.36/cloud/logs/syslog \
| python3 -c "
import sys,json,base64
d=json.load(sys.stdin)
open(d['filename'],'wb').write(base64.b64decode(d['binary']))
print('wrote', d['filename'])"
tar tzf syslog.tar.gz
```

Two observations worth documenting:

- **`RcLog` is large** — ~10.5 MB uncompressed in a single response. There are
  **no parameters** on any of these operations: no time range, no severity
  filter, no line count, no paging. Retrieval is all-or-nothing.
- **The `Rg*` logs are one file per gateway restart**, named
  `<warning|error>-<ISO timestamp>-0.txt`. The six timestamps observed (14:55,
  14:58, 15:00, 15:08, 15:20, 16:03) line up with the reader-gateway restarts
  caused by the endpoint reconfiguration testing in `cloud-config-PUT/` and
  `cloud-cloudConfig-PUT/`. `RgErrorLog` is therefore the most useful of the four
  for diagnosing those connection findings.

### 7. ⚠️ `radioPacketLog` returns 422 when empty; `syslog` returns 200

Two endpoints in the same family, both freshly purged, disagree:

| After its `DELETE` | `GET` result |
|---|---|
| `syslog` | **200**, 396 B — archive with a 346-byte `messages` member |
| `radioPacketLog` | **422** `{"code":1,"message":"No radio packet logs available"}` |

An empty log is a legitimate, expected state — especially straight after a purge
this same API offers. Treating it as a client error means a caller polling for
logs must special-case the message to tell "nothing to collect" from a real
failure. HTTP 200 with an empty archive, or 204 No Content, would say the same
thing unambiguously.

The message itself is clear. It is the status code, and the inconsistency with
`syslog`, that are the issue.

The two verbs also disagree about the same state: `DELETE` on an already-empty
`radioPacketLog` returns **200**, while `GET` on it returns **422**.

### 8. `radioPacketLog` gates generation, not retrieval — full lifecycle verified

The flag's meaning is specifically *"generate new packet log data"*:

- With `radioPacketLog: false`, `GET` still returned **602 KB** of existing
  content. So the flag does not gate retrieval — data from an earlier period when
  it was on stays readable after it is turned off.
- From the empty/422 state, the full cycle works:

```
GET  /cloud/logs/radioPacketLog          → 422 "No radio packet logs available"
PUT  /cloud/logs {"radioPacketLog":true} → 200
PUT  /cloud/start                        → 200
     … 20 s inventory …
PUT  /cloud/stop                         → 200
GET  /cloud/logs/radioPacketLog          → 200, 65,201 bytes
```

This confirms the 422 means "empty", not "broken", and that the flag is a real
functional switch. Which in turn makes finding 5 consequential: a PUT that
changes only a log level silently stops packet log generation.

### 9. Both purges work, are verifiable, and are idempotent

`DELETE /cloud/logs/syslog`, confirmed by decoding rather than by size alone:

```
before   GET → 200, 33,392 B     archive member "messages" = 72,394 B
DELETE   200, empty body
after    GET → 200,    396 B     archive member "messages" =    346 B
```

The remaining 346 bytes are entries generated *by the purge itself*:

```
2026-09-05T17:36:56 FXR609BE34A rsyslogd: [...] rsyslogd was HUPed
```

So the reader truncates the file and signals `rsyslogd` (SIGHUP) to reopen it —
the correct way to rotate a live syslog.

Both purges return **200 on a repeat call**, so they are idempotent. And only the
two documented paths accept `DELETE`; the others correctly return 405:

```
DELETE /cloud/logs/RcLog  → 405 {"message":"DELETE not a valid METHOD for Req :/logs/RcLog"}
DELETE /cloud/logs        → 405 {"message":"DELETE not a valid METHOD for Req :/logs"}
```

**No confirmation step.** These are destructive, irreversible operations with no
dry-run, no confirmation parameter and no backup. One `DELETE` and the diagnostic
history is gone. Auth is the only guard — which does hold: all four operations
tested return **401** without a bearer token.

`syslog` is genuinely irreversible. `radioPacketLog` is recoverable, since
re-enabling the flag and running an inventory regenerates it (finding 8).

### 10. Validation is mostly good, with one gap and one inconsistency

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
| `{}` | ⚠️ **200** — and silently resets `radioPacketLog` (finding 5) |

Required fields and types are enforced correctly, and level matching is
case-sensitive as with `/cloud/timeZone`.

Two points:

- **`{}` returns 200** rather than a "payload required" error. Compare
  `PUT /cloud/displayConfig`, which returns `payload must be a non-empty JSON
  object`.
- **The messages are inconsistent with each other.** The endpoint produces a
  precise, enumerated message for a bad `radio_control` level (finding 3) and a
  generic `Invalid payload fields` — which names no field — for everything else.

An unknown log path returns 404 with a missing space:
`{"message":"/logs/nosuchlogis not a valid URI.Request not valid"}` — the same
cosmetic bug seen on `/connectionStatus`.

---

## Questions for Zebra

1. **`radio_control` log level (highest priority).** Can it be set at all? Every
   accepted level returns HTTP 200 and leaves it at `INFO`. The value is
   validated for this component specifically and then discarded. If the level is
   fixed, please reject the request; if it is settable, please make `GET
   /cloud/logs` report the applied value.

2. **`componentName` mapping.** `radio_control`, `RC` and `cloud_agent` all write
   to `reader_gateway`. Is the documented alias mapping wrong, or the
   implementation? Three of five documented values do not address the component
   they name.

3. **`cloud_agent`.** Does this component exist on FXR60/FXR90? It never appears
   in a `GET` response, it writes to `reader_gateway`, and the validator's error
   text names "cloud_agent or reader_gateway" as one thing.

4. **Per-component level enums.** `reader_gateway` accepts all 8 documented
   levels; `radio_control` accepts 4 (`ERROR`, `WARNING`, `INFO`, `DEBUG`).
   Please document the per-component sets — the schema declares one shared enum
   and cannot express this.

5. **The spec's `PUT` example.** It is accepted with HTTP 200 but only one of its
   three requests takes effect. Please correct it, since it is what integrators
   will copy first.

6. **`radioPacketLog` reset.** Should omitting the field disable packet logging?
   Currently changing a log level, or sending `{}`, silently turns it off. And
   should `{}` be accepted at all?

7. **Empty-log status code.** `GET /cloud/logs/radioPacketLog` returns 422 when
   empty; `GET /cloud/logs/syslog` returns 200 with an empty archive. Could these
   be consistent — ideally 200 or 204, since an empty log is an expected state
   after a purge this API provides? Note `DELETE` and `GET` also disagree about
   the same state (200 vs 422).

8. **Log response schema.** None of the four retrievals documents a response
   schema. All return `{"binary": "<base64 gzip tar>", "filename": "..."}`.
   Please document it.

9. **Log filtering and size.** No operation takes any parameter — no time range,
   severity filter, line count or paging. `RcLog` returns ~10.5 MB uncompressed
   in one response. Is filtering planned? Retrieval is currently all-or-nothing.

10. **Purge safety.** Both `DELETE`s are irreversible with no confirmation
    parameter and no dry-run. Is a confirmation mechanism planned? `syslog` in
    particular cannot be regenerated.

---

## Reader state after testing

| | Pre-test | Post-test |
|---|---|---|
| `radio_control` level | `INFO` | `INFO` ✅ |
| `reader_gateway` level | `INFO` | `INFO` ✅ |
| `radioPacketLog` | `false` | `false` ✅ |

Log **configuration** restored byte-identically.

Log **content** was deliberately purged as part of testing:

| Log | State |
|---|---|
| `syslog` | purged — irreversible; captured to `/tmp/logbase/syslog.out` first |
| `radioPacketLog` | purged, then regenerated to 65 KB by finding 8's test |
| `RcLog`, `RgWarningLog`, `RgErrorLog` | untouched — no `DELETE` exists for these |

All five were captured with `GET` **before** any `DELETE`, into `/tmp/logbase/`.

---

## Folder contents

```
cloud-logs-GET/                       1 test
cloud-logs-PUT/                       8 tests
cloud-logs-syslog-GET/                1 test
cloud-logs-syslog-DELETE/             1 test
cloud-logs-RcLog-GET/                 1 test
cloud-logs-RgWarningLog-GET/          1 test
cloud-logs-RgErrorLog-GET/            1 test
cloud-logs-radioPacketLog-GET/        3 tests
cloud-logs-radioPacketLog-DELETE/     1 test
```

Each numbered folder holds:

| Path | Contents |
|---|---|
| `request body/request.json` | The real request — method, URL, reader, headers, body |
| `response body/response.json` or `.txt` | The response verbatim; 0-byte `.txt` where the reader returned an empty body |
| `response body/http_status.txt` | HTTP status code |
| `response body/verification.txt` | How the result was confirmed, and what it revealed |

The `binary` field in the log-retrieval responses is **truncated** in
`response.json`, with the original length recorded — the full values are 380 B to
622 KB of base64. Each `verification.txt` records the decoded archive's members
and sizes.

A few folders cover a sweep rather than one request —
`02-all-component-names-write-to-reader-gateway`,
`03-radio-control-level-never-changes`,
`05-all-eight-levels-on-reader-gateway-SUCCESS`, `08-validation-probes`. Their
`request.json` records the probe set and `verification.txt` gives each response.

Bearer tokens are not stored; each `request.json` records the command that mints
one.

---

## Related

| File | Contents |
|---|---|
| [`SETTINGS_ENDPOINTS_TEST_REPORT.md`](SETTINGS_ENDPOINTS_TEST_REPORT.md) | The six settings endpoints, 47 tests |
| [`cloud-config-PUT/CONFIG_TEST_REPORT.md`](cloud-config-PUT/CONFIG_TEST_REPORT.md) | `PUT /cloud/config` — GPIO-LED and READER-GATEWAY |
| [`cloud-cloudConfig-PUT/CLOUDCONFIG_TEST_REPORT.md`](cloud-cloudConfig-PUT/CLOUDCONFIG_TEST_REPORT.md) | `PUT /cloud/cloudConfig` — connection types |
| [`../findings/`](../findings/) | Every finding as its own folder with evidence |
