# Finding 32 — The level enum is per-component; the schema declares one shared enum

**Endpoint** `PUT /cloud/logs`
**Type** Spec-vs-firmware mismatch
**Status** Confirmed — all 8 levels sent to both components

The schema declares a **single** `level` enum of 8 values, applying to every
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

So `reader_gateway` supports **8** levels and `radio_control` supports **4**.

The schema expresses one shared enum and cannot represent this. A client sending
a **documented** level to a **documented** component receives a 422 it had no way
to predict.

Note the `radio_control` 200s do not mean the level applied — see
[[30-radio-control-level-cannot-be-set]]. This finding is only about which values
pass validation.

## Credit where due

This is one of the **best error messages on the API**. It names the offending
value *and* enumerates the acceptable ones — which is precisely how the real enum
was discovered, since the spec gives no hint of it.

Compare the generic message returned for a bad `reader_gateway` level, which
lists nothing:

```json
{"code":1,"message":"Unsupported cloud_agent or reader_gateway level provided"}
```

The endpoint is inconsistent with itself: precise and enumerated for one
component, generic for the other.

## Ask

Document the per-component level sets, or accept all 8 for both. And apply the
`radio_control` message's style — name the field, list the valid values — to the
`reader_gateway` error too.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-radio-control-rejects-four-levels/` | `rest/cloud-logs-PUT/04-radio-control-rejects-four-documented-levels/` |
| `evidence-2-reader-gateway-accepts-all-eight/` | `rest/cloud-logs-PUT/05-all-eight-levels-on-reader-gateway-SUCCESS/` |
