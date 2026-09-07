# Finding 37 — `radioPacketLog` gates generation, not retrieval — lifecycle verified

**Endpoint** `PUT /cloud/logs` → `radioPacketLog`, and `GET /cloud/logs/radioPacketLog`
**Type** ✅ Positive finding — behaviour clarified
**Status** Full lifecycle confirmed end to end

The flag's meaning is specifically **"generate new packet log data"**, not
"expose the packet log".

## Evidence 1 — content readable while the flag is off

`GET /cloud/logs/radioPacketLog` returned **602 KB** of archived packet log while
`GET /cloud/logs` reported `radioPacketLog: false`.

So the flag does not gate retrieval. Data from an earlier period when it was on
stays readable after it is turned off — useful to know: turning the flag off does
not hide existing evidence.

## Evidence 2 — the full cycle works

From the empty/422 state left by the `DELETE`:

```
GET  /cloud/logs/radioPacketLog          → 422 "No radio packet logs available"
PUT  /cloud/logs {"radioPacketLog":true} → 200
PUT  /cloud/start                        → 200
     … 20 s inventory …
PUT  /cloud/stop                         → 200
GET  /cloud/logs/radioPacketLog          → 200, 65,201 bytes
```

Purge → empty → enable → generate → retrieve. All five steps confirmed.

## Two things this establishes

1. **The 422 means "empty", not "broken"** — which is what makes
   [[36-empty-log-status-code-inconsistent]] a status-code complaint rather than
   a functional defect.
2. **The flag is a real functional switch**, not merely a stored boolean. It
   controls whether the radio actually writes packet log data.

## Which makes finding 34 consequential

Because the flag genuinely controls generation,
[[34-omitting-radiopacketlog-disables-it]] is not a cosmetic issue: a `PUT` that
changes only a log level silently **stops packet log generation**. Combined with
the fact that existing content remains readable, the failure is easy to miss —
`GET` keeps returning the old data, so nothing looks wrong until the gap in
coverage matters.

## Practical note

`radioPacketLog` is also the one purgeable log that is **recoverable**. `syslog`
is not — see [[38-purges-work-but-have-no-confirmation-step]].

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-repopulates-after-enable/` | `rest/cloud-logs-radioPacketLog-GET/03-repopulates-after-enable/` |
| `evidence-2-content-readable-while-flag-false/` | `rest/cloud-logs-radioPacketLog-GET/01-retrieve-SUCCESS/` |
