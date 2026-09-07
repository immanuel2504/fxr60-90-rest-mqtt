# FXR60 MQTT Endpoint Configuration

Everything needed to point the FXR60 reader at our own MQTT broker, under four
different security models.

```
Mqqt/
├── README.md                             this file
├── certificate/                          certificates to copy to the reader
│   ├── lab-ca.crt                        CA — verify the broker
│   ├── fxr60-client.crt                  reader's own certificate
│   ├── fxr60-client.key                  reader's private key (SECRET)
│   └── fxr60-lab-client.pfx              bundle for certificate-store install
├── 00-install-client-certificate.json    install the client cert (needed for 04)
├── 01-plain-1883.json                    plain MQTT
├── 03-mtls-8884-filepaths.json           mutual TLS via file paths
├── 04-mtls-8884-certstore.json           mutual TLS via certificate store
└── 99-rollback-reader-own-broker.json    recovery — back to the reader's own broker
```

---

## Contents

1. [Prerequisites](#1-prerequisites)
2. [The broker](#2-the-broker)
3. [The certificates](#3-the-certificates)
4. [How to send a config](#4-how-to-send-a-config)
5. [Endpoint 01 — plain MQTT](#5-endpoint-01--plain-mqtt-1883)
6. [Why there is no TLS-only example](#6-why-there-is-no-tls-only-example)
7. [Endpoint 03 — mTLS via file paths](#7-endpoint-03--mtls-via-file-paths-8884)
8. [Endpoint 04 — mTLS via certificate store](#8-endpoint-04--mtls-via-certificate-store-8884)
9. [Recovery](#9-recovery)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Prerequisites

### Before you start

| Requirement | How to check |
|---|---|
| Reader reachable on the network | `ping 10.117.229.9` |
| Broker host reachable from the reader | must be able to reach `10.117.229.18` |
| Brokers running | see [section 2](#2-the-broker) |
| A way to send config to the reader | REST + Bearer token, MQTT, or the web UI |
| For TLS/mTLS: certificates on the reader | copied into `/data/apps/` |

### Recommended order

Each step adds exactly one variable, so a failure tells you which piece broke.

```
01 plain  →  03 mTLS files  →  04 mTLS store
   ↑              ↑                 ↑
 nothing    + CA + own cert    + cert store
```

There is no server-auth-only TLS step. The reader rejects a CA-only security
block on the data-event channel, so mutual TLS is the first secure option —
see [section 6](#6-why-there-is-no-tls-only-example).

Start with **01**. It differs from the reader's default only in the broker address,
so if it works, networking is confirmed and every later failure is about security.

### Keep this to hand

`99-rollback-reader-own-broker.json` returns the reader to its own built-in broker.
A config that is *accepted but cannot connect* drops the reader off both the new
broker and the old one — you will need this.

Keep `enableLocalRest: true` in every config (all files here do). It keeps the
reader's web UI reachable even when MQTT is broken, which is how recovery is done.

---

## 2. The broker

Four Mosquitto brokers on **`10.117.229.18`**, one per security model. All
systemd-managed and enabled at boot.

| Port | Security model | Client needs | systemd service |
|---|---|---|---|
| **1883** | Plain, anonymous | nothing | `mosquitto` |
| **1884** | Username/password | credentials | `mosquitto-fxr60-auth-1884` |
| **8883** | TLS, server auth | CA cert | `mosquitto-fxr60-tls-8883` |
| **8884** | Mutual TLS | CA + client cert/key | `mosquitto-fxr60-mtls-8884` |

Port 1884 is listed for completeness but has **no example here** — the reader's
API has no working way to supply broker credentials (see
[section 10](#10-troubleshooting)).

### Check they are running

```bash
for s in mosquitto mosquitto-fxr60-auth-1884 \
         mosquitto-fxr60-tls-8883 mosquitto-fxr60-mtls-8884; do
  printf "%-34s %s\n" "$s" "$(systemctl is-active $s)"
done
```

### Prove they work

```bash
cd /home/altautoadmin/pfx_server
H=10.117.229.18

mosquitto_pub -h $H -p 1883 -t chk -m x                            # plain
mosquitto_pub -h $H -p 8883 --cafile ca/ca.crt -t chk -m x         # TLS
mosquitto_pub -h $H -p 8884 --cafile ca/ca.crt \
  --cert broker-certs/fxr60-client.crt \
  --key  broker-certs/fxr60-client.key -t chk -m x                 # mTLS
```

Silence means success.

### Watch traffic

```bash
# everything on the plain broker
mosquitto_sub -h 10.117.229.18 -p 1883 -t '#' -v

# just the reader's heartbeats
mosquitto_sub -h 10.117.229.18 -p 1883 -t 'fxr60-lab/mevents'
```

### Logs

```
/var/log/mosquitto/mosquitto.log      port 1883
/var/log/mosquitto/fxr60-auth.log     port 1884
/var/log/mosquitto/fxr60-tls.log      port 8883
/var/log/mosquitto/fxr60-mtls.log     port 8884
```

Full operational detail: `../BROKER_REFERENCE.md`.
How the brokers were built: `../MQTT_BROKER_SETUP_GUIDE.md`.

---

## 3. The certificates

All in `certificate/`, all signed by **Local RFID Test CA** — the same CA the
broker uses, which is what allows the two to trust each other.

| File | Secret? | Purpose |
|---|---|---|
| `lab-ca.crt` | No | Reader uses this to **verify the broker** |
| `fxr60-client.crt` | No | Reader's own certificate — **proves who it is** |
| `fxr60-client.key` | **YES** | Private key proving the reader owns that certificate |
| `fxr60-lab-client.pfx` | **YES** | The cert + key bundled, for endpoint 04. Password: `Fxr60-Client-Pfx-2026!` |

### Which endpoint needs what

| Endpoint | Files on reader |
|---|---|
| 01 plain | none |
| 03 mTLS files | `lab-ca.crt`, `fxr60-client.crt`, `fxr60-client.key` |
| 04 mTLS store | none as files — the `.pfx` is installed into the cert store instead |

### Copying them to the reader

Destination is **`/data/apps/`**. Writes to `/data` directly are denied on this
reader.

```
certificate/lab-ca.crt         →  /data/apps/lab-ca.crt
certificate/fxr60-client.crt   →  /data/apps/fxr60-client.crt
certificate/fxr60-client.key   →  /data/apps/fxr60-client.key
```

The JSON files reference exactly these paths, so keep the names as-is or update the
JSON to match.

### Verifying them

```bash
cd certificate

# CA-signed? subject and issuer must DIFFER
openssl x509 -in fxr60-client.crt -noout -subject -issuer

# does the chain validate?
openssl verify -CAfile lab-ca.crt fxr60-client.crt

# do cert and key match? both hashes must be identical
openssl x509 -noout -modulus -in fxr60-client.crt | openssl md5
openssl rsa  -noout -modulus -in fxr60-client.key | openssl md5
```

Creating your own set: `../CERTIFICATE_GUIDE.md`.

### Do not use the AWS certificate here

`../FXR60-LAB/` holds an AWS IoT certificate signed by **Amazon Root CA 1** — a
different CA. Our broker correctly rejects it. That is the trust boundary working,
not a fault.

---

## 4. How to send a config

Three ways; all write the same underlying configuration.

### REST (Postman)

```
PUT https://10.117.229.9/cloud/cloudConfig
Authorization: Bearer <token from GET /cloud/localRestLogin>
Content-Type: application/json

Body: the contents of the .json file, as-is
```

### MQTT

Wrap the file contents in a command envelope and publish to the reader's current
command topic:

```json
{
  "command": "set_importCloudConfig",
  "command_id": "cfg-1",
  "payload": <file contents>
}
```

### Web UI

`https://10.117.229.9` → **ENDPOINT** tab → fill the fields → **PUBLISH**.
Handy for recovery, since it works even when MQTT is down.

### What a response means

| Response | Meaning |
|---|---|
| `{"response":"success"}` | Config **accepted and applied**. Reader switches immediately |
| `{"code":3,...schema...}` | **Rejected** — nothing changed, reader keeps its current connection |
| No response | Reader may have already switched away from the topic you asked on |

Accepted does **not** mean connected. Always verify afterwards.

---

## 5. Endpoint 01 — plain MQTT (1883)

**File:** `01-plain-1883.json` — **confirmed working**

No encryption, no authentication. The baseline.

```json
"enableSecurity": false,
"endpoint": { "hostName": "10.117.229.18", "port": 1883, "protocol": "tcp" }
```
No `security` block at all.

### Steps

1. Nothing to prepare — no certificates needed
2. Send `01-plain-1883.json`
3. Verify:

```bash
mosquitto_sub -h 10.117.229.18 -p 1883 -t fxr60-lab/mrsp &
mosquitto_pub -h 10.117.229.18 -p 1883 -t fxr60-lab/mcmd \
  -m '{"command":"get_status","command_id":"t1","payload":{}}'
```

A full status response means it works.

### Confirmed evidence

All four reader clients connected (`fxr60-lab-ctrl`, `-data`, `-mcmd`, `-mevents`),
heartbeats arriving on `fxr60-lab/mevents` every ~60s, and `get_status` returning a
correct response. The heartbeat itself reports:

```json
"interfaceConnectionStatus": {
  "management": [{"interface":"MGMT_CMD_MQTT","connectionStatus":"connected",
                  "stats":{"commands_received":2,"responses_sent":2,"responses_failed":0}}]
}
```

### Next step

Endpoint 03 — adds mutual TLS. (There is no TLS-only step; see section 6.)

---

## 6. Why there is no TLS-only example

Server-auth-only TLS (broker proves identity, reader does not) **cannot be
configured on this reader**, because of a constraint the schema does not document.

### What was tried

A config with a CA-only security block on all four channels, port 8883:

```json
"security": {
  "CACertificateFileLocation": "/data/apps/lab-ca.crt",
  "keyAlgorithm": "RS256",
  "keyFormat": "PEM",
  "verifyHostName": true,
  "verifyPeer": true
}
```

### The result

```json
{
  "code": 3,
  "message": "Invalid Cloud Config File Schema - DATA config: event - invalid configuration (invalid \"security\" JSON object)"
}
```

Note it names **one channel only**: `DATA config: event`. The identical CA-only
block was accepted on `control.commandResponse`, `management.event` and
`management.commandResponse`.

### Why

**The data-event channel requires a client certificate.** Either the
`privateKeyFileLocation` + `publicKeyFileLocation` pair, or
`installedCertificateName` + `installedCertificateType`. CA-only is not accepted
there, though it is on the other three channels.

This is confirmed by the spec's own examples — every data-event example supplies a
full client identity:

| Spec example | data.event security |
|---|---|
| `mqtt_tls_all_channels` | CA + `privateKeyFileLocation` + `publicKeyFileLocation` |
| `data_mqtt_tls_installed_cert` | `installedCertificateName` + `installedCertificateType` |

No example anywhere gives data-event a CA-only block.

### The schema does not say this

The `security` schema is **identical** for all four channels and specifies
`required: None` on each — implying CA-only is valid anywhere. It is not. Nothing
in the documented schema predicts this constraint.

Logged in `../MQTT_API_Findings.xlsx` as an undocumented constraint, with a request
that Zebra either document it or confirm it is a firmware bug.

### Consequence

Mutual TLS is effectively **mandatory** for encrypted tag-data delivery. Go
straight from endpoint 01 to endpoint 03.

---

## 7. Endpoint 03 — mTLS via file paths (8884)

**File:** `03-mtls-8884-filepaths.json`

Both sides prove identity.

```json
"security": {
  "CACertificateFileLocation": "/data/apps/lab-ca.crt",
  "privateKeyFileLocation":    "/data/apps/fxr60-client.key",
  "publicKeyFileLocation":     "/data/apps/fxr60-client.crt",
  "keyAlgorithm": "RS256",
  "keyFormat": "PEM",
  "verifyHostName": true,
  "verifyPeer": true
}
```

### Field mapping

| Certificate | JSON field |
|---|---|
| `lab-ca.crt` — verify the broker | `CACertificateFileLocation` |
| `fxr60-client.crt` — reader's own cert | `publicKeyFileLocation` |
| `fxr60-client.key` — proves ownership | `privateKeyFileLocation` |

Note the reader's **certificate** goes in a field named `publicKeyFileLocation`.
Confusing, but that is the field the reader expects.

### Steps

1. Copy all three files to `/data/apps/`:
   ```
   lab-ca.crt
   fxr60-client.crt
   fxr60-client.key
   ```
2. Confirm the broker is up: `systemctl is-active mosquitto-fxr60-mtls-8884`
3. Send `03-mtls-8884-filepaths.json`
4. Verify:

```bash
cd /home/altautoadmin/pfx_server
mosquitto_sub -h 10.117.229.18 -p 8884 --cafile ca/ca.crt \
  --cert broker-certs/fxr60-client.crt --key broker-certs/fxr60-client.key \
  -t fxr60-lab/mrsp &

mosquitto_pub -h 10.117.229.18 -p 8884 --cafile ca/ca.crt \
  --cert broker-certs/fxr60-client.crt --key broker-certs/fxr60-client.key \
  -t fxr60-lab/mcmd -m '{"command":"get_status","command_id":"t3","payload":{}}'

sudo tail -20 /var/log/mosquitto/fxr60-mtls.log
```

The mTLS log is the best diagnostic here — it reports whether the reader presented
a certificate at all, and if so why it was accepted or rejected.

### What changed from 01

`enableSecurity` → `true`, `port` → `8884`, `protocol` → `ssl`, plus a `security`
block carrying all three certificate references. These must change together —
changing the port alone attempts a plain connection against a TLS listener.

### Next step

Endpoint 04 — same result via the certificate store instead of file paths.

---

## 8. Endpoint 04 — mTLS via certificate store (8884)

**File:** `04-mtls-8884-certstore.json`

Identical security to 03, but the reader references a certificate held in its own
store rather than loose files.

```json
"security": {
  "installedCertificateName": "FXR60-LAB-CLIENT",
  "installedCertificateType": "client",
  "keyAlgorithm": "RS256",
  "keyFormat": "PEM",
  "verifyHostName": true,
  "verifyPeer": true
}
```

### Steps

**1. The `.pfx` is already being served**

The file server runs as a systemd service (`pfx-file-server`), enabled at boot and
set to restart automatically. Nothing to start.

Confirm it is up:

```bash
systemctl is-active pfx-file-server                       # expect: active

curl -sk -u 'altautoadmin:@1T@uT0dud3' -o /dev/null -w "%{http_code}\n" \
  https://10.117.229.18/fxr60-lab-client.pfx              # expect 200
```

If a different `.pfx` needs serving, drop it into
`/home/altautoadmin/pfx_server/files/` — no restart required.

**2. Install it onto the reader**

Send `00-install-client-certificate.json` to:

```
PUT https://10.117.229.9/cloud/certificates
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "name": "FXR60-LAB-CLIENT",
  "type": "client",
  "url": "https://10.117.229.18/fxr60-lab-client.pfx",
  "authenticationType": "BASIC",
  "authenticationOptions": {
    "username": "altautoadmin",
    "password": "@1T@uT0dud3"
  },
  "pfxPassword": "Fxr60-Client-Pfx-2026!",
  "verifyPeer": false,
  "verifyHost": false
}
```

Expected: `{"response":"success"}` (REST returns HTTP 200).

**Use `BASIC` — the other methods do not work.** Testing on Reader Application
5.0.5 found only Basic authentication succeeds for this download:

| Download auth method | Result |
|---|---|
| `BASIC` via `authenticationOptions` | ✅ Success |
| `NONE` (anonymous) | ❌ HTTP 422 — `INVALID USER NAME` |
| Bearer token in `headers.Authorization` | ❌ HTTP 422 — `INVALID USER NAME` |
| mTLS using an installed certificate | ❌ HTTP 422 — reader presented no client cert |

Full detail: `../CERTIFICATE_AUTH_TEST_REPORT.md`.

Note the misleading error: `NONE` and Bearer both report `INVALID USER NAME` even
though no username was supplied — and in both cases the reader never contacted the
file server at all.

**3. Confirm it installed** — `get_certificates` should list `FXR60-LAB-CLIENT`

**4. Send `04-mtls-8884-certstore.json`**, then verify exactly as for 03

No need to stop the file server — it is a managed service and stays running.

### Status of this method

`installedCertificateName` is what makes the AWS connection work, so the mechanism
is real. But every earlier local attempt failed with
`connection initialization failed with return code (255), retry count (0)`. That
turned out to be a blocked port in the AWS case — so the local failures may have
had the same cause, or a different one. It has not been independently confirmed
against our own broker.

This is why 03 comes first: if **03 works and 04 fails**, that isolates
`installedCertificateName` as genuinely faulty, which is a real finding worth
reporting.

---

## 9. Recovery

**File:** `99-rollback-reader-own-broker.json`

Returns the reader to its own built-in broker at `10.117.229.9:1883`.

### When you need it

- Reader unreachable on both the new broker and the old one
- A config was accepted but the connection never came up
- You want a known-good state before trying something else

### How

The web UI is the most reliable route, because it works even when MQTT is
completely down — that is what `enableLocalRest: true` buys you.

```
https://10.117.229.9  →  ENDPOINT tab  →  set the values below  →  PUBLISH
```

| Field | Value |
|---|---|
| Endpoint Type | MQTT |
| Server | `10.117.229.9` |
| Port | `1883` |
| Protocol | TCP |
| Client Id | `fxr60-lab-mcmd` (per channel: `-ctrl`, `-data`, `-mevents`) |
| Publish topic | `fxr60-lab/mrsp` |
| Subscribe topic | `fxr60-lab/mcmd` |

Repeat for all four channels. Or send the JSON file via Postman if REST is
reachable.

### Confirm recovery

```bash
cd /home/altautoadmin/pfx_server
.venv/bin/python -c "
import json,time,uuid,paho.mqtt.client as mqtt
r={};c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id='chk-'+uuid.uuid4().hex[:6])
c.on_connect=lambda *a,**k: c.subscribe('fxr60-lab/mrsp')
c.on_message=lambda cl,u,m: r.update({'x':m.payload[:80]})
c.connect('10.117.229.9',1883);c.loop_start();time.sleep(1)
cid='chk-'+uuid.uuid4().hex[:6]
c.publish('fxr60-lab/mcmd',json.dumps({'command':'get_status','command_id':cid,'payload':{}}))
time.sleep(5);c.loop_stop()
print('reader responding' if r else 'no response')
"
```

---

## 10. Troubleshooting

### `invalid "..." path: File Not Found`

A certificate file is missing on the reader. The message names which one. Harmless
— the config was rejected, so the reader kept its current connection. Copy the file
to `/data/apps/` and resend.

### `CS:'Add/Refresh certificate' failed,Reason: Could not connect to remote host`

The reader could not reach the file server hosting the `.pfx`.

```bash
systemctl is-active pfx-file-server         # expect: active
sudo systemctl restart pfx-file-server      # if not
ss -tlnp | grep ":443"                      # expect 0.0.0.0:443
```

The server is a systemd service enabled at boot, so this should be rare. If the
service is active but the reader still cannot connect, check network reachability
from the reader's segment to `10.117.229.18:443` — the reader's outbound access
differs from this host's.

Distinguish it from the auth failure:

| Error | Meaning |
|---|---|
| `Could not connect to remote host` | Nothing listening — reader got no response at all |
| `INVALID USER NAME` | Server was reached, but auth was wrong or not `BASIC` |

### `invalid "security" JSON object`

A field in the `security` block is not in the schema. The nine permitted fields are:

```
CACertificateFileLocation   installedCertificateName   installedCertificateType
keyAlgorithm                keyFormat                  privateKeyFileLocation
publicKeyFileLocation       verifyHostName             verifyPeer
```

Notably `CACertificateFileContent` / `privateKeyFileContent` /
`publicKeyFileContent` (inline PEM) are **not** valid here — even though the
spec's own AWS example uses them. That is a documented spec bug.

### `connection initialization failed with return code (255), retry count (0)`

**Read this before assuming a certificate problem.** This generic error appears for
a **blocked port** just as often as a certificate fault, with nothing to
distinguish them. It cost hours during the AWS work — the cause turned out to be
port 8883 blocked on the reader's network path, not certificates at all.

Check port reachability from the reader's segment first. The reader's outbound
access differs from this host's: 8883 to AWS was blocked from the reader while open
from here.

### Reader shows "connected" but nothing arrives

Check the broker log for the reader's client IDs:

```bash
sudo grep -E "fxr60-lab-(ctrl|data|mcmd|mevents)" \
  /var/log/mosquitto/mosquitto.log | tail
```

Absent means the reader is connected somewhere else — its own broker, or AWS.

### mTLS rejects a valid-looking certificate

Probably signed by a different CA than the broker trusts:

```bash
openssl verify -CAfile certificate/lab-ca.crt <the-cert>
```

`unable to get local issuer certificate` means wrong CA. The AWS certificate fails
this check by design.

### Best diagnostic available

The reader's heartbeat events on `fxr60-lab/mevents` carry per-interface
`connectionStatus` and `connectionError` — far more useful than the reader's
generic error codes. If any one channel still reaches a working broker, subscribe
to its management-events topic to learn why the others are failing.

### Username/password (port 1884) — why there is no example

The reader's firmware clearly supports it: `basicAuthentication` appears in the
reader's own `get_config` output, and the web UI has a "BASIC Authentication"
checkbox. But:

- The field is in **no schema** in `FXR_60-90_rest_api.yaml`
- The one example showing it (`mqtt-Azure`) places it inside `options`, while the
  reader reports it inside `options.additional`

Sending it either way did not work. Open question for Zebra — the capability
exists in firmware but the documented API cannot reliably reach it.

---

## Summary

| # | File | Port | Security | Files on reader | Status |
|---|---|---|---|---|---|
| 00 | `00-install-client-certificate.json` | — | — | — | Prerequisite for 04 |
| 01 | `01-plain-1883.json` | 1883 | none | none | ✅ **Confirmed working** |
| 03 | `03-mtls-8884-filepaths.json` | 8884 | CA + cert + key | 3 | Not yet tested |
| 04 | `04-mtls-8884-certstore.json` | 8884 | installed cert | 0 (pfx installed) | Not confirmed locally |
| 99 | `99-rollback-reader-own-broker.json` | 1883 | none | none | Recovery |

All four validated against the `SetImportcloudconfigRequest` schema — every field
permitted, no extras.

Two security models have **no example** because the reader cannot be configured for
them:

| Model | Why |
|---|---|
| Username/password (1884) | No schema field for broker credentials — see [section 10](#10-troubleshooting) |
| TLS, server auth only (8883) | data-event requires a client certificate — see [section 6](#6-why-there-is-no-tls-only-example) |

---

## Related documents

| File | Contents |
|---|---|
| `../BROKER_REFERENCE.md` | Operating the four brokers |
| `../MQTT_BROKER_SETUP_GUIDE.md` | Building a broker from scratch |
| `../CERTIFICATE_GUIDE.md` | Creating CA-signed certificates |
| `../MTLS_SIMPLE_GUIDE.md` | TLS vs mTLS explained simply |
| `../Aws example/` | The same, for AWS IoT Core |
| `../MQTT_API_Findings.xlsx` | API findings and open questions for Zebra |
