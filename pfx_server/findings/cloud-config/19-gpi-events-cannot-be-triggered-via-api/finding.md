# Finding 19 — GPI events cannot be triggered through the API

**Endpoint** `PUT /cloud/config` (`GPIO-LED` → `GPI_*` events)
**Type** Test-coverage gap
**Status** Confirmed — configuration accepted, behaviour unverifiable

The four GPI events — `GPI_1_H`, `GPI_1_L`, `GPI_2_H`, `GPI_2_L` — are accepted
and stored correctly. But **nothing in the API can trigger a GPI transition**.

| | |
|---|---|
| GPO pins | ✅ writable via `PUT /cloud/gpo` |
| GPI pins | ❌ readable via `GET /cloud/gpi`, but **not** writable |

GPI means *general purpose **input***, so this is consistent — an input reflects
external wiring. The consequence is that `GPI_*` event configuration cannot be
validated without someone physically closing a contact at the reader.

## What this means for the test coverage

Of the nine GPIO-LED events, seven are verifiable remotely:

| Event | Triggerable via API? |
|---|---|
| `RADIO_START` / `RADIO_STOP` | ✅ `PUT /cloud/start` / `/cloud/stop` |
| `TAG_READ` | ✅ run an inventory with tags present |
| `CLOUD_CONNECT` / `CLOUD_DISCONNECT` | ✅ apply/break an endpoint config |
| `GPI_1_H` / `GPI_1_L` / `GPI_2_H` / `GPI_2_L` | ❌ **physical access required** |

## Ask

Is there any way to trigger a GPI transition through the API for test purposes —
a simulate/inject call? Without one, a quarter of the GPIO-LED event surface
cannot be validated by an integrator before deployment.

## Evidence

`request body/` + `response body/` — `rest/cloud-config-PUT/06-gpio-led-gpi-events-SUCCESS/`
