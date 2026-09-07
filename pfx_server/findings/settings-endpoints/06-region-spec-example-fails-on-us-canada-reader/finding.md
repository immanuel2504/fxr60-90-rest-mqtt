# Finding 06 — The spec's `region` example does not work on a US/Canada reader

**Endpoint** `PUT /cloud/region`
**Type** Documentation defect (likely SKU-specific example)
**Status** Confirmed

The spec's example, sent verbatim:

```json
{"country": "Canada", "standardname": "CANADA_FCC_15"}
→ 422 {"code":3,"message":"CS:'regionStandardRsp' failed,Reason: RADIO REGION NOT AVAILABLE"}
```

Neither value exists on this reader:

| | This reader reports |
|---|---|
| `GET /cloud/supportedRegionList` | `["United States/Canada"]` — one entry only |
| `GET /cloud/supportedStandardList` | `US_FCC_15`, `US_FCC_A`, `US_FCC_B`, `US_FCC_C`, `US_FCC_CUSTOM` |

There is no bare `"Canada"` and no `"CANADA_FCC_15"`.

## Assessment

Most likely a **SKU difference rather than a defect** — a Canada-specific unit may
well report those values. But the documented example fails on a US/Canada reader,
and the spec gives no indication that its example is region-specific.

## What does work

Switching between the standards this reader actually supports works, repeatedly,
without a reboot — and is fully verifiable:

| | `regulatoryStandard` | `region` | channels |
|---|---|---|---|
| before | `US_FCC_15` | `FCC_Generic` | 50 |
| after `US_FCC_A` | `US_FCC_A` | `FCC_A` | 50 |
| after `US_FCC_C` | `US_FCC_C` | `FCC_C` | 50 |
| restored | `US_FCC_15` | `FCC_Generic` | 50 |

`channelData` updates to the new standard's frequencies each time.

## Ask

Either use a universally valid example, or state that valid values are per-device
and must be read from `supportedRegionList` / `supportedStandardList` first.

## Note on safe testing

`region` governs radio regulatory compliance. Every test here stayed inside the
reader's supported list and restored `US_FCC_15` with all 50 original channels
afterwards.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-spec-example-rejected/` | `rest/cloud-region-PUT/07-spec-example-canada-REJECTED/` |
| `evidence-2-supported-standard-works/` | `rest/cloud-region-PUT/01-us-fcc-a-SUCCESS/` |
