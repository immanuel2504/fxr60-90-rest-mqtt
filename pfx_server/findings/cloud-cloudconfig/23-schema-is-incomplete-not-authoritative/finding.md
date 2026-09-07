# Finding 23 — The schema is incomplete, not authoritative — a correction

**Endpoint** `PUT /cloud/cloudConfig`
**Type** Methodological finding + **withdrawn** prediction
**Status** Established by two opposite results

## The prediction that was wrong

The schema for `data.event.options` permits exactly six fields:

```
additional  enableSecurity  endpoint  publishTopic  security  subscribeTopic
```

Several documented connection types use fields outside that set. Having seen two
such fields **rejected**, the report predicted `httpPost` and `tcpip-server` would
be rejected the same way, and marked them "schema gap expected".

**Both were accepted.**

## What actually happens

| Fields | Used in example | In schema? | Reader's verdict |
|---|---|---|---|
| `CACertificateFileContent`, `privateKeyFileContent`, `publicKeyFileContent` | `mqtt_aws_all_channels` | ❌ | **Rejected** |
| `URL`, `authenticationType`, `verifyHost` | `data_http_post` | ❌ | ✅ **Accepted, works end to end** |
| `tcpipport` | `data_tcpip_server` | ❌ | ✅ **Accepted, reader listens** |
| `alpnProtocolNames` | — | ❌ | ✅ **Required** on port 443 |
| `basicAuthentication` | `mqtt-Azure` examples | ❌ | ✅ Accepted in `options.additional` |

`httpPost` was proven fully working — 18 POSTs, 170 tag events, 8 unique EPCs
delivered to the receiver.

## Conclusion

**The validator applies per-type rules; the documented schema is an incomplete
description of them.** A field's absence from `data.event.options` predicts
nothing:

- some absent fields are rejected (`*FileContent`)
- some are accepted and work (`URL`, `tcpipport`, `basicAuthentication`)
- one is outright **required** (`alpnProtocolNames` on port 443)

## The methodological lesson

This corrected reasoning that had already produced two wrong calls — the ALPN
claim in [[22-reader-requires-alpn-on-port-443]] and these two predicted
rejections. On this API, only a test settles whether a field is accepted.

## Ask

Either complete the schema with the per-type field sets the validator actually
enforces, or state that the schema is indicative and the examples are normative.
At present three of six documented connection types cannot be configured from the
documented schema alone.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-httppost-undocumented-fields-accepted/` | `rest/cloud-cloudConfig-PUT/10-httpPost-SUCCESS/` |
| `evidence-2-inline-filecontent-rejected/` | `rest/cloud-cloudConfig-PUT/07-aws-inline-FileContent-REJECTED/` |
