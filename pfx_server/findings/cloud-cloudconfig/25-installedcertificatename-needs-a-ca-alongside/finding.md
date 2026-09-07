# Finding 25 — `installedCertificateName` needs a CA alongside it — an open question resolved

**Endpoint** `PUT /cloud/cloudConfig`
**Type** Root cause found for a long-standing failure
**Status** Confirmed by an A/B pair

## The symptom

Test 04 was accepted (HTTP 200) but the connection failed immediately and
repeatedly:

```
OpenSSL Error[0]: error:0A000418:SSL routines::tlsv1 alert unknown ca
Client <unknown> disconnected: Protocol error.
```

`unknown ca` is a TLS alert sent **by the reader** — it is rejecting *our
broker's* certificate, not the other way round.

## Root cause

The security block supplied only `installedCertificateName` +
`installedCertificateType`. That gives the reader its **own identity** but **no CA
with which to verify the broker**. With `verifyPeer: true` and no trust anchor,
the reader rejects the broker as `unknown ca`.

| Test | Security block | Result |
|---|---|---|
| 03 | `CACertificateFileLocation` + `privateKeyFileLocation` + `publicKeyFileLocation` | ✅ works |
| 04 | `installedCertificateName` + `installedCertificateType` only | ❌ `unknown ca` |
| **04b** | `installedCertificateName` + **`CACertificateFileLocation`** | ✅ **connects immediately** |

## This resolves an earlier open question

`installedCertificateName` had long been suspected of being **broken**, because it
failed repeatedly during the AWS work.

**It is not broken.** It simply does not supply a CA, and must be paired with
`CACertificateFileLocation` whenever `verifyPeer` is `true`.

It worked for AWS only because the reader **already trusts Amazon's public root
CA** — so the missing trust anchor never mattered there. Against a private lab
broker it does.

## Ask

Document that `installedCertificateName` provides client identity only, and that a
CA source is required alongside it when `verifyPeer` is true — unless the peer
chains to a CA the reader already trusts.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-certstore-alone-fails-unknown-ca/` | `rest/cloud-cloudConfig-PUT/04-mqtt-mtls-8884-certstore-FAILED/` |
| `evidence-2-certstore-plus-CA-works/` | `rest/cloud-cloudConfig-PUT/04b-mqtt-mtls-8884-certstore-plus-CA-SUCCESS/` |
