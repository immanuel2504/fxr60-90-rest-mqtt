# Finding 31 — 🐛 Three of the five documented `componentName` values are silently redirected

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
