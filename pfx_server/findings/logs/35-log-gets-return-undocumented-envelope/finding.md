# Finding 35 — All four log retrievals return an undocumented envelope

**Endpoints** `GET /cloud/logs/{syslog,RcLog,RgWarningLog,RgErrorLog,radioPacketLog}`
**Type** Missing response schema + no filtering
**Status** Confirmed and decoded for all five

The spec defines **no response schema** for any log retrieval — only a path, an
`operationId` and a one-line summary. All of them return the same shape:

```json
{"binary": "<base64 of a gzipped tar>", "filename": "<name>.tar.gz"}
```

**Verified for each**: the base64 decodes to valid gzip (magic bytes `1f8b`) and
opens as a tar archive containing real log content.

| Operation | Response | `filename` | Archive contents |
|---|---|---|---|
| `syslog` | 13,364 B | `syslog.tar.gz` | 1 member — `messages`, 72 KB |
| `RcLog` | 621,823 B | `rcLog.tar.gz` | 3 members — live + 2 rotated, ~5 MB each |
| `RgWarningLog` | 426 B | `rgWarningLog.tar.gz` | 6 members, 26 B each — **header only** |
| `RgErrorLog` | 3,856 B | `rgErrorLog.tar.gz` | 6 members, 184–8,886 B — real content |
| `radioPacketLog` | 602,317 B | `radioPktLog.tar.gz` | 4 members, ~1 MiB each |

## Extracting one

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

## No filtering, and one very large response

**No operation takes any parameter** — no time range, no severity filter, no line
count, no paging. Retrieval is all-or-nothing, and `RcLog` returns roughly
**10.5 MB uncompressed** in a single response.

Rotation sizes observed: `RcLog` at ~5 MB per file, `radioPacketLog` at ~1 MiB
(1048576) per file. The `radioPacketLog` numbering is non-sequential
(6, 7, 8, 11), suggesting a ring of numbered slots rather than a monotonic
sequence.

## Practical note on the `Rg*` logs

Both are **one file per gateway restart**, named
`<warning|error>-<ISO timestamp>-0.txt`. The six timestamps observed — 14:55,
14:58, 15:00, 15:08, 15:20, 16:03 — line up with the reader-gateway restarts
caused by the endpoint reconfiguration testing in `cloud-config-PUT/` and
`cloud-cloudConfig-PUT/`.

`RgWarningLog`'s members are 26 bytes each and contain **only a date line** — the
files exist but hold no warnings. `RgErrorLog`'s have real content, and its
largest member (8,886 B, timestamped 16:03:24) covers the session in which the
unreachable-broker test ran. That makes `RgErrorLog` the most useful of the four
for diagnosing the reader side of the error-255 connection failures in
[[16-cloud-connect-fires-on-failed-attempt]].

## Ask

1. Document the response schema.
2. Is filtering planned — time range, severity, line count, paging? A 10.5 MB
   all-or-nothing retrieval is awkward to poll.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-syslog/` | `rest/cloud-logs-syslog-GET/01-retrieve-SUCCESS/` |
| `evidence-2-rclog-largest/` | `rest/cloud-logs-RcLog-GET/01-retrieve-SUCCESS/` |
| `evidence-3-rgerrorlog/` | `rest/cloud-logs-RgErrorLog-GET/01-retrieve-SUCCESS/` |

The `binary` field is truncated in each `response.json`, with the original length
recorded; `verification.txt` lists the decoded archive members and sizes.
