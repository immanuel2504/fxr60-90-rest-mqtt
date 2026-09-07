# httpPost, WEBSOCKET and tcpip-server payloads

Configs for the three non-MQTT connection types `PUT /cloud/cloudConfig`
documents, pointed at the receivers on this host.

MQTT and AWS payloads live in `../Mqqt/` and `../Aws example/`.

```
Endpoint types/
├── 01-httpPost-9443.json            httpPost → our HTTPS receiver
├── 02-websocket-spec-shape.json     WEBSOCKET, exactly as the spec's example
├── 03-websocket-with-endpoint.json  WEBSOCKET with an endpoint block added
└── 04-tcpip-server-8081.json        tcpip-server, reader listens on 8081
```

All four configure `data.event` only — these types carry tag data, not commands.

---

## Schema check, done before sending

| File | Type | Verdict |
|---|---|---|
| `01-httpPost-9443.json` | `httpPost` | ⚠️ **likely rejected** — `URL`, `authenticationType`, `verifyHost` not in schema |
| `02-websocket-spec-shape.json` | `WEBSOCKET` | ✅ schema-valid |
| `03-websocket-with-endpoint.json` | `WEBSOCKET` | ✅ schema-valid |
| `04-tcpip-server-8081.json` | `tcpip-server` | ⚠️ **likely rejected** — `tcpipport` not in schema |

The schema for `data.event.options` permits exactly six fields:

```
additional  enableSecurity  endpoint  publishTopic  security  subscribeTopic
```

Files 01 and 04 follow the shapes in the spec's own `data_http_post` and
`data_tcpip_server` examples — which use fields the schema does not define. That
same contradiction has already been confirmed twice on this API
(`CACertificateFileContent`, `basicAuthentication`), and the reader rejected both
with `invalid "..." JSON object`.

They are included anyway, because a rejection *is* the finding: it confirms three
of six documented connection types cannot be configured from the documented
schema. The receivers exist and are verified, so a failure cannot be blamed on our
end.

---

## Receivers

Built and tested — see `../receivers/README.md`.

| Type | Receiver | Port | Service |
|---|---|---|---|
| `httpPost` | HTTPS server | 9443 | `fxr60-recv-http-post` (running, enabled) |
| `WEBSOCKET` | wss server | 9444 | `fxr60-recv-websocket` (running, enabled) |
| `tcpip-server` | TCP client | 8081 on the **reader** | manual, see below |

Check they are up:

```bash
systemctl is-active fxr60-recv-http-post fxr60-recv-websocket
```

---

## 01 — httpPost

```json
"options": {
  "URL": "https://10.117.229.18:9443/tagdata",
  "security": {
    "authenticationType": "NONE",
    "verifyHost": false,
    "verifyPeer": false
  }
}
```

`verifyPeer: false` because the receiver's certificate is signed by the lab CA and
the reader may not have it loaded for this connection. To test *with* verification,
put `lab-ca.crt` at `/data/apps/` and set `verifyPeer: true`.

**Watch for arrivals:**

```bash
sudo journalctl -u fxr60-recv-http-post -f
tail -f receivers/received/http_post.log
```

If it is rejected at validation, the reader will never contact the receiver —
check the response message before suspecting the receiver.

---

## 02 and 03 — WEBSOCKET

Two variants, because the spec's example has **no address field of any kind** —
there is nowhere to say where to connect.

**02** is the spec's example verbatim: only `security.verifyPeer`. If this is
accepted, the interesting question is where the reader tries to connect, since
nothing told it. Watch the receiver log and `journalctl`.

**03** adds a schema-valid `endpoint` block:

```json
"enableSecurity": true,
"endpoint": { "hostName": "10.117.229.18", "port": 9444, "protocol": "ssl" },
"security": {
  "CACertificateFileLocation": "/data/apps/lab-ca.crt",
  "verifyHostName": false,
  "verifyPeer": true
}
```

This is a guess, but an informed one — `endpoint` is in the schema, unlike the
fields the httpPost example uses. `verifyHostName: false` because the receiver
certificate's SAN names `10.117.229.18`, which should match, but hostname checks
are a common source of confusion; tighten it once the connection works.

Requires `/data/apps/lab-ca.crt` on the reader — the same file the MQTT TLS configs
use.

**Watch:**

```bash
sudo journalctl -u fxr60-recv-websocket -f
tail -f receivers/received/websocket.log
```

---

## 04 — tcpip-server

```json
"options": {
  "enableSecurity": false,
  "tcpipport": "8081"
}
```

**The reader is the server here.** No hostname appears in the spec's example, only
a port — so the reader opens a listening socket on 8081 and we connect *to it*.
That is the reverse of every other connection type.

So after applying this config, connect **to the reader**:

```bash
cd /home/altautoadmin/pfx_server
.venv/bin/python receivers/tcpip_client.py --host 10.233.48.36 --port 8081
```

The port stays closed until the config is applied. Check first:

```bash
nc -zv 10.233.48.36 8081
```

If the reader turns out to connect outward instead — contradicting the field
naming — use listen mode:

```bash
.venv/bin/python receivers/tcpip_client.py --listen --port 8081
```

Note `tcpipport` is a **string** in the spec's example, not a number. Kept as a
string here to match.

---

## How to send

```
PUT https://10.233.48.36/cloud/cloudConfig
Authorization: Bearer <token>
Content-Type: application/json
```

Get a token:

```bash
TOKEN=$(curl -sk -u 'admin:Zebra@123' \
  https://10.233.48.36/cloud/localRestLogin \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['message'])")
```

Or over MQTT, wrapped as
`{"command": "set_importCloudConfig", "payload": <file contents>}`.

### Reading the response

| Response | Meaning |
|---|---|
| `{"response":"success"}` / HTTP 200 | Applied. Watch the receiver for data |
| `invalid "..." JSON object` | Rejected at validation — nothing changed, reader keeps its current config |
| `Could not connect to remote host` | Config applied; the reader could not reach the receiver |

A rejection is safe: the reader keeps working as before.

---

## Suggested order

1. **02** — spec-shape WEBSOCKET. Schema-valid, so it should at least be accepted;
   the question is where it connects
2. **03** — WEBSOCKET with an endpoint. If 02 is accepted but never connects, and
   03 does connect, that answers where the address belongs
3. **01** — httpPost. Expect rejection; the message will confirm the schema gap
4. **04** — tcpip-server. Same expectation, plus it resolves which side listens

Doing the schema-valid ones first means a rejection on 01/04 can be attributed to
the missing fields rather than something about our setup.

---

## Related

| File | Contents |
|---|---|
| `../receivers/README.md` | The receivers, how to watch them, ports in use |
| `../Mqqt/README.md` | MQTT endpoint configs |
| `../Aws example/README.md` | AWS IoT Core configs |
| `../MQTT_API_Findings.xlsx` | Findings, including the schema-vs-example defects |
