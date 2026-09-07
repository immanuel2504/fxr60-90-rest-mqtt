# Finding 22 — `alpnProtocolNames` is **required** input on port 443 — a correction

**Endpoint** `PUT /cloud/cloudConfig` (`mqtt-AWS`)
**Type** Schema gap + **withdrawn** claim
**Status** Confirmed by the reader's own error message

## The claim that was wrong

An earlier conclusion stated that `alpnProtocolNames` is **output-only** — added
by the firmware, absent from the `additional` schema, and therefore **must not be
sent**.

**That was wrong.** The reasoning was unsound: *absent from schema ⇒ prohibited*
does not hold on this API, where the schema is demonstrably incomplete (see
[[23-schema-is-incomplete-not-authoritative]]).

## What the reader actually says

A `*FileLocation` AWS payload on port 443 **without** ALPN was rejected:

```
AWS requires ALPN protocol name for "port" number 443
```

Adding it worked:

```json
"alpnProtocolNames": ["x-amzn-mqtt-ca"]
```

So `alpnProtocolNames` is **required input** for port 443, not output-only. It is
also genuinely absent from the documented `additional` schema — which is the real
defect here.

## Why the firmware appeared to add it

`GET`/`get_config` does return `alpnProtocolNames: ["x-amzn-mqtt-ca"]` on every
port-443 connection, which is what prompted the original wrong inference. It
appears in output *because it is required input* — on the working port-443
configurations it had already been supplied.

## Ask

Add `alpnProtocolNames` to the `additional` schema and document it as required
when `port` is 443 with `mqtt-AWS`.

## The lesson

On this API, a field's absence from the schema says nothing about whether it is
accepted, required, or rejected. Only a test settles it.

## Evidence

`request body/` + `response body/` — `rest/cloud-cloudConfig-PUT/08-aws-fileLocation-SUCCESS/`
