# FXR60 Lab MQTT Broker Reference

Four Mosquitto brokers on this host, one per security model, for testing how the
FXR60 reader connects under each. All four are systemd-managed and **start
automatically on boot**.

- **Host:** `10.117.229.18` (this machine)
- **Software:** Mosquitto 2.0.11
- **Bind:** `0.0.0.0` on all listeners (reachable across the network)

The reader also has its *own* built-in broker at `10.117.229.9:1883` — that is a
different broker, not one of these.

---

## Also always-on: the PFX file server

| Service | Port | Purpose |
|---|---|---|
| `pfx-file-server` | 443 | Serves `.pfx`/certificate files over HTTPS with Basic auth, for `set_updateCertificate` downloads |

```bash
systemctl status pfx-file-server
sudo systemctl restart pfx-file-server
```

- Serves from `/home/altautoadmin/pfx_server/files/` — drop a file in, no restart needed
- Credentials: `altautoadmin` / `@1T@uT0dud3`, held in `/etc/pfx-server.env` (root-only, `chmod 600`)
- Unit: `/etc/systemd/system/pfx-file-server.service`

---

## Quick reference

| Port | Security model | Client needs | systemd service |
|---|---|---|---|
| **1883** | Plain MQTT, anonymous | nothing | `mosquitto` |
| **1884** | Plain MQTT + username/password | credentials | `mosquitto-fxr60-auth-1884` |
| **8883** | MQTT over TLS, server auth only | CA cert | `mosquitto-fxr60-tls-8883` |
| **8884** | MQTT over TLS + mutual TLS | CA cert + client cert/key | `mosquitto-fxr60-mtls-8884` |

**Credentials (port 1884):** `fxr60user` / `Fxr60-Mqtt-2026!`

---

## Managing the brokers

```bash
# status of all four
systemctl status mosquitto mosquitto-fxr60-auth-1884 \
                 mosquitto-fxr60-tls-8883 mosquitto-fxr60-mtls-8884

# one-line summary
for s in mosquitto mosquitto-fxr60-auth-1884 mosquitto-fxr60-tls-8883 mosquitto-fxr60-mtls-8884; do
  printf "%-34s %s\n" "$s" "$(systemctl is-active $s)"
done

# restart / stop / start any one
sudo systemctl restart mosquitto-fxr60-tls-8883
sudo systemctl stop    mosquitto-fxr60-mtls-8884
sudo systemctl start   mosquitto-fxr60-auth-1884

# confirm they will come back after a reboot
systemctl is-enabled mosquitto mosquitto-fxr60-auth-1884 \
                     mosquitto-fxr60-tls-8883 mosquitto-fxr60-mtls-8884
```

### Verify all four are working

```bash
cd /home/altautoadmin/pfx_server
H=10.117.229.18
mosquitto_pub -h $H -p 1883 -t chk -m x                                    # plain
mosquitto_pub -h $H -p 1884 -u fxr60user -P 'Fxr60-Mqtt-2026!' -t chk -m x  # auth
mosquitto_pub -h $H -p 8883 --cafile ca/ca.crt -t chk -m x                 # TLS
mosquitto_pub -h $H -p 8884 --cafile ca/ca.crt \
  --cert broker-certs/fxr60-client.crt --key broker-certs/fxr60-client.key \
  -t chk -m x                                                             # mTLS
```

Silence means success. Also worth confirming the negative cases still hold —
1884 without credentials and 8884 without a client cert should both be **rejected**.

### Watch traffic live

```bash
# everything hitting the plain broker
mosquitto_sub -h 10.117.229.18 -p 1883 -t '#' -v

# just the reader's heartbeat events
mosquitto_sub -h 10.117.229.18 -p 1883 -t 'fxr60-lab/mevents'
```

---

## Broker 1 — Plain MQTT, port 1883

Anonymous access, no encryption. Mirrors the reader's own built-in broker, so it is
the cleanest baseline: if the reader connects here, networking is fine and any later
failure is about security configuration.

- **Service:** `mosquitto` (the distro's default unit)
- **Config:** `/etc/mosquitto/conf.d/fxr60-broker.conf`
- **Log:** `/var/log/mosquitto/mosquitto.log`

```
listener 1883 0.0.0.0
protocol mqtt
allow_anonymous true
log_type all
```

**Reader config:** `MQTT example/01-plain-1883-no-security.json` — **confirmed working**
(see `MQTT example/01-RESULT-verified.md`).

---

## Broker 2 — Username/password, port 1884

Requires credentials; no encryption. Note the credentials cross the network in
clear text — fine for a lab, not for production.

- **Service:** `mosquitto-fxr60-auth-1884`
- **Config:** `broker/auth-1884.conf`
- **Password file:** `/etc/mosquitto/fxr60.pwfile`
- **Log:** `/var/log/mosquitto/fxr60-auth.log`

```
listener 1884 0.0.0.0
protocol mqtt
allow_anonymous false
password_file /etc/mosquitto/fxr60.pwfile
```

### Managing users

```bash
# add or change a user (omit -c to add to an existing file)
sudo mosquitto_passwd -b /etc/mosquitto/fxr60.pwfile <user> '<password>'
sudo systemctl restart mosquitto-fxr60-auth-1884

# delete a user
sudo mosquitto_passwd -D /etc/mosquitto/fxr60.pwfile <user>
sudo systemctl restart mosquitto-fxr60-auth-1884
```

### Reader-side status: unresolved

The reader's `get_config` output contains a `basicAuthentication` block with
`username`/`password` inside `options.additional`, so the **firmware does support
broker credentials**. But:

- `basicAuthentication` is **absent from every schema** in `FXR_60-90_rest_api.yaml`
- The one example that shows it (`mqtt-Azure`) places it inside `options`, not
  inside `options.additional` where the reader actually reports it

Sending it inside `options` (per the spec) is rejected as an invalid object.
Sending it inside `additional` (per the reader's own output) was not confirmed
working either. Treat this as an open question for Zebra — the field exists in
firmware and in the web UI ("BASIC Authentication" checkbox), but the documented
API surface cannot reliably reach it.

---

## Broker 3 — TLS, server authentication only, port 8883

Encrypted. The reader verifies the broker's certificate; the broker does not ask
the reader for one.

- **Service:** `mosquitto-fxr60-tls-8883`
- **Config:** `broker/tls-8883.conf`
- **Log:** `/var/log/mosquitto/fxr60-tls.log`

```
listener 8883 0.0.0.0
protocol mqtt
allow_anonymous true
cafile   /etc/mosquitto/ca_certificates/lab-ca.crt
certfile /etc/mosquitto/certs/broker.crt
keyfile  /etc/mosquitto/certs/broker.key
require_certificate false
```

**The reader needs the CA certificate** to validate the broker — copy `ca/ca.crt`
to `/data/apps/lab-ca.crt` on the reader (writes to `/data` directly are denied).

**Reader config:** `MQTT example/03-tls-8883-server-auth-only.json`

---

## Broker 4 — Mutual TLS, port 8884

Encrypted, and the reader must present its own certificate signed by the lab CA.
Strongest of the four.

- **Service:** `mosquitto-fxr60-mtls-8884`
- **Config:** `broker/mtls-8884.conf`
- **Log:** `/var/log/mosquitto/fxr60-mtls.log`

```
listener 8884 0.0.0.0
protocol mqtt
allow_anonymous true
cafile   /etc/mosquitto/ca_certificates/lab-ca.crt
certfile /etc/mosquitto/certs/broker.crt
keyfile  /etc/mosquitto/certs/broker.key
require_certificate true
use_identity_as_username true
```

`use_identity_as_username` makes the broker treat the client certificate's CN as
the username, so ACLs can be written against certificate identity.

**Reader configs:** two ways to supply the client certificate —
- `MQTT example/04-mtls-8884-installedCertificate.json` — via `installedCertificateName`
- `MQTT example/05-mtls-8884-fileLocation.json` — via file paths under `/data/apps/`

---

## Certificates

All issued by the existing lab CA at `ca/ca.crt` (key: `ca/ca.key`).

| Purpose | Location | Notes |
|---|---|---|
| CA certificate | `ca/ca.crt` | Give to any client that must validate the broker |
| Broker server cert | `broker-certs/broker.crt` + `.key` | `subjectAltName = IP:10.117.229.18` |
| Client cert (for mTLS) | `broker-certs/fxr60-client.crt` + `.key` | CN = `FXR60-LAB-CLIENT` |

Installed copies used by the brokers live at:
```
/etc/mosquitto/ca_certificates/lab-ca.crt
/etc/mosquitto/certs/broker.crt
/etc/mosquitto/certs/broker.key
```

The broker certificate carries `IP:10.117.229.18` in its SAN, which is what allows
the reader's `verifyHostName: true` to pass. If the broker's IP ever changes, the
certificate must be reissued or hostname verification will fail.

### Reissuing the broker certificate

```bash
cd /home/altautoadmin/pfx_server/broker-certs
openssl genrsa -out broker.key 2048
openssl req -new -key broker.key -out broker.csr -config broker-san.cnf
openssl x509 -req -in broker.csr -CA ../ca/ca.crt -CAkey ../ca/ca.key \
  -CAcreateserial -out broker.crt -days 825 -sha256 \
  -extfile broker-san.cnf -extensions ext
sudo cp broker.crt broker.key /etc/mosquitto/certs/
sudo chown mosquitto:mosquitto /etc/mosquitto/certs/broker.*
sudo chmod 600 /etc/mosquitto/certs/broker.key
sudo systemctl restart mosquitto-fxr60-tls-8883 mosquitto-fxr60-mtls-8884
```

Edit the `subjectAltName` line in `broker-san.cnf` first if the IP has changed.

### A note on the AWS certificate

The AWS device certificate in `FXR60-LAB/` is signed by **Amazon's** CA, not the lab
CA, so broker 8884 correctly rejects it. mTLS testing needs the lab-CA client cert
above. This is expected behaviour, not a fault.

---

## Reader topics

Same topic names as the reader's own broker, so tooling works unchanged:

| Channel | Reader publishes to | Reader subscribes to |
|---|---|---|
| Control | `fxr60-lab/rsp` | `fxr60-lab/cmd` |
| Management cmd/rsp | `fxr60-lab/mrsp` | `fxr60-lab/mcmd` |
| Management events | `fxr60-lab/mevents` | — |
| Tag data | `fxr60-lab/tevents` | — |

Client IDs: `fxr60-lab-ctrl`, `fxr60-lab-mcmd`, `fxr60-lab-mevents`, `fxr60-lab-data`.

Send a command by publishing to the `mcmd` topic and listening on `mrsp`:

```bash
mosquitto_sub -h 10.117.229.18 -p 1883 -t fxr60-lab/mrsp &
mosquitto_pub -h 10.117.229.18 -p 1883 -t fxr60-lab/mcmd \
  -m '{"command":"get_status","command_id":"test-1","payload":{}}'
```

---

## Troubleshooting

**Reader shows connected but nothing arrives.** Check the broker log for the
reader's client IDs. If they are absent, the reader is connected somewhere else —
its own broker, or AWS.

```bash
sudo grep -E "fxr60-lab-(ctrl|data|mcmd|mevents)" /var/log/mosquitto/mosquitto.log | tail
```

**Reader is unreachable everywhere.** A config that is accepted but cannot connect
drops the reader off both the new broker and the old one. Recover with
`mqtt/verified/rollback_local_mqtt_fxr60.json` (back to the reader's own broker) or
`MQTT example/01-plain-1883-no-security.json` (onto this host's plain broker), applied
through the reader's local web UI — reachable thanks to `enableLocalRest: true` — or
via Postman.

**`connection initialization failed with return code (255), retry count (0)`.**
Learned during the AWS work: this generic error appears for a **blocked port** as
well as for certificate problems, and gives no hint which. Check port reachability
from the reader's network segment before suspecting certificates. Note the reader's
outbound access differs from this host's — port 8883 to AWS was blocked from the
reader while open from here.

**Best diagnostic available.** The reader's heartbeat events carry per-interface
`connectionStatus` and `connectionError`, which are far more informative than the
generic error codes. If any one channel still reaches a working broker, subscribe to
its management-events topic to find out why the others are failing.

---

## Mosquitto 2.x gotcha worth remembering

`allow_anonymous` and `password_file` are effectively **global**, not per-listener.
A single config file with several listeners and mixed auth settings silently applies
the last-seen value everywhere — during setup, a combined config allowed anonymous
access on the password-protected listener. That is why these run as four separate
instances with one security model each.

---

## Files

```
BROKER_REFERENCE.md                  this file
broker/auth-1884.conf                username/password broker config
broker/tls-8883.conf                 TLS broker config
broker/mtls-8884.conf                mutual-TLS broker config
broker-certs/                        broker + client certs, and broker-san.cnf
ca/ca.crt, ca/ca.key                 the lab CA
MQTT example/                        reader cloudConfig payloads, one per model
Aws example/                         reader cloudConfig payloads for AWS IoT Core
mqtt/verified/rollback_local_mqtt_fxr60.json   recovery config

/etc/systemd/system/mosquitto-fxr60-auth-1884.service
/etc/systemd/system/mosquitto-fxr60-tls-8883.service
/etc/systemd/system/mosquitto-fxr60-mtls-8884.service
/etc/mosquitto/conf.d/fxr60-broker.conf        the 1883 listener
/etc/mosquitto/fxr60.pwfile                    password file for 1884
```
