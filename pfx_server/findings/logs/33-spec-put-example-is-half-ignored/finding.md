# Finding 33 — The spec's `PUT /cloud/logs` example is half-ignored

**Endpoint** `PUT /cloud/logs`
**Type** Documentation defect — surfaces two other defects on first contact
**Status** Confirmed

The spec's example, sent verbatim, returns **HTTP 200** and applies **one of its
three requests**:

```json
{"components":[{"componentName":"radio_control","level":"DEBUG"},
               {"componentName":"cloud_agent","level":"DEBUG"}],
 "radioPacketLog":true}
```

```
before: {"components":[{"componentName":"radio_control","level":"INFO"},
                       {"componentName":"reader_gateway","level":"INFO"}],
         "radioPacketLog":false}

after:  {"components":[{"componentName":"radio_control","level":"INFO"},
                       {"componentName":"reader_gateway","level":"DEBUG"}],
         "radioPacketLog":true}
```

| Requested | Outcome |
|---|---|
| `radioPacketLog: true` | ✅ applied |
| `cloud_agent: DEBUG` | ⚠️ landed on `reader_gateway` — [[31-component-names-silently-redirected]] |
| `radio_control: DEBUG` | 🐛 ignored, still `INFO` — [[30-radio-control-level-cannot-be-set]] |

Note `cloud_agent` does not appear in the response at all — the reader only ever
reports `radio_control` and `reader_gateway`.

## Why this one matters on its own

The documented example is the **most likely thing an integrator will copy**. Both
underlying defects are hit on first contact, with a 200 response and no
indication anything was dropped. Someone following the documentation exactly will
conclude both components are at `DEBUG` when neither is.

It is also a useful signal for triage: an example that cannot work as written
suggests the example and the firmware were never checked against each other.

## Ask

Correct the example so it works as written on current firmware.

## Evidence

`request body/` + `response body/` — `rest/cloud-logs-PUT/01-spec-example-PARTIALLY-SILENTLY-IGNORED/`
