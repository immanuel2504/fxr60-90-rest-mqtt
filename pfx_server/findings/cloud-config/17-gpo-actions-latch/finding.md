# Finding 17 — GPO actions latch; the cloud pin pair cannot show current state

**Endpoint** `PUT /cloud/config` (`GPIO-LED`)
**Type** Design limitation, undocumented
**Status** Confirmed

`CLOUD_CONNECT` and `CLOUD_DISCONNECT` each drive their own pin HIGH, and neither
clears the other. After a normal endpoint change — which emits
`CLOUD_DISCONNECT` then `CLOUD_CONNECT` — **both pins are HIGH** while the reader
is connected.

```
baseline     {"1":"LOW", "2":"LOW"}
after apply  {"1":"HIGH","2":"HIGH"}     ← and /cloud/status says "connected"
at t+20s     {"1":"HIGH","2":"HIGH"}     ← stable, not transient
```

The pins are **latched event markers, not a state indicator**.

## Making them show state

Each event must also clear the other's pin:

```json
"CLOUD_CONNECT":    [{"type":"GPO","pin":1,"state":"HIGH"},
                     {"type":"GPO","pin":2,"state":"LOW"}]
"CLOUD_DISCONNECT": [{"type":"GPO","pin":2,"state":"HIGH"},
                     {"type":"GPO","pin":1,"state":"LOW"}]
```

## LEDs do not have this problem

LED 2 is a single resource that both events set to a different colour, so the last
event wins and the LED **does** track current state. Only the GPO pins latch.

## Important caveat

This pattern cannot rescue [[16-cloud-connect-fires-on-failed-attempt]]. A
spuriously-firing `CLOUD_CONNECT` would clear the disconnect pin too, so the
indicator would still be wrong on a reader retrying a dead endpoint.

## Ask

Are GPO actions intended to latch? Is driving both pins from both events the
intended pattern, or is there a supported way for one event to clear another's pin?

## Evidence

`request body/` + `response body/` — `rest/cloud-config-PUT/18-combined-aws-and-cloud-events-SUCCESS/`
