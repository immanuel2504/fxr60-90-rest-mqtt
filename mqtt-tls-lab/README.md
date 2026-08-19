# MQTT TLS lab

A self-contained TLS MQTT setup for testing FXR60/FXR90 reader connections:
private CA, broker certificate, client certificate, a TLS broker, a subscriber,
and a publisher that emits FXR-shaped tag events.

Everything here was run and verified on 2026-08-14 against this PC
(`10.117.129.205`) — see [Verified results](#verified-results).

```
mqtt-tls-lab/
  gen_certs.py             creates the CA, broker, and client certificates
  broker.py                TLS MQTT 3.1.1 broker, mutual auth, stdlib only
  listener.py              subscriber over TLS (paho)
  fake_reader.py           publisher over TLS (paho), FXR tag-event payloads
  reader_config_tls.json   endpoint config to point a real reader here
  requirements.txt         paho-mqtt (broker needs nothing)
  certs/                   generated key material — do not commit
```

## Setup

```powershell
py -3 -m pip install -r requirements.txt
py -3 gen_certs.py
```

`gen_certs.py` auto-detects the LAN IP that faces the reader and puts it in the
broker certificate's SAN, alongside `127.0.0.1` and `localhost`. That matters:
a broker certificate whose SAN is only `127.0.0.1` cannot be validated by
anything off this PC, so a reader with `verifyHostName: true` fails the
handshake. Override with `--san-ip` if the reader reaches you by another address.

Files produced in `certs/`:

| File | Role |
|---|---|
| `ca.key` | CA private key — signs everything, keep secret |
| `ca.crt`, `ca.pem` | CA certificate (identical content, two names) |
| `server.key`, `server.crt` | broker identity, SAN = LAN IP + 127.0.0.1 + localhost |
| `client.key`, `client.crt`, `client.pem` | client/reader identity |
| `san.ext`, `client.ext`, `*.csr`, `ca.srl` | signing inputs and bookkeeping |

`client.pem` is a copy of `client.crt` because the FXR field
`publicKeyFileLocation` expects a `.pem` name.

## Run

Three terminals. Broker first:

```powershell
py -3 broker.py                  # 0.0.0.0:8883, client certificate REQUIRED
py -3 broker.py --host 127.0.0.1 # local only
py -3 broker.py -v               # log control packets too
```

Then the listener:

```powershell
py -3 listener.py
py -3 listener.py --host 10.117.129.205 --topic 'site/dock01/#'
```

Then the publisher:

```powershell
py -3 fake_reader.py --count 5
```

The broker logs the CN from each client's certificate on connect, so you can see
exactly which identity connected — useful once a real reader joins.

## Verified results

| Case | Command | Result |
|---|---|---|
| Local end to end | broker + listener + fake_reader on 127.0.0.1 | 5 published, 5 received, 5 confirmed |
| Over the LAN | `--host 10.117.129.205` | 2 published, 2 received — SAN validates |
| No client certificate | `fake_reader.py --no-cert` | rejected, `PEER_DID_NOT_RETURN_A_CERTIFICATE` |
| Certificate from another CA | `fake_reader.py --certs <rogue>` | rejected, `CERTIFICATE_VERIFY_FAILED` |
| No cert, anonymous broker | `broker.py --allow-anonymous` | accepted, logged as `anonymous` |
| Two brokers, one port | `broker.py` twice | second exits with WinError 10048 |

`--allow-anonymous` is the broker-side equivalent of `verifyPeer: false` in a
reader config: it proves a handshake problem is about client identity rather
than about reachability or the CA.

## Pointing a real reader at this broker

Prerequisites on this PC:

1. Broker bound to `0.0.0.0` (the default), not `127.0.0.1`.
2. Windows Firewall allowing inbound TCP 8883:
   ```powershell
   New-NetFirewallRule -DisplayName "MQTT TLS lab 8883" -Direction Inbound `
     -Protocol TCP -LocalPort 8883 -Action Allow
   ```
3. `hostName` in the reader config matching a SAN entry — `10.117.129.205`.

Then send [reader_config_tls.json](reader_config_tls.json) with
`PUT /cloud/config`:

```bash
READER=10.233.46.162
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)
curl -sk -X PUT "https://$READER/cloud/config" \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d @reader_config_tls.json
```

### The open blocker

The reader must trust `ZebraRootCA`, and `config.security` accepts only a file
path (`CACertificateFileLocation`) or an installed-certificate name
(`installedCertificateName`) — there is no inline-PEM field anywhere in the
spec. On the FXR60 tested here (readerApplication 5.0.1, cloudAgent 0.6.2.64),
`/cloud/caCertificates` returns **404 "not a valid URI"** for GET, PUT, and
DELETE, so the CA cannot be installed over REST. Two ways forward, both needing
confirmation from firmware:

1. Place `ca.pem`, `client.key`, and `client.pem` under `/data/apps/certs/` — the
   user-app area, so they travel with an installed app.
2. Set `verifyPeer: false` and `verifyHostName: false` and skip validation. Works
   for a lab, unacceptable for production, and it is what
   `Selected/Fixed reader Certificate/` does.

Until one is settled, the lab is exercised with `fake_reader.py` standing in for
the reader.

## Notes

- `broker.py` implements CONNECT, SUBSCRIBE, UNSUBSCRIBE, PUBLISH (QoS 0/1 with
  PUBACK), retained messages, PINGREQ, DISCONNECT, and `+`/`#` wildcards. Not
  implemented: QoS 2, will messages, persistent sessions, password auth
  (identity comes from the certificate).
- Certificates last 365 days; the CA lasts 10 years. `gen_certs.py --force`
  regenerates, which invalidates anything already deployed from the old CA.
- Do not commit `certs/` — it holds three private keys.
