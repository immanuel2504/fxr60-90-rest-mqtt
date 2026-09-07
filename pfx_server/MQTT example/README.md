# MQTT cloudConfig examples — against our own Mosquitto broker

These payloads point the reader at a **Mosquitto broker we control** on this host
(`10.117.229.18`), rather than the broker embedded in the reader's own firmware
(`10.117.229.9:1883`). Controlling both ends lets us test each security model and
see exactly what the reader sends.

## Our broker

Mosquitto 2.0.11, installed on `10.117.229.18`. Four listeners, each a **separate
instance** — mosquitto 2.x applies `allow_anonymous` globally rather than
per-listener, so one config with mixed auth settings silently allows anonymous
access on every listener. Separate instances avoid that trap.

| Port | Security model | Managed by |
|---|---|---|
| 1883 | Plain MQTT, anonymous | systemd (`/etc/mosquitto/conf.d/fxr60-broker.conf`) |
| 1884 | Plain MQTT + username/password | `broker/auth-1884.conf` |
| 8883 | MQTT over TLS, server auth only | `broker/tls-8883.conf` |
| 8884 | MQTT over TLS + mutual TLS | `broker/mtls-8884.conf` |

### Starting / stopping

```bash
# plain 1883 (systemd)
sudo systemctl restart mosquitto
sudo systemctl status mosquitto

# the other three
cd /home/altautoadmin/pfx_server
sudo mosquitto -c "$PWD/broker/auth-1884.conf" -d
sudo mosquitto -c "$PWD/broker/tls-8883.conf"  -d
sudo mosquitto -c "$PWD/broker/mtls-8884.conf" -d

# stop a specific instance
sudo pkill -f auth-1884.conf
```

Logs: `/var/log/mosquitto/mosquitto.log`, plus `fxr60-auth.log`, `fxr60-tls.log`,
`fxr60-mtls.log` in the same directory.

### Credentials and certificates

- Broker user: `fxr60user` / `Fxr60-Mqtt-2026!` (in `/etc/mosquitto/fxr60.pwfile`)
- Broker TLS cert: `broker-certs/broker.crt` + `.key`, signed by the existing lab CA
  (`ca/ca.crt`), with `subjectAltName = IP:10.117.229.18` so `verifyHostName: true`
  passes
- Client cert for mTLS: `broker-certs/fxr60-client.crt` + `.key`, also lab-CA signed

Note the AWS device certificate (`FXR60-LAB/`) is signed by *Amazon's* CA, so our
mTLS listener correctly rejects it. mTLS testing needs the lab-CA client cert above.

### Broker verified working (all six cases)

| Test | Result |
|---|---|
| 1883 anonymous | connects |
| 1884 without credentials | correctly rejected |
| 1884 with credentials | connects |
| 8883 TLS with CA | connects |
| 8884 mTLS without client cert | correctly rejected |
| 8884 mTLS with lab-CA client cert | connects |

## The payloads

Send as `PUT https://10.117.229.9/cloud/cloudConfig` with a Bearer token, or over
MQTT wrapped as `{"command": "set_importCloudConfig", "payload": <file contents>}`.

| File | Targets | Notes |
|---|---|---|
| `01-plain-1883-no-security.json` | 1883 | Baseline. Same shape as the known-good reader config, only the host changes |
| `02-plain-1884-username-password.json` | 1884 | **Expected to fail** — see below |
| `03-tls-8883-server-auth-only.json` | 8883 | Reader verifies the broker; no client cert. Needs the lab CA on the reader |
| `04-mtls-8884-installedCertificate.json` | 8884 | mTLS via `installedCertificateName` — the method confirmed working for AWS |
| `05-mtls-8884-fileLocation.json` | 8884 | mTLS via file paths under `/data/apps/` |

### Why 02 cannot work as written

**The schema has no field for MQTT broker credentials.** The `security` object
allows only certificate-related fields, and the `options` object allows only
`additional`, `enableSecurity`, `endpoint`, `publishTopic`, `security`,
`subscribeTopic`. There is no `username`/`password` anywhere.

`basicAuthentication` appears **only in the spec's mqtt-Azure examples** and is
absent from every schema — the same example-vs-schema mismatch as
`CACertificateFileContent`, which the reader rejects. It has been removed from
file 02 to keep every payload here schema-clean, which means **02 is currently
identical to 01 apart from the port**, and will be rejected by the 1884 listener
for having no credentials.

That is itself the finding: **this API appears unable to configure a
password-protected MQTT broker.** Plain MQTT with password auth is a common setup,
so this is worth raising with Zebra. If you want to confirm it hands-on, add
`basicAuthentication: {"username": "fxr60user", "password": "Fxr60-Mqtt-2026!"}`
inside `options` and expect an `invalid ... JSON object` schema rejection.

### A schema asymmetry worth knowing

`additionalOptions` (the `retention` block) is valid **only on `data.event`
connections**. It is not in the schema for `management.event`,
`control.commandResponse`, or `management.commandResponse` — even though retention
would seem to apply equally to management events. All files here reflect this:
retention appears on `data.event` only.

Similarly, `enableLocalRest` is valid only on the two `commandResponse` channels,
not on `event` channels.

### Files needed on the reader

`03` and `05` reference files under `/data/apps/` (writes to `/data` directly are
denied on this reader):

```
/data/apps/lab-ca.crt          <- ca/ca.crt
/data/apps/fxr60-client.key    <- broker-certs/fxr60-client.key   (05 only)
/data/apps/fxr60-client.crt    <- broker-certs/fxr60-client.crt   (05 only)
```

If missing, the config is rejected with `File Not Found` — harmless, since a
rejected config is never applied.

For `04`, install the client cert into the reader's certificate store first via
`set_updateCertificate` under the name `FXR60-LAB-CLIENT`, and confirm with
`get_certificates`.

## Suggested order

Run `01` first. It only changes the broker host, so if it works you have a clean
baseline and know the reader can reach our broker at all. Then work up through TLS
and mTLS.

## If the reader goes unreachable

A config that is accepted but cannot connect drops the reader off both the new
broker and the old one. Restore with
`../mqtt/verified/rollback_local_mqtt_fxr60.json` via the reader's local web UI
(reachable thanks to `enableLocalRest: true`) or Postman.

Also worth remembering from the AWS work: a **blocked port** produces
`connection initialization failed with return code (255), retry count (0)` — the
same generic error as a certificate failure. If a config looks correct but won't
connect, check port reachability from the reader's network before suspecting certs.
