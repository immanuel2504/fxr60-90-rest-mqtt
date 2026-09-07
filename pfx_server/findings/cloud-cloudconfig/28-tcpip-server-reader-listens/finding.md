# Finding 28 — `tcpip-server`: the reader listens — confirmed empirically

**Endpoint** `PUT /cloud/cloudConfig` (`tcpip-server`)
**Type** Undocumented integration direction — now settled
**Status** Confirmed

For this connection type the **reader is the server**. Clients connect *to it* —
the reverse of every other type.

## Proof

```
before: nc -zv 10.233.48.36 8081   → closed
after : nc -zv 10.233.48.36 8081   → succeeded
```

`receivers/tcpip_client.py` then connected to `10.233.48.36:8081` and held the
connection open. No tag data arrived because no inventory was running.

The spec's example **implies** this by carrying a port and no hostname, but never
states it. It matters: it inverts the integration architecture, and a firewall
must allow inbound connections to the reader rather than outbound from it.

## Also disproves a prediction

`options.tcpipport` is absent from the documented schema, and this test was
expected to be rejected for that reason. It was **accepted and stored verbatim**
(confirmed via `GET /cloud/config`) — see
[[23-schema-is-incomplete-not-authoritative]].

Note `tcpipport` is a **string** in the spec's example, not a number, and was
kept as a string here.

## A quirk in `connectionStatus`

The reader reported `disconnected` with an empty `connectionError` **while the
port was open and accepting connections**. So for this type the field appears to
mean *"no data flowing"* rather than *"not listening"* — worth knowing before
using it for health monitoring.

## Ask

State explicitly in the docs that the reader listens for `tcpip-server`, and
clarify what `connectionStatus` means for a type where the reader is the server.

## Evidence

`request body/` + `response body/` — `rest/cloud-cloudConfig-PUT/13-tcpip-server-ACCEPTED-reader-listens/`
