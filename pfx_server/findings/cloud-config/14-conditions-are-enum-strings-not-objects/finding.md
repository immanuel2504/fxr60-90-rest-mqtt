# Finding 14 — Conditions are enum strings, not objects

**Endpoint** `PUT /cloud/config` (`GPIO-LED` → `actionConditions`)
**Type** Schema clarification
**Status** Confirmed, stored verbatim

`conditionsArray.v1` defines conditions as plain **enum strings**, with only four
possible values:

```
IS_CLOUD_CONNECTED    ~IS_CLOUD_CONNECTED
IS_RADIO_ONGOING      ~IS_RADIO_ONGOING
```

The `~` prefix negates. There is no GPI-state condition, no comparison operator,
and no way to test a pin.

## Both container forms work

Verified stored exactly as sent via `GET /cloud/config`:

```json
"TAG_READ":         { "conditions": ["IS_CLOUD_CONNECTED", "IS_RADIO_ONGOING"] }
"CLOUD_DISCONNECT": { "conditions": {"operator":"or","operands":["~IS_CLOUD_CONNECTED"]} }
```

So `actionConditions` accepts both the **bare array** (implicit `and`) and the
explicit **`{operator, operands}`** object.

## A wrong inference, caught before sending

An earlier draft used:

```json
{"type":"GPI","pin":1,"state":"HIGH"}
```

inferring an object shape from other condition schemas elsewhere in the spec.
That was **wrong** — checking `conditionsArray.v1` showed conditions are plain
enum strings from a four-value set. Caught by reading the schema rather than
extrapolating from a similar-looking one.

## Related

[[15-conditions-are-genuinely-enforced]] — conditions are not merely stored; they
gate actions at runtime.

## Evidence

`request body/` + `response body/` — `rest/cloud-config-PUT/07-gpio-led-conditions-SUCCESS/`
