# Finding 18 — `GPIO-LED` does drive hardware — an earlier conclusion corrected

**Endpoint** `PUT /cloud/config` (`GPIO-LED`)
**Type** Positive finding + **withdrawn** defect report
**Status** Confirmed across tests 15–19

## The claim that was wrong

An earlier version of the report asked, as its highest-priority question, whether
the GPIO-LED engine was functional at all — based on test 08, in which a
`RADIO_START` action left its pin LOW while the radio was confirmed active.

**That conclusion was wrong.** Tests 15–19 confirm GPIO-LED actions do drive
hardware.

## What test 15 showed

One request carrying both `GPIO-LED` and `READER-GATEWAY`. Both halves applied,
confirmed via `GET /cloud/config`, and both halves proven at runtime:

- **Data half** — real tag reads captured on `fxr60-lab/tevents`, e.g. `idHex
  e2806894000040017790ac71`, antenna 1, channel 926.25, peakRssi −49
- **GPIO half** — GPO pins moved on `RADIO_START` / `RADIO_STOP`, across repeated
  start/stop cycles

Tests 16–19 then extended this to conditions
([[15-conditions-are-genuinely-enforced]]) and cloud events
([[16-cloud-connect-fires-on-failed-attempt]]).

## Why the wrong conclusion was reached

Test 08 is a single test, and it was generalised into a claim about the whole
subsystem. Two suspicions raised at the time — that `READER-GATEWAY`'s presence
was interfering, and that pin 1 specifically was faulty — were later isolated and
**both cleared**.

Test 08's non-firing is still unexplained, but it is an **isolated case, not the
general behaviour**. Its folder is marked `INCONCLUSIVE` rather than `FAILED`.

A second contributor: GPO state persists across configuration changes, and early
observations did not always reset the pins and read back to confirm. See
[[10-gpo-is-the-model-endpoint]].

## The lesson

One negative result is not a subsystem verdict. Before reporting a capability as
broken, test it more than one way — especially where the observation depends on
persistent state that an earlier test could have left behind.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-radio-events-move-pins/` | `rest/cloud-config-PUT/15-combined-mqtt-and-gpio-led-SUCCESS/` |
| `evidence-2-earlier-inconclusive-test/` | `rest/cloud-config-PUT/08-gpio-led-complete-reference-INCONCLUSIVE/` |
