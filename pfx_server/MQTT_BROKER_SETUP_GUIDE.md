# How to Create an MQTT Broker

Building a Mosquitto MQTT broker from scratch, with four security models: plain,
username/password, TLS, and mutual TLS. Written from the working setup on this
host (`10.117.229.18`), so every command here has been run and verified.

---

## Contents

1. [What a broker is](#1-what-a-broker-is)
2. [Install](#2-install)
3. [Broker 1 — plain MQTT](#3-broker-1--plain-mqtt-port-1883)
4. [Broker 2 — username/password](#4-broker-2--usernamepassword-port-1884)
5. [Broker 3 — TLS](#5-broker-3--tls-port-8883)
6. [Broker 4 — mutual TLS](#6-broker-4--mutual-tls-port-8884)
7. [Running multiple brokers](#7-running-multiple-brokers)
8. [Auto-start on boot](#8-auto-start-on-boot)
9. [Testing](#9-testing)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. What a broker is

MQTT is publish/subscribe. Clients never talk to each other directly — they all
connect to a **broker**, which routes messages by topic.

```
   READER ──publish──►  ┌────────┐  ──deliver──►  SUBSCRIBER A
                        │ BROKER │
   TOOL   ──publish──►  └────────┘  ──deliver──►  SUBSCRIBER B
```

A publisher doesn't know or care who is subscribed. A subscriber doesn't know who
published. The broker decouples them.

In our setup the FXR60 reader publishes tag data and heartbeats, and subscribes to
a command topic. Our tooling does the reverse.

**Note:** the reader has its *own* built-in broker at `10.117.229.9:1883`. Running
our own broker on `10.117.229.18` gives us control over authentication, TLS, and
logging — which is what makes it possible to test each security model and see
exactly what the reader sends.

---

## 2. Install

```bash
sudo apt-get update
sudo apt-get install -y mosquitto mosquitto-clients
```

- `mosquitto` — the broker daemon
- `mosquitto-clients` — `mosquitto_pub` and `mosquitto_sub` for testing

Verify:

```bash
mosquitto -h | head -2          # expect: mosquitto version 2.0.11
systemctl is-active mosquitto   # expect: active
```

### First surprise: it is localhost-only by default

Mosquitto 2.x binds to `127.0.0.1` unless told otherwise. Check:

```bash
ss -tlnp | grep 1883
# LISTEN 127.0.0.1:1883   ← only this machine can connect
```

Nothing on the network can reach it yet. Fixing that is the first config change.

---

## 3. Broker 1 — plain MQTT (port 1883)

No encryption, no authentication. Useful as a baseline: if a client connects here,
networking is fine and any later failure is about security configuration.

Create `/etc/mosquitto/conf.d/mybroker.conf`:

```
listener 1883 0.0.0.0
protocol mqtt
allow_anonymous true
log_type all
```

| Directive | Meaning |
|---|---|
| `listener 1883 0.0.0.0` | Listen on port 1883, **all** interfaces (not just localhost) |
| `protocol mqtt` | Plain MQTT (as opposed to `websockets`) |
| `allow_anonymous true` | No credentials required |
| `log_type all` | Verbose logging — invaluable when debugging |

Files in `/etc/mosquitto/conf.d/` are included automatically by the shipped
`mosquitto.conf`, so the distro's own file stays untouched.

```bash
sudo systemctl restart mosquitto
ss -tlnp | grep 1883        # expect 0.0.0.0:1883 now
```

Test:

```bash
mosquitto_sub -h 10.117.229.18 -p 1883 -t 'test/#' -v &
mosquitto_pub -h 10.117.229.18 -p 1883 -t test/hello -m "it works"
```

---

## 4. Broker 2 — username/password (port 1884)

Credentials required, still unencrypted — so the password crosses the network in
clear text. Fine for a lab, not for production. Use TLS if credentials matter.

### Create the password file

```bash
sudo mosquitto_passwd -c -b /etc/mosquitto/mybroker.pwfile myuser 'MyPassword123!'
sudo chown mosquitto:mosquitto /etc/mosquitto/mybroker.pwfile
sudo chmod 600 /etc/mosquitto/mybroker.pwfile
```

`-c` creates a new file (**overwrites** any existing one — omit it to add users).
`-b` supplies the password on the command line.

Managing users afterwards:

```bash
# add or change a user
sudo mosquitto_passwd -b /etc/mosquitto/mybroker.pwfile newuser 'Password456!'

# delete a user
sudo mosquitto_passwd -D /etc/mosquitto/mybroker.pwfile olduser

# restart to pick up changes
sudo systemctl restart mosquitto-auth-1884
```

### Config

```
listener 1884 0.0.0.0
protocol mqtt
allow_anonymous false
password_file /etc/mosquitto/mybroker.pwfile
log_dest file /var/log/mosquitto/auth.log
log_type all
```

Test — and check the negative case, which is the one that actually matters:

```bash
# with credentials: should succeed
mosquitto_pub -h 10.117.229.18 -p 1884 -u myuser -P 'MyPassword123!' -t test -m x

# without credentials: MUST be rejected
mosquitto_pub -h 10.117.229.18 -p 1884 -t test -m x
# expect: Connection Refused: not authorised.
```

---

## 5. Broker 3 — TLS (port 8883)

Encrypted. The broker proves its identity with a certificate; clients are not
asked for one.

### You need certificates first

Three files — see `CERTIFICATE_GUIDE.md` for how to create them:

- `ca.crt` — the CA certificate
- `broker.crt` — the broker's certificate, **signed by the CA**, with the broker's
  IP in its Subject Alternative Name
- `broker.key` — the broker's private key

### Install them

```bash
sudo cp ca.crt     /etc/mosquitto/ca_certificates/lab-ca.crt
sudo cp broker.crt /etc/mosquitto/certs/
sudo cp broker.key /etc/mosquitto/certs/

sudo chown mosquitto:mosquitto \
  /etc/mosquitto/ca_certificates/lab-ca.crt \
  /etc/mosquitto/certs/broker.crt \
  /etc/mosquitto/certs/broker.key

sudo chmod 644 /etc/mosquitto/ca_certificates/lab-ca.crt
sudo chmod 644 /etc/mosquitto/certs/broker.crt
sudo chmod 600 /etc/mosquitto/certs/broker.key     # SECRET
```

The `600` on the key matters. Mosquitto also **silently fails to start** if it
cannot read its own key — so the `chown` is not optional.

### Config

```
listener 8883 0.0.0.0
protocol mqtt
allow_anonymous true
cafile   /etc/mosquitto/ca_certificates/lab-ca.crt
certfile /etc/mosquitto/certs/broker.crt
keyfile  /etc/mosquitto/certs/broker.key
require_certificate false
log_dest file /var/log/mosquitto/tls.log
log_type all
```

| Directive | Purpose |
|---|---|
| `cafile` | CA used to verify client certificates (unused when `require_certificate false`, but must be present) |
| `certfile` | The broker's own certificate, presented to clients |
| `keyfile` | Private key proving the broker owns that certificate |
| `require_certificate false` | Do **not** demand a client certificate — this is what makes it server-auth only |

Test — the client needs the CA to verify the broker:

```bash
mosquitto_pub -h 10.117.229.18 -p 8883 --cafile ca/ca.crt -t test -m x
```

---

## 6. Broker 4 — mutual TLS (port 8884)

Encrypted, and clients must present their own CA-signed certificate. Only holders
of a valid certificate can connect.

### Config

```
listener 8884 0.0.0.0
protocol mqtt
allow_anonymous true
cafile   /etc/mosquitto/ca_certificates/lab-ca.crt
certfile /etc/mosquitto/certs/broker.crt
keyfile  /etc/mosquitto/certs/broker.key
require_certificate true
use_identity_as_username true
log_dest file /var/log/mosquitto/mtls.log
log_type all
```

Only two lines differ from the TLS config:

| Directive | Effect |
|---|---|
| `require_certificate true` | Demand a client certificate. **This single line is the difference between TLS and mTLS** |
| `use_identity_as_username true` | Treat the client certificate's CN as the username, so ACLs can key off certificate identity |

Here `cafile` does real work — it's what the broker uses to verify client
certificates.

Test:

```bash
# with a CA-signed client certificate: should succeed
mosquitto_pub -h 10.117.229.18 -p 8884 --cafile ca/ca.crt \
  --cert client.crt --key client.key -t test -m x

# without a client certificate: MUST be rejected
mosquitto_pub -h 10.117.229.18 -p 8884 --cafile ca/ca.crt -t test -m x
# expect: Error: The connection was lost.
```

---

## 7. Running multiple brokers

### The Mosquitto 2.x trap

It is tempting to put all four listeners in one config file. **This does not work
as expected.** `allow_anonymous` and `password_file` behave as **global** settings,
not per-listener — the last value seen applies everywhere.

A combined config like this:

```
listener 1883
allow_anonymous true          ← wins globally

listener 1884
allow_anonymous false         ← silently ineffective
password_file /etc/mosquitto/mybroker.pwfile
```

...leaves port 1884 accepting anonymous connections. This happened during our
setup and was only caught by running the negative test — the broker started
cleanly and logged no warning.

### The fix: one instance per security model

Separate config files, separate processes:

```bash
mkdir -p ~/broker
# ~/broker/auth-1884.conf   — username/password
# ~/broker/tls-8883.conf    — TLS
# ~/broker/mtls-8884.conf   — mutual TLS

sudo mosquitto -c ~/broker/auth-1884.conf -d
sudo mosquitto -c ~/broker/tls-8883.conf  -d
sudo mosquitto -c ~/broker/mtls-8884.conf -d
```

`-d` daemonises. Keep port 1883 under the distro's `mosquitto` service.

**Always run the negative tests** after any change to a multi-broker setup.

---

## 8. Auto-start on boot

Manually started daemons vanish on reboot. Give each a systemd unit.

`/etc/systemd/system/mosquitto-tls-8883.service`:

```ini
[Unit]
Description=MQTT broker - TLS (8883)
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=mosquitto
Group=mosquitto
ExecStart=/usr/sbin/mosquitto -c /home/altautoadmin/pfx_server/broker/tls-8883.conf
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Note: no `-d` flag. systemd manages the process, so it must stay in the
foreground — `Type=simple` expects that. `Restart=always` brings it back if it
crashes.

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now mosquitto-tls-8883
systemctl is-enabled mosquitto-tls-8883    # expect: enabled
```

Repeat per broker. Verify the whole set:

```bash
for s in mosquitto mosquitto-auth-1884 mosquitto-tls-8883 mosquitto-mtls-8884; do
  printf "%-30s active=%-8s enabled=%s\n" "$s" \
    "$(systemctl is-active $s)" "$(systemctl is-enabled $s 2>/dev/null)"
done
```

Then actually test a restart — `enabled` alone does not prove the config is
loadable.

---

## 9. Testing

### Subscribe and publish

```bash
# watch everything ('#' is the multi-level wildcard)
mosquitto_sub -h 10.117.229.18 -p 1883 -t '#' -v

# watch one topic
mosquitto_sub -h 10.117.229.18 -p 1883 -t 'fxr60-lab/mevents'

# publish
mosquitto_pub -h 10.117.229.18 -p 1883 -t test/topic -m "hello"
```

`-v` prints the topic alongside the payload, which is what you want with wildcards.

### Test all four at once

```bash
H=10.117.229.18
mosquitto_pub -h $H -p 1883 -t chk -m x && echo "1883 OK"
mosquitto_pub -h $H -p 1884 -u myuser -P 'MyPassword123!' -t chk -m x && echo "1884 OK"
mosquitto_pub -h $H -p 8883 --cafile ca/ca.crt -t chk -m x && echo "8883 OK"
mosquitto_pub -h $H -p 8884 --cafile ca/ca.crt \
  --cert client.crt --key client.key -t chk -m x && echo "8884 OK"
```

Silence from `mosquitto_pub` means success.

### Do not skip the negative tests

```bash
# 1884 without credentials — must FAIL
mosquitto_pub -h $H -p 1884 -t chk -m x

# 8884 without a client certificate — must FAIL
mosquitto_pub -h $H -p 8884 --cafile ca/ca.crt -t chk -m x
```

A positive test passing tells you the broker works. Only the negative test tells
you it is actually *secure*.

### Watch the logs

```bash
sudo tail -f /var/log/mosquitto/mosquitto.log
sudo grep -E "New client connected" /var/log/mosquitto/mosquitto.log | tail
```

---

## 10. Troubleshooting

**Cannot connect from another machine.** Almost always the localhost default.
Check `ss -tlnp | grep 1883` — if it shows `127.0.0.1`, add `0.0.0.0` to the
`listener` line. Then check the firewall.

**Broker will not start after adding TLS.** Usually a certificate the `mosquitto`
user cannot read:

```bash
sudo journalctl -u mosquitto-tls-8883 -n 30
sudo -u mosquitto cat /etc/mosquitto/certs/broker.key > /dev/null && echo readable
```

**TLS connects but hostname verification fails.** The certificate's Subject
Alternative Name does not match the address being connected to:

```bash
openssl x509 -in broker.crt -noout -text | grep -A1 "Subject Alternative Name"
```

The SAN must contain the broker's actual IP or hostname. Missing or wrong SAN is
the single most common TLS failure.

**mTLS rejects a valid-looking certificate.** It is probably signed by a different
CA than the broker's `cafile`:

```bash
openssl verify -CAfile /etc/mosquitto/ca_certificates/lab-ca.crt client.crt
```

`unable to get local issuer certificate` means wrong CA. This is why the AWS device
certificate (Amazon's CA) is correctly rejected by our lab broker.

**Auth appears configured but anonymous clients get in.** The Mosquitto 2.x global
`allow_anonymous` trap — see section 7. Split into separate instances.

**Client connects then immediately disconnects.** Often a duplicate client ID: MQTT
requires unique IDs, and a second client using the same one evicts the first. Watch
for a connect/disconnect loop in the log.

**Inspect a live TLS handshake:**

```bash
openssl s_client -connect 10.117.229.18:8883 -CAfile ca/ca.crt
openssl s_client -connect 10.117.229.18:8884 -CAfile ca/ca.crt \
  -cert client.crt -key client.key
```

More informative than most client error messages — it shows the certificate chain
and the exact verification result.

---

## Our actual setup

Four brokers on `10.117.229.18`, all systemd-managed and enabled at boot:

| Port | Model | Service | Config |
|---|---|---|---|
| 1883 | Plain | `mosquitto` | `/etc/mosquitto/conf.d/fxr60-broker.conf` |
| 1884 | User/password | `mosquitto-fxr60-auth-1884` | `broker/auth-1884.conf` |
| 8883 | TLS | `mosquitto-fxr60-tls-8883` | `broker/tls-8883.conf` |
| 8884 | Mutual TLS | `mosquitto-fxr60-mtls-8884` | `broker/mtls-8884.conf` |

Credentials for 1884: `fxr60user` / `Fxr60-Mqtt-2026!`

See `BROKER_REFERENCE.md` for full operational detail.

---

## Related documents

| File | Contents |
|---|---|
| `BROKER_REFERENCE.md` | Operating our four brokers day to day |
| `CERTIFICATE_GUIDE.md` | Creating CA-signed certificates and installing them |
| `MQTT example/` | Reader cloudConfig payloads, one per security model |
| `MQTT example/01-RESULT-verified.md` | Confirmed-working plain-MQTT result |
