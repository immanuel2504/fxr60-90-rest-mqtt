# Receivers for the reader's non-MQTT connection types

`PUT /cloud/cloudConfig` documents six connection types. Three of them —
`httpPost`, `WEBSOCKET`, `tcpip-server` — need something on the other end to
receive tag data. These are those receivers.

| Type | Receiver | Port | Service | Status |
|---|---|---|---|---|
| `httpPost` | `http_post_receiver.py` | 9443 (HTTPS) | `fxr60-recv-http-post` | ✅ running, verified |
| `WEBSOCKET` | `websocket_receiver.py` | 9444 (wss) | `fxr60-recv-websocket` | ✅ running, verified |
| `tcpip-server` | `tcpip_client.py` | 8081 | manual — see below | ✅ tested |

TLS uses the same lab CA chain as the brokers (`broker-certs/broker.crt` and
`.key`), so the reader can verify these receivers with `/data/apps/lab-ca.crt` —
the same CA file it already uses for the MQTT brokers.

---

## Read this before configuring the reader

The spec's examples for two of these types **use fields its own schema does not
define.** This is the same defect already confirmed twice on this API — with
`CACertificateFileContent` and with `basicAuthentication` — and in both of those
cases the reader's validator rejected the payload.

The schema for `data.event.options` allows exactly six fields:

```
additional  enableSecurity  endpoint  publishTopic  security  subscribeTopic
```

Measured against that:

| Spec example | Fields it uses that are **not** in the schema |
|---|---|
| `data_http_post` | `URL` (in options), `authenticationType` and `verifyHost` (in security) |
| `data_tcpip_server` | `tcpipport` (in options) |
| `data_websocket` | none — but it also has **no URL or endpoint at all** |

So `httpPost` and `tcpip-server` may well be rejected at schema validation before
the reader ever contacts a receiver. If that happens, the receiver is not at
fault — check the response message first.

`WEBSOCKET` raises a different question: its example carries only a `security`
block, with nothing to say *where* to connect. How the reader is meant to learn
the WebSocket address is unclear from the spec.

---

## httpPost — port 9443

An HTTPS server that accepts POST on any path, logs the body, and always replies
`200 {}` so the reader has no delivery reason to retry.

```bash
systemctl status fxr60-recv-http-post
sudo systemctl restart fxr60-recv-http-post
sudo journalctl -u fxr60-recv-http-post -f      # watch live
```

Test it:

```bash
curl -sk -X POST -H "Content-Type: application/json" \
  -d '{"test":"hello"}' https://10.117.229.18:9443/tagdata
```

Reader config, following the spec's example shape:

```json
{
  "name": "DATA_HTTP",
  "description": "Tag events over HTTP POST",
  "type": "httpPost",
  "options": {
    "URL": "https://10.117.229.18:9443/tagdata",
    "security": {
      "authenticationType": "NONE",
      "verifyHost": false,
      "verifyPeer": false
    }
  }
}
```

Note `URL` is capitalised in the spec, and `authenticationType`/`verifyHost` sit
inside `security` — all three absent from the schema.

---

## WEBSOCKET — port 9444

A `wss` server accepting connections on any path, logging every frame.

```bash
systemctl status fxr60-recv-websocket
sudo journalctl -u fxr60-recv-websocket -f
```

Test it:

```bash
cd /home/altautoadmin/pfx_server
.venv/bin/python -c "
import asyncio, ssl, json, websockets
async def go():
    ctx = ssl.create_default_context(cafile='ca/ca.crt'); ctx.check_hostname=False
    async with websockets.connect('wss://10.117.229.18:9444/tagdata', ssl=ctx) as ws:
        await ws.send(json.dumps({'test':'hello'}))
        await asyncio.sleep(0.5)
asyncio.run(go())
"
```

Reader config per the spec's example — note there is nowhere to put an address:

```json
{
  "name": "DATA_WS",
  "description": "Tag events over WebSocket",
  "type": "WEBSOCKET",
  "options": {
    "security": { "verifyPeer": false }
  }
}
```

Worth trying with an `endpoint` block added (`hostName`/`port`/`protocol`), since
that *is* schema-valid, unlike the fields the other examples use.

---

## tcpip-server — port 8081

**The reader is the server here.** Its spec example has a `tcpipport` but no
hostname, which means the reader opens a listening socket and we connect *to it* —
the reverse of the other types.

So this tool is a **client**, not a service:

```bash
cd /home/altautoadmin/pfx_server
.venv/bin/python receivers/tcpip_client.py --host 10.233.48.36 --port 8081
```

It only connects once a `tcpip-server` connection is configured on the reader;
before that the port is closed.

If the reader turns out to connect outward instead — contradicting the field
naming, but worth being able to test — the tool also has a listen mode:

```bash
.venv/bin/python receivers/tcpip_client.py --listen --port 8081
```

Not a systemd service, because which side listens is unresolved. Once that is
settled it can be made one.

Reader config per the spec's example:

```json
{
  "name": "DATA_TCP",
  "description": "Tag events over TCP/IP server",
  "type": "tcpip-server",
  "options": {
    "enableSecurity": false,
    "tcpipport": "8081"
  }
}
```

`tcpipport` is a string in the example, and is not in the schema.

---

## Where received data goes

```
receivers/received/
├── http_post.log              one JSON object per line, appended
├── http_post_latest.json      the newest, pretty-printed
├── websocket.log
├── websocket_latest.json
├── tcpip.log
└── tcpip_latest.json
```

Each entry records the timestamp, source address, and the parsed body (or raw
text if it was not JSON). For `httpPost` the request headers are captured too.

```bash
# newest payload
cat receivers/received/http_post_latest.json

# follow as data arrives
tail -f receivers/received/http_post.log
```

---

## Verified working

All three were tested end to end before being put into service:

| Receiver | Test | Result |
|---|---|---|
| httpPost | `curl -X POST` with a JSON body | 200, body logged and stored |
| WEBSOCKET | `websockets.connect` + `send` | frame logged and stored |
| tcpip-server | `nc` to the listener | 57 bytes logged and stored |

The two systemd services were then re-tested after being started by systemd, to
confirm they work under it and not just when launched by hand.

---

## Ports in use on this host

| Port | Service |
|---|---|
| 443 | `pfx-file-server` — certificate/PFX downloads |
| 1883 | Mosquitto — plain MQTT |
| 1884 | Mosquitto — username/password |
| 8883 | Mosquitto — TLS |
| 8884 | Mosquitto — mutual TLS |
| **9443** | **httpPost receiver** |
| **9444** | **WEBSOCKET receiver** |

`tcpip-server` uses 8081 on the **reader**, not here.

---

## Related

| File | Contents |
|---|---|
| `../BROKER_REFERENCE.md` | The four MQTT brokers |
| `../Mqqt/README.md` | MQTT endpoint configs and how to apply them |
| `../Aws example/README.md` | AWS IoT Core configs |
| `../MQTT_API_Findings.xlsx` | All API findings, including the schema-vs-example defects |
