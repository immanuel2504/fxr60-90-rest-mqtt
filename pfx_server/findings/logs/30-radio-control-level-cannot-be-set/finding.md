# Finding 30 — 🐛 `radio_control`'s log level cannot be set

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
