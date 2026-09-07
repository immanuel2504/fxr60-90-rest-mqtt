# Finding 34 — Omitting `radioPacketLog` silently turns it off

**Endpoint** `PUT /cloud/logs`
**Type** Undocumented mixed update semantics
**Status** Confirmed, including via the empty body

```
before  {"components":[...rg=TRACE...], "radioPacketLog":true}
PUT     {"components":[{"componentName":"reader_gateway","level":"INFO"}]}   → 200
after   {"components":[...rg=INFO...],  "radioPacketLog":false}   ← reset
```

**Changing a log level silently disables the radio packet log.** The empty body
does the same, and that is its *only* effect:

```
before  {"components":[...rg=TRACE...], "radioPacketLog":true}
PUT     {}                                                       → 200
after   {"components":[...rg=TRACE...], "radioPacketLog":false}   ← reset
```

## The semantics are mixed, per field

| Field | Omitted from request |
|---|---|
| `components` | **merged** — existing levels survive |
| `radioPacketLog` | **reset to default** — reverts to `false` |

A caller cannot reason about this endpoint as either "merge" or "replace" — it is
one of each, and neither is documented.

## Why it matters

The flag is a **real functional switch**, not a stored boolean — it gates packet
log generation ([[37-radiopacketlog-gates-generation-not-retrieval]]). So a PUT
that changes only a log level stops packet logging, silently. Anyone raising a
log level to investigate a problem would disable the packet log they may also
need, at exactly the wrong moment.

## Practical guidance

Always send `radioPacketLog` explicitly on every `PUT /cloud/logs`, even when
only changing a level. When sent, it works correctly and toggles both ways,
verified by read-back.

## The wider pattern

Three endpoints on this API, three different update semantics, none documented:

| Endpoint | Partial update |
|---|---|
| `PUT /cloud/displayConfig` | merges every field |
| `PUT /cloud/config` → `GPIO-LED` | replaces wholesale |
| `PUT /cloud/logs` | **merges `components`, resets `radioPacketLog`** |

## Ask

Should omitting the field disable packet logging? And should `{}` be accepted at
all — compare `PUT /cloud/displayConfig`, which returns `payload must be a
non-empty JSON object`.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-level-change-resets-flag/` | `rest/cloud-logs-PUT/07-omitting-radiopacketlog-resets-it-to-false/` |
| `evidence-2-flag-toggles-correctly-when-sent/` | `rest/cloud-logs-PUT/06-radiopacketlog-toggle-SUCCESS/` |

## Related

[[08-displayconfig-merges-partial-updates]] · [[13-gpio-led-replaces-wholesale]]
