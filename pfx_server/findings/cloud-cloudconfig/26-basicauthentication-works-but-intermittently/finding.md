# Finding 26 — `basicAuthentication` works, in the undocumented placement — but intermittently

**Endpoint** `PUT /cloud/cloudConfig`
**Type** Undocumented field + reliability defect + **withdrawn** claim
**Status** Works, but unreliably

## The claim that was wrong

An earlier conclusion was that `basicAuthentication` **never worked** in either
placement, and was "supported by firmware but unreachable via the API".

**That was wrong.** It works — in one specific placement.

## Correct placement

```
options.additional.basicAuthentication = {username, password}     ✅ works
options.basicAuthentication            (the spec's mqtt-Azure example)   ✗
```

The working placement matches the **reader's own `get_config` output**, not the
spec's example. Confirmed stored correctly via `GET /cloud/config`.

## Proof it works

The auth broker logged the reader connecting **with the username** on four
separate occasions:

```
New client connected from 10.233.48.36 as fxr60-lab-mcmd (u'fxr60user')
New client connected from 10.233.48.36 as fxr60-lab-data (u'fxr60user')
```

The `u'fxr60user'` field is mosquitto recording the authenticated username.

## But it is intermittent

In the **same session**, other attempts were rejected:

```
Sending CONNACK to 10.233.48.36 (0, 5)      ← MQTT return code 5 = not authorised
Client <unknown> disconnected, not authorised.
```

`<unknown>` means the client was rejected before its ID was registered — i.e. it
connected **without credentials** on those attempts. Reader-side:
`connection initialization failed with return code (255), retry count (0)`.

The broker credentials are valid throughout — `mosquitto_pub` with the same
username/password succeeds every time.

**So the reader sometimes sends the stored credentials and sometimes does not.**
Cause not established.

## Why this is worth reporting

Intermittent credential presentation is **worse than an outright failure**,
because it looks like a broker problem. Considerable time went into checking the
broker before the reader was suspected.

## Ask

1. Is `basicAuthentication` supported, and in which object? The reader reports it
   inside `options.additional`; the spec's example puts it in `options`.
2. Why would stored credentials be omitted on some connection attempts?

## Evidence

`request body/` + `response body/` — `rest/cloud-cloudConfig-PUT/09-mqtt-username-password-1884-WORKS-intermittent/`
