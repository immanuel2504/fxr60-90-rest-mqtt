# Finding 16 — 🐛 `CLOUD_CONNECT` fires on a connection *attempt*, not a connection

**Endpoint** `PUT /cloud/config` (`GPIO-LED` → `CLOUD_CONNECT`)
**Severity** High — makes the event unusable as a connectivity indicator
**Status** Reproduced twice, including with **no config change at all**

## Test 18 — the working case

Apply a working AWS endpoint from a verified all-LOW baseline:

| | GPO 1 `CLOUD_CONNECT` | GPO 2 `CLOUD_DISCONNECT` | GPO 3 `RADIO_START` |
|---|---|---|---|
| baseline | LOW | LOW | LOW |
| after apply | **HIGH** | **HIGH** | LOW |

`/cloud/status` confirmed `DATA_AWS_CLOUD_EVENTS` `connected`.

Both cloud pins latching is legitimate here — replacing an endpoint tears the old
connection down and brings the new one up within one PUT, so both events really do
occur. Pin 3 staying LOW is the **negative control**: the pins moved because of
events, not merely because a configuration was applied.

## Test 19 — the defect

Point `data.event` at unreachable `10.255.255.1:1883`, so a connect can never
succeed. Pin 1 is kept as a control: with no broker, it must stay LOW.

| | GPO 1 `CLOUD_CONNECT` | GPO 2 `CLOUD_DISCONNECT` |
|---|---|---|
| baseline | LOW | LOW |
| t+20 s | LOW | **HIGH** ✅ |
| t+40 s | **HIGH** 🐛 | HIGH |

At t+20 s the behaviour is exactly right — and this is the **isolated confirmation
that `CLOUD_DISCONNECT` works**. By t+40 s pin 1 was HIGH too, while the interface
reported:

```json
{"connectionStatus": "disconnected",
 "connectionError": "connection initialization failed with return code (255), retry count (0)"}
```

## Reproduced with the config untouched

The pins were reset to LOW and **no new configuration was sent**. The dead
endpoint stayed active, so the only thing the reader could be doing was retrying:

| | GPO 1 | GPO 2 |
|---|---|---|
| baseline (read back) | LOW | LOW |
| t+20 s | LOW | LOW |
| t+40 s | **HIGH** 🐛 | LOW |
| t+100 s | HIGH | LOW |

This second run rules out every alternative:

- **not** the config-apply — no PUT was sent
- **not** stale pin state — baseline read back as LOW in both runs
- **not** a real connection — status never once reported `connected`
- **not** pin-specific — pin 1 behaves correctly in tests 15–18

The ~40 s onset against a `reconnectDelay`/`reconnectDelayMax` of 2/10 s points at
the event being hooked to the **start of a connection attempt** rather than to a
successful CONNACK.

## Why it matters

`CLOUD_CONNECT` cannot be used as a cloud-connectivity indicator. Wired to a stack
light or PLC input it will show "cloud OK" on a reader that has never connected and
is retrying a dead endpoint — precisely the failure the indicator exists to catch.

## Workaround

Read `GET /cloud/status → interfaceConnectionStatus[].connectionStatus`, which
reported `disconnected` correctly and consistently throughout both runs.

## Method note — why the baseline matters

GPO state **persists** across configuration changes. An earlier run of test 18
reported pin 3 HIGH as well; that observation was discarded because the reset loop
was malformed (missing URL) so the pins were never actually reset, and the token
expired mid-run. Every observation above starts from all four pins driven LOW and
**read back to confirm**. See [[10-gpo-is-the-model-endpoint]].

## Ask

1. Is `CLOUD_CONNECT` specified to fire on a successful connection or on an
   attempt?
2. Should it re-fire on every reconnect attempt?
3. Error 255 is returned here for an unreachable host, and elsewhere for a blocked
   port and for certificate faults — three causes, one message.

## Related

[[17-gpo-actions-latch]] — the second, milder problem visible in test 18.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-unreachable-broker-fires-cloud-connect/` | `rest/cloud-config-PUT/19-force-cloud-disconnect-BUG-FOUND/` |
| `evidence-2-working-aws-both-pins-latch/` | `rest/cloud-config-PUT/18-combined-aws-and-cloud-events-SUCCESS/` |
