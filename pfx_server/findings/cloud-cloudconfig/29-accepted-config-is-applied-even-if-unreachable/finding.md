# Finding 29 — A rejected config is safe; an accepted one is not

**Endpoint** `PUT /cloud/cloudConfig`
**Type** Operational hazard
**Status** Confirmed repeatedly — the rollback config was needed several times

| Response | Effect |
|---|---|
| Schema rejection | **Nothing changes** — the reader keeps its current connection |
| `{"response":"success"}` | **Applied immediately**, even if the endpoint is unreachable |

There is no validation that the configured endpoint is actually reachable, and no
automatic revert.

## Why that is dangerous

An accepted-but-unreachable config drops the reader off **both** the new endpoint
and the old one. It is then unmanageable over MQTT — the very channel used to
configure it.

Confirmed directly in a related test: pointing `data.event` at unreachable
`10.255.255.1:1883` was accepted with HTTP 200 and left the interface
`disconnected` with error 255 indefinitely
([[16-cloud-connect-fires-on-failed-attempt]]).

## What made recovery possible

Every config used in this exercise sets:

```json
"enableLocalRest": true
```

That keeps the local REST API and web UI reachable regardless of cloud state,
which is the only reason the reader could be recovered each time. The rollback
config in this folder — pointing at the reader's own broker — was applied several
times over the course of testing.

## Practical guidance

1. **Always** set `enableLocalRest: true`, on every config.
2. Keep a known-good rollback config to hand before changing an endpoint.
3. Treat `{"response":"success"}` as "syntactically accepted", **not** as
   "connected". Confirm with
   `GET /cloud/status → interfaceConnectionStatus[].connectionStatus`.

## Ask

Could the reader validate reachability before committing an endpoint change, or
auto-revert after a timeout with no successful connection? A config that
disconnects the management channel cannot be undone through that channel.

## Evidence

`request body/` + `response body/` — `rest/cloud-cloudConfig-PUT/99-rollback-reader-own-broker-SUCCESS/`
