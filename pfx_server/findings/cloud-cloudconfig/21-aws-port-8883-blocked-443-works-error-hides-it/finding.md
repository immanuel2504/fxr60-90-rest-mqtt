# Finding 21 — Port 8883 to AWS is blocked; 443 works — and the error hides this

**Endpoint** `PUT /cloud/cloudConfig` (`mqtt-AWS`)
**Severity** High — the single most expensive issue in this exercise
**Status** Confirmed; tests differ **only** in the port

Tests 05 and 06 are identical apart from the port number. 8883 failed, 443
succeeded.

The failure looked like a certificate problem:

```
[DATA#1]/[EVENTS]/[CTRL]/[MGMT]: connection initialization failed with return code (255), retry count (0)
```

All four channels failing within ~2 ms with zero retries — which reads like a
local config fault, not a network one. That misdirection cost hours.

## AWS itself was proven fine first

Before the port was suspected, connecting from this host with the reader's exact
certificate files succeeded: MQTT connect, publish and subscribe all worked.
Credentials, policy, endpoint and reachability were all confirmed good — which is
what eventually left the port as the only remaining variable.

## The core problem

**The same generic error 255 is returned for a blocked TCP port and for a
certificate fault, with nothing to distinguish them.**

The same code also appears for an unreachable host — see
[[16-cloud-connect-fires-on-failed-attempt]]. Three distinct causes, one
indistinguishable message.

## Ask

1. What does error 255 mean at MQTT client initialization, and can the causes be
   distinguished?
2. Is 443 + ALPN the recommended path for AWS? 8883 is blocked on many corporate
   networks, and the spec does not mention this.

## Related

[[22-reader-requires-alpn-on-port-443]] — what port 443 additionally needs.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-port-8883-fails/` | `rest/cloud-cloudConfig-PUT/05-aws-installedCert-port8883-FAILED/` |
| `evidence-2-port-443-works/` | `rest/cloud-cloudConfig-PUT/06-aws-installedCert-port443-SUCCESS/` |
