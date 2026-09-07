# Finding 10 — `/cloud/gpo` is the model the other endpoints should follow

**Endpoint** `PUT /cloud/gpo`
**Type** Positive finding — reference behaviour
**Status** Confirmed across 9 tests

The only endpoint of the six with a **genuine read-back of what was written**, and
strict throughout.

| Probe | Response |
|---|---|
| `{"port":3,"state":true}` | 200 — pin 3 LOW→HIGH, confirmed, no other pin touched |
| `{"port":0,…}` / `{"port":5,…}` | 422 `Invalid GPO pin` |
| `{"port":1}` / `{"state":true}` | 422 `Required Fields not provided.Expected port/state` |
| `{"port":1,"state":"true"}` | 422 `state (expected boolean)` |
| `{"port":"1","state":true}` | 422 `port (expected positive number)` |

What it gets right, and the others do not:

- **Writes are verifiable** — `GET /cloud/gpo` reports actual pin state
- **Bounds enforced**, matching the schema's documented 1–4
- **Types checked on both fields**, with no silent string→boolean coercion
- **Every message names the offending field** and the expected type
- **Required fields match the schema** — contrast
  [[03-required-fields-undeclared-in-both-directions]]

All four pins are individually writable in both directions. There is no bulk
form — one pin per request, so setting four pins is four PUTs.

## Why this endpoint mattered beyond itself

`PUT /cloud/gpo` is what made the GPIO-LED findings possible. When a GPIO-LED
event failed to move a pin, this endpoint proved the pin itself was fine —
separating "the hardware is broken" from "the event did not fire".

It is also the reset used to establish a clean baseline before each GPIO
observation. **GPO state persists across configuration changes**, so the reset
must always be *read back* to confirm, or leftover state from an earlier test
reads as a fresh event. Skipping that read-back invalidated one earlier run of
cloud-config test 18 — see [[16-cloud-connect-fires-on-failed-attempt]].

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-write-verified-by-readback/` | `rest/cloud-gpo-PUT/01-spec-example-port3-high-SUCCESS/` |
| `evidence-2-type-checked-with-named-field/` | `rest/cloud-gpo-PUT/08-state-wrong-type-REJECTED/` |
