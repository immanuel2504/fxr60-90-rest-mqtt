# Finding 24 — `data.event` requires a client certificate — undocumented

**Endpoint** `PUT /cloud/cloudConfig`
**Type** Undocumented per-channel constraint
**Status** Confirmed; only one of four channels rejected the same block

Test 02 sent an identical CA-only security block on all four channels. **Only one
was rejected:**

```json
{"code":3,"message":"Invalid Cloud Config File Schema - DATA config: event - invalid configuration (invalid \"security\" JSON object)"}
```

`control.commandResponse`, `management.event` and `management.commandResponse` all
**accepted** the same block.

## Confirmed by the spec's own examples

Every `data.event` example supplies a full client identity:

| Spec example | `data.event` security |
|---|---|
| `mqtt_tls_all_channels` | CA + `privateKeyFileLocation` + `publicKeyFileLocation` |
| `data_mqtt_tls_installed_cert` | `installedCertificateName` + `installedCertificateType` |

Test 03 then confirmed the positive case: mTLS with `CACertificateFileLocation` +
`privateKeyFileLocation` + `publicKeyFileLocation` is accepted on `data.event`.

## The schema does not express this

It is **identical** across all four channels, with `required: None` on each. There
is nothing to indicate that `data.event` alone demands a client certificate.

## Consequence

Server-auth-only TLS **cannot** be configured for tag data. Mutual TLS is
effectively mandatory on that channel.

## Ask

Document the constraint in the schema, or confirm it is a bug and that CA-only
should be accepted as the schema implies.

## Related

[[25-installedcertificatename-needs-a-ca-alongside]] — the other half of getting
`data.event` security right.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-ca-only-rejected-on-data-event/` | `rest/cloud-cloudConfig-PUT/02-mqtt-tls-8883-CAonly-REJECTED/` |
| `evidence-2-mtls-filepaths-accepted/` | `rest/cloud-cloudConfig-PUT/03-mqtt-mtls-8884-filepaths-SUCCESS/` |
