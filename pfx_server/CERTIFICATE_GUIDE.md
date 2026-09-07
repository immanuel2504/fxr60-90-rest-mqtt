# Creating and Installing CA-Signed Certificates

How to build a certificate authority, issue CA-signed certificates for the MQTT
broker and the FXR60 reader, and install them on both sides for mutual TLS.

---

## Contents

1. [Concepts](#1-concepts)
2. [Creating the certificates](#2-creating-the-certificates)
3. [Installing on the broker](#3-installing-on-the-broker)
4. [Installing on the reader](#4-installing-on-the-reader)
5. [Verifying](#5-verifying)
6. [Common mistakes](#6-common-mistakes)
7. [What we already have](#7-what-we-already-have)

---

## 1. Concepts

### Self-signed vs CA-signed

A certificate carries a **subject** (who it identifies) and an **issuer** (who
vouched for it).

| | Subject vs issuer | Trust model |
|---|---|---|
| **Self-signed** | identical | Each peer must be told to trust that exact certificate |
| **CA-signed** | different | Peers trust the CA; anything it signs is trusted automatically |

The **CA's own certificate is necessarily self-signed** — nothing exists above a
root CA to vouch for it. That is the one and only self-signed certificate in this
setup. Everything the CA signs afterwards is CA-signed.

This matters practically: with CA-signed certificates you can replace the broker,
change its IP, or add more devices without reconfiguring anything that already
trusts the CA.

### What each side holds

```
                My Lab CA
        (ca.key signs, ca.crt distributed)
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
 broker.crt/.key         reader.crt/.key
        │                       │
  ┌─────┴──────┐         ┌──────┴─────┐
  │   BROKER   │◄─ mTLS ─┤   READER   │
  └────────────┘         └────────────┘
   own cert + key         own cert + key
   + ca.crt               + ca.crt
```

Each side presents its own certificate to prove identity, and uses `ca.crt` to
verify the other's. Symmetric — hence *mutual* TLS.

### TLS vs mutual TLS

| | Server auth only (TLS) | Mutual TLS (mTLS) |
|---|---|---|
| Broker proves identity | Yes | Yes |
| Reader proves identity | No | Yes |
| Reader needs `ca.crt` | Yes | Yes |
| Reader needs own cert + key | No | Yes |
| Who can connect | Anyone | Only certificate holders |
| Analogy | Bank website (HTTPS) | Building requiring a keycard |

Our brokers: port **8883** = TLS, port **8884** = mTLS.

---

## 2. Creating the certificates

Full script — creates a CA, a broker certificate, and a reader certificate.

```bash
mkdir -p ~/mycerts && cd ~/mycerts

# ═══════════════════════════════════════════════════════════
# STEP 1 — the Certificate Authority
# ═══════════════════════════════════════════════════════════

# 1a. CA private key. THE SECRET. Never distribute this.
openssl genrsa -out ca.key 2048

# 1b. CA certificate. Self-signed (unavoidable for a root CA).
#     PUBLIC — this is what you hand to every device.
openssl req -x509 -new -key ca.key -sha256 -days 1825 -out ca.crt \
  -subj "/C=IN/ST=KA/O=Zebra Technologies/OU=RFID Dev/CN=My Lab CA" \
  -addext "basicConstraints=critical,CA:TRUE" \
  -addext "keyUsage=critical,keyCertSign,cRLSign"

# ═══════════════════════════════════════════════════════════
# STEP 2 — broker (server) certificate
# ═══════════════════════════════════════════════════════════

# 2a. broker private key
openssl genrsa -out broker.key 2048

# 2b. SAN config — REQUIRED, see "Common mistakes"
cat > broker-san.cnf << 'EOF'
[req]
distinguished_name = dn
req_extensions = ext
prompt = no
[dn]
C  = IN
ST = KA
O  = Zebra Technologies
OU = RFID Dev
CN = 10.117.229.18
[ext]
subjectAltName = IP:10.117.229.18, DNS:pfx-broker
EOF

# 2c. certificate signing request (just a request; trusted by nothing yet)
openssl req -new -key broker.key -out broker.csr -config broker-san.cnf

# 2d. the CA signs it — this is what makes it CA-signed
openssl x509 -req -in broker.csr \
  -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out broker.crt -days 825 -sha256 \
  -extfile broker-san.cnf -extensions ext

# ═══════════════════════════════════════════════════════════
# STEP 3 — reader (client) certificate
# ═══════════════════════════════════════════════════════════

# 3a. reader private key
openssl genrsa -out reader.key 2048

# 3b. CSR — no SAN needed; clients are identified by CN
openssl req -new -key reader.key -out reader.csr \
  -subj "/C=IN/ST=KA/O=Zebra Technologies/OU=RFID Dev/CN=FXR60-READER"

# 3c. the CA signs it
openssl x509 -req -in reader.csr \
  -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out reader.crt -days 825 -sha256

# ═══════════════════════════════════════════════════════════
# VERIFY
# ═══════════════════════════════════════════════════════════
openssl verify -CAfile ca.crt broker.crt     # expect: broker.crt: OK
openssl verify -CAfile ca.crt reader.crt     # expect: reader.crt: OK
```

### Expected output

```
$ openssl x509 -in ca.crt -noout -subject -issuer
subject=... CN = My Lab CA
issuer=...  CN = My Lab CA          ← same: self-signed, correct for a CA

$ openssl x509 -in broker.crt -noout -subject -issuer
subject=... CN = 10.117.229.18
issuer=...  CN = My Lab CA          ← different: CA-signed

$ openssl x509 -in reader.crt -noout -subject -issuer
subject=... CN = FXR60-READER
issuer=...  CN = My Lab CA          ← different: CA-signed
```

### Where each file goes

| File | Secret? | Destination |
|---|---|---|
| `ca.key` | **YES** | Nowhere. Stays on the signing machine |
| `ca.crt` | No | **Both** broker and reader |
| `broker.crt` | No | Broker only |
| `broker.key` | **YES** | Broker only |
| `reader.crt` | No | Reader only |
| `reader.key` | **YES** | Reader only |

---

## 3. Installing on the broker

### Copy the files

```bash
sudo cp ca.crt     /etc/mosquitto/ca_certificates/lab-ca.crt
sudo cp broker.crt /etc/mosquitto/certs/
sudo cp broker.key /etc/mosquitto/certs/
```

### Fix ownership and permissions

Easy to skip, and it causes silent startup failures — mosquitto runs as the
`mosquitto` user and cannot read root-owned files.

```bash
sudo chown mosquitto:mosquitto \
  /etc/mosquitto/ca_certificates/lab-ca.crt \
  /etc/mosquitto/certs/broker.crt \
  /etc/mosquitto/certs/broker.key

sudo chmod 644 /etc/mosquitto/ca_certificates/lab-ca.crt   # public
sudo chmod 644 /etc/mosquitto/certs/broker.crt             # public
sudo chmod 600 /etc/mosquitto/certs/broker.key             # SECRET
```

`600` on the private key matters — `644` on a key is a real security problem.

### Reference them in the config

Server-auth only (port 8883):

```
listener 8883 0.0.0.0
cafile   /etc/mosquitto/ca_certificates/lab-ca.crt
certfile /etc/mosquitto/certs/broker.crt
keyfile  /etc/mosquitto/certs/broker.key
require_certificate false
```

Mutual TLS (port 8884):

```
listener 8884 0.0.0.0
cafile   /etc/mosquitto/ca_certificates/lab-ca.crt
certfile /etc/mosquitto/certs/broker.crt
keyfile  /etc/mosquitto/certs/broker.key
require_certificate true
use_identity_as_username true
```

| Directive | Purpose |
|---|---|
| `cafile` | CA used to **verify client** certificates |
| `certfile` | The broker's own certificate, **presented** to clients |
| `keyfile` | Private key proving the broker owns that certificate |
| `require_certificate` | `true` demands a client certificate — the only difference between TLS and mTLS |
| `use_identity_as_username` | Treats the client certificate CN as the username, so ACLs can key off certificate identity |

### Restart

```bash
sudo systemctl restart mosquitto-fxr60-tls-8883
sudo systemctl restart mosquitto-fxr60-mtls-8884
```

---

## 4. Installing on the reader

The reader needs **`ca.crt`**, **`reader.crt`**, **`reader.key`**.

Roles are mirrored from the broker's:

| File | Broker's role | Reader's role |
|---|---|---|
| `ca.crt` | verify *client* certs | verify *broker* cert |
| `broker.crt` / `.key` | own identity | — |
| `reader.crt` / `.key` | — | own identity |

### Method A — file paths (recommended first attempt)

Copy the three files to `/data/apps/` on the reader. Writes to `/data` directly
are denied on this reader; `/data/apps` is writable.

```
/data/apps/lab-ca.crt
/data/apps/fxr60-client.crt
/data/apps/fxr60-client.key
```

Then in the cloudConfig `security` block:

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

For **server-auth only** (8883), include just `CACertificateFileLocation` and omit
the private/public key fields — the reader then verifies the broker without
presenting anything itself.

Preferred as a first attempt because the validator gives clear feedback: a wrong
path returns `invalid "publicKeyFileLocation" path: File Not Found`, and a rejected
config is never applied, so the reader keeps its existing connection.

### Method B — certificate store

Bundle the certificate and key into a `.pfx`:

```bash
openssl pkcs12 -export \
  -in reader.crt -inkey reader.key -certfile ca.crt \
  -out fxr60-lab-client.pfx \
  -passout pass:'Fxr60-Client-Pfx-2026!' \
  -name "FXR60-LAB-CLIENT"
```

Serve it over HTTPS:

```bash
cd /home/altautoadmin/pfx_server
cp fxr60-lab-client.pfx files/
sudo -n env PFX_USER='altautoadmin' PFX_PASS='@1T@uT0dud3' \
  .venv/bin/python3 server.py --auth basic --port 443 &
```

Install onto the reader — `PUT https://10.117.229.9/cloud/certificates`:

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

Confirm with `get_certificates`, then reference it by name:

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

Note: only `BASIC` authentication is confirmed working for the certificate
download. `NONE`, Bearer-token headers, and mTLS on the download itself all failed
in testing — see `CERTIFICATE_AUTH_TEST_REPORT.md`.

### Status of Method B

`installedCertificateName` repeatedly failed during the AWS work with
`connection initialization failed with return code (255), retry count (0)` — a
generic error with no diagnostic detail. It later transpired the AWS failure was a
blocked port, so the mechanism may well be fine, but it has not been independently
confirmed for mTLS against our own broker. Try Method A first; if A works and B
does not, that isolates `installedCertificateName` as the problem.

---

## 5. Verifying

### The certificates themselves

```bash
# is it CA-signed? subject and issuer should DIFFER
openssl x509 -in broker.crt -noout -subject -issuer

# does the chain validate?
openssl verify -CAfile ca.crt broker.crt
openssl verify -CAfile ca.crt reader.crt

# is the SAN present? (server certs only)
openssl x509 -in broker.crt -noout -text | grep -A1 "Subject Alternative Name"

# do cert and key match? the two hashes must be identical
openssl x509 -noout -modulus -in broker.crt | openssl md5
openssl rsa  -noout -modulus -in broker.key | openssl md5
```

### The broker

```bash
cd /home/altautoadmin/pfx_server

# TLS (8883) — CA only
mosquitto_pub -h 10.117.229.18 -p 8883 --cafile ca/ca.crt -t chk -m x

# mTLS (8884) — CA plus client cert and key
mosquitto_pub -h 10.117.229.18 -p 8884 --cafile ca/ca.crt \
  --cert broker-certs/fxr60-client.crt \
  --key  broker-certs/fxr60-client.key \
  -t chk -m x

# negative test: mTLS WITHOUT a client cert must be REJECTED
mosquitto_pub -h 10.117.229.18 -p 8884 --cafile ca/ca.crt -t chk -m x
```

Silence means success. Run the negative test too — a broker that accepts
unauthenticated clients on the mTLS port is misconfigured.

### The reader

```bash
# subscribe to responses, then send a command
mosquitto_sub -h 10.117.229.18 -p 1883 -t fxr60-lab/mrsp &
mosquitto_pub -h 10.117.229.18 -p 1883 -t fxr60-lab/mcmd \
  -m '{"command":"get_status","command_id":"test-1","payload":{}}'
```

For TLS ports, add `--cafile` (and `--cert`/`--key` for mTLS).

Best diagnostic available: the reader's heartbeat events on `fxr60-lab/mevents`
carry per-interface `connectionStatus` and `connectionError`, which are far more
informative than the reader's generic error codes.

---

## 6. Common mistakes

**Missing SAN on a server certificate.** The most frequent TLS failure. Clients
check the Subject Alternative Name, not the CN, when verifying hostnames. Without
it, `verifyHostName: true` fails even though the certificate is otherwise valid.

**Forgetting `-extfile` when signing.** Extensions in a CSR are *not* copied into
the signed certificate automatically. Omit `-extfile`/`-extensions` in step 2d and
the SAN silently disappears — the certificate looks fine but hostname verification
fails. Always re-check with:

```bash
openssl x509 -in broker.crt -noout -text | grep -A1 "Subject Alternative Name"
```

**Wrong IP in the SAN.** The SAN must match the address clients actually connect
to. If the broker's IP changes, reissue the certificate.

**Key permissions.** `chmod 600` on private keys, owned by the process user.
Mosquitto silently fails to start if it cannot read its key.

**Mixing CAs.** A certificate signed by CA-A cannot be verified with CA-B's
certificate. This is why the AWS device certificate (Amazon's CA) is rejected by
our broker (lab CA) — correct behaviour, not a fault.

**Assuming a certificate problem when it is a network problem.**
`connection initialization failed with return code (255), retry count (0)` appears
for a **blocked port** just as often as for a certificate fault, with nothing to
distinguish them. Check port reachability from the reader's network segment first.
Note the reader's outbound access differs from this host's — port 8883 to AWS was
blocked from the reader while open from here.

---

## 7. What we already have

A working CA and CA-signed certificates are already in place. New ones are only
needed if you want a separate trust domain (for example, to test that the reader
correctly *rejects* certificates from an untrusted CA).

| File | Subject | Issuer | Notes |
|---|---|---|---|
| `ca/ca.crt` + `ca/ca.key` | Local RFID Test CA | itself | Valid to Aug 2031 |
| `broker-certs/broker.crt` + `.key` | `10.117.229.18` | Local RFID Test CA | SAN `IP:10.117.229.18` |
| `broker-certs/fxr60-client.crt` + `.key` | `FXR60-LAB-CLIENT` | Local RFID Test CA | For reader mTLS |
| `files/fxr60-lab-client.pfx` | — | — | Bundle for Method B, password `Fxr60-Client-Pfx-2026!` |

Installed on the broker at:

```
/etc/mosquitto/ca_certificates/lab-ca.crt
/etc/mosquitto/certs/broker.crt
/etc/mosquitto/certs/broker.key
```

Both broker certificates verify against the CA, and the mTLS listener has been
confirmed to accept a CA-signed client certificate and reject a connection without
one.

### The AWS certificate is separate

`FXR60-LAB/` holds an AWS IoT device certificate signed by **Amazon Root CA 1**, a
different CA entirely. It works with AWS IoT Core and is correctly rejected by our
lab broker. Do not mix the two sets.

---

## Related documents

| File | Contents |
|---|---|
| `BROKER_REFERENCE.md` | The four brokers: ports, services, configs, management |
| `MQTT example/` | Reader cloudConfig payloads, one per security model |
| `Aws example/` | Reader cloudConfig payloads for AWS IoT Core |
| `CERTIFICATE_AUTH_TEST_REPORT.md` | Which download auth methods work for `set_updateCertificate` |
| `MQTT_API_Findings.xlsx` | All API findings and open questions for Zebra |
