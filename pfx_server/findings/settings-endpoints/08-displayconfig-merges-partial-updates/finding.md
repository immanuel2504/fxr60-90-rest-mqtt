# Finding 08 — `displayConfig` merges partial updates — the opposite of `/cloud/config`

**Endpoint** `PUT /cloud/displayConfig`
**Type** Undocumented update semantics
**Status** Confirmed

Sending two fields preserves the other five:

```
before  enable:true  onscreenKb:false  layout:French  orientation:portrait
        resolution:1280x720  timeout:45  url:https://10.117.229.18/

PUT     {"enable":true,"orientation":"landscape-flipped"}   → 200

after   enable:true  onscreenKb:false  layout:French  orientation:landscape-flipped
        resolution:1280x720  timeout:45  url:https://10.117.229.18/
```

Only `orientation` changed. This endpoint **merges**.

## The inconsistency

That is the **opposite** of the `GPIO-LED` object in `PUT /cloud/config`, which
replaces wholesale and silently discards any event not named in the request.

| Endpoint | Partial update behaviour |
|---|---|
| `PUT /cloud/displayConfig` | **merges** — omitted fields preserved |
| `PUT /cloud/config` → `GPIO-LED` | **replaces** — omitted events discarded |

Two endpoints on the same API with opposite semantics, neither documented.

## A correction this test forced

An earlier reading of test 03 concluded "partial updates are not supported",
because a single-field PUT was rejected:

```json
PUT {"orientation":"landscape-flipped"}
→ 422 {"code":3,"message":"CS:'setDisplayConfig' failed, Reason: Missing required parameters"}
```

**That was wrong.** The real cause is the missing `enable` field — the one
mandatory field on this endpoint (see
[[03-required-fields-undeclared-in-both-directions]]). Add `enable` and the same
partial update succeeds. The rejection changed nothing: state before and after
was identical.

## Ask

State the update semantics per endpoint in the docs.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-partial-update-merges/` | `rest/cloud-displayConfig-PUT/05-partial-update-merges-SUCCESS/` |
| `evidence-2-single-field-without-enable-rejected/` | `rest/cloud-displayConfig-PUT/03-partial-no-enable-REJECTED/` |

## Related

[[03-required-fields-undeclared-in-both-directions]] · [[13-gpio-led-replaces-wholesale]]
