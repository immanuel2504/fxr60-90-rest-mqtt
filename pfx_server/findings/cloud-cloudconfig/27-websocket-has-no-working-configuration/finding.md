# Finding 27 — `WEBSOCKET` has no working configuration on either endpoint

**Endpoints** `PUT /cloud/cloudConfig` **and** `PUT /cloud/config`
**Type** Unusable connection type
**Status** Unresolved — both possible shapes tested and both fail

The spec's `data_websocket` example carries **only** `security.verifyPeer`. There
is **nowhere to say where the reader should connect**.

Two shapes were tested. Neither yields a working connection.

## Shape A — the spec's example verbatim

```json
{"options": {"security": {"verifyPeer": false}}}
```

**Accepted** (HTTP 200) and stored verbatim, then silently does nothing:

```
interfaceConnectionStatus.data[0] = {interface: DATA_WS,
                                     connectionStatus: 'disconnected',
                                     connectionError: ''}
```

`connectionError` is **empty** — the reader gives no reason at all. Nothing ever
reached the WebSocket receiver on port 9444 (verified working independently).

Expected, since the config contains no destination. The finding is that the reader
**accepts** an address-less config rather than rejecting it.

## Shape B — add a schema-valid `endpoint` block

`endpoint` (`hostName`/`port`/`protocol`) **is** in the schema, unlike the fields
the `httpPost` example uses. Adding it, with a CA for verification:

```json
→ 422 {"code":3,"message":"Invalid Cloud Config File Schema - DATA config: event - invalid WEBSOCKET configuration (invalid \"security\" JSON object)"}
```

**Rejected.** The `WEBSOCKET` security object accepts **only** `verifyPeer` —
`CACertificateFileLocation`, `verifyHostName` and the rest are refused for this
type specifically.

## So both paths are closed

| Shape | Address? | Result |
|---|---|---|
| Spec example | none | accepted, never connects, no error |
| With `endpoint` + CA | yes | rejected — security block too rich for this type |

## Not endpoint-specific

Test 12 on `PUT /cloud/config` was run specifically to see whether that endpoint
validated `WEBSOCKET` differently. **It does not** — identical behaviour: accepted,
stored, `connectionStatus: disconnected`, empty `connectionError`, no connection
attempt.

## A wrong inference, corrected

Port 9000 was observed open on the reader after this test and initially taken for a
WebSocket listener. **Reverting the config left 9000 still open**, so it is
unrelated — the earlier port scan simply had not covered 9000. It is not opened by
the `WEBSOCKET` config.

## Ask

**Where does the WebSocket address go?** No documented field carries it, the
`endpoint` block is rejected for this type, and the security object accepts only
`verifyPeer`. As documented, `WEBSOCKET` cannot be configured at all.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-spec-shape-accepted-never-connects/` | `rest/cloud-cloudConfig-PUT/11-websocket-spec-shape-ACCEPTED-never-connects/` |
| `evidence-2-endpoint-block-rejected/` | `rest/cloud-cloudConfig-PUT/12-websocket-with-endpoint-REJECTED/` |
