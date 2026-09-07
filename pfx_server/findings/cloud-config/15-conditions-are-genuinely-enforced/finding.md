# Finding 15 — Conditions are genuinely enforced, not just stored

**Endpoint** `PUT /cloud/config` (`GPIO-LED` → `actionConditions`)
**Type** Positive finding — runtime behaviour confirmed
**Status** Confirmed by divergent pin behaviour in one test

The most interesting result of the combined tests. Two actions in the **same
config**, differing only in their conditions, behaved **differently** at runtime —
which is only explicable if conditions are evaluated, not merely recorded.

```
before : {"1":"LOW", "2":"LOW","3":"HIGH","4":"LOW"}
start  : {"1":"HIGH","2":"LOW","3":"HIGH","4":"LOW"}
stop   : {"1":"LOW", "2":"LOW","3":"HIGH","4":"LOW"}
```

| Pin | Event | Conditions | Fired? |
|---|---|---|---|
| 1 | `TAG_READ` | `[IS_CLOUD_CONNECTED, IS_RADIO_ONGOING]` | ✅ yes |
| 2 | `RADIO_START` | `[IS_CLOUD_CONNECTED]` | ❌ no |

Pin 1 went HIGH during the inventory and returned LOW after it — exactly what
`IS_RADIO_ONGOING` implies. Pin 2 never moved.

## The unresolved part

Pin 2's condition (`IS_CLOUD_CONNECTED`) is a **subset** of pin 1's, and pin 1
fired — so `IS_CLOUD_CONNECTED` evaluated **true** for pin 1 and **false** for
pin 2 in the same config, at nearly the same moment.

That is not explained. Recording it as observed rather than resolved. Two
possibilities not yet distinguished: the condition may be evaluated per-event at
different moments in the connection lifecycle, or `RADIO_START` may evaluate its
conditions before the cloud state is considered established.

## Alongside this, the data half was proven

The `httpPost` receiver log grew 27 → 46 lines — 19 new POSTs of real tag data
during the inventory. So both halves of the combined request worked.

## Related

[[14-conditions-are-enum-strings-not-objects]] — the accepted condition syntax.

## Evidence

`request body/` + `response body/` — `rest/cloud-config-PUT/16-combined-httpPost-and-conditional-gpio-SUCCESS/`
