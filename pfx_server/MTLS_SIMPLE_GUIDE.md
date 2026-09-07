# mTLS with FXR60 Reader and Mosquitto Broker — the simple version

---

## Normal TLS (8883)

### Files

**Broker**
```
broker.crt
broker.key
```

**Reader**
```
ca.crt
```

### Flow

```
Reader ---> Broker

Reader checks Broker certificate.
```

Only the broker proves its identity.

---

## mTLS (8884)

Now both sides prove who they are.

### Broker needs
```
ca.crt
broker.crt
broker.key
```

### Reader needs
```
ca.crt
reader.crt
reader.key
```

---

## Configure the broker

In the config file:

```
listener 8884

cafile /etc/mosquitto/certs/ca.crt

certfile /etc/mosquitto/certs/broker.crt
keyfile  /etc/mosquitto/certs/broker.key

require_certificate true
```

The important line is:

```
require_certificate true
```

This makes the broker ask:

> Reader, show me your certificate.

---

## Connection flow

**Step 1** — Reader:
> I want to connect.

**Step 2** — Broker:
> Here is my certificate.

Sends: `broker.crt`

**Step 3** — Reader verifies `broker.crt` using `ca.crt`
> OK, I trust you.

**Step 4** — Broker asks:
> Now show me YOUR certificate.

**Step 5** — Reader sends `reader.crt` and proves ownership using `reader.key`

**Step 6** — Broker verifies `reader.crt` using `ca.crt`
> OK, I trust you.

Connection succeeds.

---

## Picture

```
                ca.crt
                   ▲
                   │
             verifies both
                   │

 Reader                     Broker

 reader.crt                 broker.crt
 reader.key                 broker.key

      <------ mTLS ------->
```

---

## What changes from TLS to mTLS?

**Normal TLS:**
```
Broker has certificate
Reader does not
```

**mTLS:**
```
Broker has certificate
Reader ALSO has certificate
```

That's literally the only concept.

---

# The request body

Now the same idea, in the JSON you actually send to the reader.

```
PUT https://10.117.229.9/cloud/cloudConfig
Authorization: Bearer <token>
Content-Type: application/json
```

## Port 8883 — TLS

Reader only needs `ca.crt`, so the security block has **one** certificate field:

```json
"security": {
  "CACertificateFileLocation": "/data/apps/ca.crt",
  "keyAlgorithm": "RS256",
  "keyFormat": "PEM",
  "verifyHostName": true,
  "verifyPeer": true
}
```

## Port 8884 — mTLS

Reader also needs its own certificate and key, so **two more fields** appear:

```json
"security": {
  "CACertificateFileLocation": "/data/apps/ca.crt",
  "privateKeyFileLocation":    "/data/apps/reader.key",
  "publicKeyFileLocation":     "/data/apps/reader.crt",
  "keyAlgorithm": "RS256",
  "keyFormat": "PEM",
  "verifyHostName": true,
  "verifyPeer": true
}
```

## Field mapping

| Concept | JSON field |
|---|---|
| `ca.crt` — verify the broker | `CACertificateFileLocation` |
| `reader.crt` — reader's own certificate | `publicKeyFileLocation` |
| `reader.key` — proves reader owns it | `privateKeyFileLocation` |

Note the naming: the reader's **certificate** goes in a field called
`publicKeyFileLocation`. Slightly confusing, but that is the field name the reader
expects.

## Side by side

| Field | 8883 TLS | 8884 mTLS |
|---|---|---|
| `CACertificateFileLocation` | ✅ | ✅ |
| `privateKeyFileLocation` | — | ✅ |
| `publicKeyFileLocation` | — | ✅ |
| `verifyHostName` | ✅ | ✅ |
| `verifyPeer` | ✅ | ✅ |

Two extra fields. That's the whole difference — exactly matching "reader ALSO has
a certificate."

---

# Full request body — port 8883 (TLS)

```json
{
  "endpointConfig": {
    "control": {
      "commandResponse": {
        "enableLocalRest": true,
        "connections": [
          {
            "name": "CTRL_TLS",
            "description": "Control cmd/rsp over TLS",
            "type": "mqtt",
            "options": {
              "enableSecurity": true,
              "endpoint": {
                "hostName": "10.117.229.18",
                "port": 8883,
                "protocol": "ssl"
              },
              "additional": {
                "cleanSession": true,
                "clientId": "fxr60-lab-ctrl",
                "debug": false,
                "keepAlive": 60,
                "qos": 0,
                "reconnectDelay": 2,
                "reconnectDelayMax": 60
              },
              "publishTopic": ["fxr60-lab/rsp"],
              "subscribeTopic": ["fxr60-lab/cmd"],
              "security": {
                "CACertificateFileLocation": "/data/apps/ca.crt",
                "keyAlgorithm": "RS256",
                "keyFormat": "PEM",
                "verifyHostName": true,
                "verifyPeer": true
              }
            }
          }
        ]
      }
    },
    "data": {
      "event": {
        "connections": [
          {
            "name": "DATA_TLS",
            "description": "Tag events over TLS",
            "type": "mqtt",
            "options": {
              "enableSecurity": true,
              "endpoint": {
                "hostName": "10.117.229.18",
                "port": 8883,
                "protocol": "ssl"
              },
              "additional": {
                "cleanSession": true,
                "clientId": "fxr60-lab-data",
                "debug": false,
                "keepAlive": 60,
                "qos": 0,
                "reconnectDelay": 2,
                "reconnectDelayMax": 60
              },
              "publishTopic": ["fxr60-lab/tevents"],
              "subscribeTopic": [],
              "security": {
                "CACertificateFileLocation": "/data/apps/ca.crt",
                "keyAlgorithm": "RS256",
                "keyFormat": "PEM",
                "verifyHostName": true,
                "verifyPeer": true
              }
            },
            "additionalOptions": {
              "retention": {
                "maxEventRetentionTimeInMin": 500,
                "maxNumEvents": 150000,
                "throttle": 500
              }
            }
          }
        ]
      }
    },
    "management": {
      "event": {
        "connections": [
          {
            "name": "MGMT_EVENTS_TLS",
            "description": "Management/heartbeat events over TLS",
            "type": "mqtt",
            "options": {
              "enableSecurity": true,
              "endpoint": {
                "hostName": "10.117.229.18",
                "port": 8883,
                "protocol": "ssl"
              },
              "additional": {
                "cleanSession": true,
                "clientId": "fxr60-lab-mevents",
                "debug": false,
                "keepAlive": 60,
                "qos": 0,
                "reconnectDelay": 2,
                "reconnectDelayMax": 60
              },
              "publishTopic": ["fxr60-lab/mevents"],
              "subscribeTopic": [],
              "security": {
                "CACertificateFileLocation": "/data/apps/ca.crt",
                "keyAlgorithm": "RS256",
                "keyFormat": "PEM",
                "verifyHostName": true,
                "verifyPeer": true
              }
            }
          }
        ]
      },
      "commandResponse": {
        "enableLocalRest": true,
        "connections": [
          {
            "name": "MGMT_CMD_TLS",
            "description": "Management cmd/rsp over TLS",
            "type": "mqtt",
            "options": {
              "enableSecurity": true,
              "endpoint": {
                "hostName": "10.117.229.18",
                "port": 8883,
                "protocol": "ssl"
              },
              "additional": {
                "cleanSession": true,
                "clientId": "fxr60-lab-mcmd",
                "debug": false,
                "keepAlive": 60,
                "qos": 0,
                "reconnectDelay": 2,
                "reconnectDelayMax": 60
              },
              "publishTopic": ["fxr60-lab/mrsp"],
              "subscribeTopic": ["fxr60-lab/mcmd"],
              "security": {
                "CACertificateFileLocation": "/data/apps/ca.crt",
                "keyAlgorithm": "RS256",
                "keyFormat": "PEM",
                "verifyHostName": true,
                "verifyPeer": true
              }
            }
          }
        ]
      }
    }
  }
}
```

---

# Full request body — port 8884 (mTLS)

Same as above, with `port` changed to `8884` and the two extra certificate fields
in every `security` block.

```json
{
  "endpointConfig": {
    "control": {
      "commandResponse": {
        "enableLocalRest": true,
        "connections": [
          {
            "name": "CTRL_MTLS",
            "description": "Control cmd/rsp over mTLS",
            "type": "mqtt",
            "options": {
              "enableSecurity": true,
              "endpoint": {
                "hostName": "10.117.229.18",
                "port": 8884,
                "protocol": "ssl"
              },
              "additional": {
                "cleanSession": true,
                "clientId": "fxr60-lab-ctrl",
                "debug": false,
                "keepAlive": 60,
                "qos": 0,
                "reconnectDelay": 2,
                "reconnectDelayMax": 60
              },
              "publishTopic": ["fxr60-lab/rsp"],
              "subscribeTopic": ["fxr60-lab/cmd"],
              "security": {
                "CACertificateFileLocation": "/data/apps/ca.crt",
                "privateKeyFileLocation": "/data/apps/reader.key",
                "publicKeyFileLocation": "/data/apps/reader.crt",
                "keyAlgorithm": "RS256",
                "keyFormat": "PEM",
                "verifyHostName": true,
                "verifyPeer": true
              }
            }
          }
        ]
      }
    },
    "data": {
      "event": {
        "connections": [
          {
            "name": "DATA_MTLS",
            "description": "Tag events over mTLS",
            "type": "mqtt",
            "options": {
              "enableSecurity": true,
              "endpoint": {
                "hostName": "10.117.229.18",
                "port": 8884,
                "protocol": "ssl"
              },
              "additional": {
                "cleanSession": true,
                "clientId": "fxr60-lab-data",
                "debug": false,
                "keepAlive": 60,
                "qos": 0,
                "reconnectDelay": 2,
                "reconnectDelayMax": 60
              },
              "publishTopic": ["fxr60-lab/tevents"],
              "subscribeTopic": [],
              "security": {
                "CACertificateFileLocation": "/data/apps/ca.crt",
                "privateKeyFileLocation": "/data/apps/reader.key",
                "publicKeyFileLocation": "/data/apps/reader.crt",
                "keyAlgorithm": "RS256",
                "keyFormat": "PEM",
                "verifyHostName": true,
                "verifyPeer": true
              }
            },
            "additionalOptions": {
              "retention": {
                "maxEventRetentionTimeInMin": 500,
                "maxNumEvents": 150000,
                "throttle": 500
              }
            }
          }
        ]
      }
    },
    "management": {
      "event": {
        "connections": [
          {
            "name": "MGMT_EVENTS_MTLS",
            "description": "Management/heartbeat events over mTLS",
            "type": "mqtt",
            "options": {
              "enableSecurity": true,
              "endpoint": {
                "hostName": "10.117.229.18",
                "port": 8884,
                "protocol": "ssl"
              },
              "additional": {
                "cleanSession": true,
                "clientId": "fxr60-lab-mevents",
                "debug": false,
                "keepAlive": 60,
                "qos": 0,
                "reconnectDelay": 2,
                "reconnectDelayMax": 60
              },
              "publishTopic": ["fxr60-lab/mevents"],
              "subscribeTopic": [],
              "security": {
                "CACertificateFileLocation": "/data/apps/ca.crt",
                "privateKeyFileLocation": "/data/apps/reader.key",
                "publicKeyFileLocation": "/data/apps/reader.crt",
                "keyAlgorithm": "RS256",
                "keyFormat": "PEM",
                "verifyHostName": true,
                "verifyPeer": true
              }
            }
          }
        ]
      },
      "commandResponse": {
        "enableLocalRest": true,
        "connections": [
          {
            "name": "MGMT_CMD_MTLS",
            "description": "Management cmd/rsp over mTLS",
            "type": "mqtt",
            "options": {
              "enableSecurity": true,
              "endpoint": {
                "hostName": "10.117.229.18",
                "port": 8884,
                "protocol": "ssl"
              },
              "additional": {
                "cleanSession": true,
                "clientId": "fxr60-lab-mcmd",
                "debug": false,
                "keepAlive": 60,
                "qos": 0,
                "reconnectDelay": 2,
                "reconnectDelayMax": 60
              },
              "publishTopic": ["fxr60-lab/mrsp"],
              "subscribeTopic": ["fxr60-lab/mcmd"],
              "security": {
                "CACertificateFileLocation": "/data/apps/ca.crt",
                "privateKeyFileLocation": "/data/apps/reader.key",
                "publicKeyFileLocation": "/data/apps/reader.crt",
                "keyAlgorithm": "RS256",
                "keyFormat": "PEM",
                "verifyHostName": true,
                "verifyPeer": true
              }
            }
          }
        ]
      }
    }
  }
}
```

---

## For your FXR60 lab

### Port 8883

Reader files:
```
/data/apps/ca.crt
```

### Port 8884

Reader files:
```
/data/apps/ca.crt
/data/apps/reader.crt
/data/apps/reader.key
```

So when your FXR60 is configured for mTLS, the additional files compared to TLS
are:

```
reader.crt
reader.key
```

Those two files allow the reader to prove:

> "I am an authorized reader."

And in the JSON, those two files are the two extra fields:

```
privateKeyFileLocation   →  reader.key
publicKeyFileLocation    →  reader.crt
```

---

## Before you send it

**1. The files must exist on the reader.** Copy them to `/data/apps/` — writes to
`/data` directly are denied on this reader.

Files to copy, from this host:

| Copy to reader | From |
|---|---|
| `/data/apps/ca.crt` | `ca/ca.crt` |
| `/data/apps/reader.crt` | `broker-certs/fxr60-client.crt` |
| `/data/apps/reader.key` | `broker-certs/fxr60-client.key` |

If a path is wrong you get `invalid "publicKeyFileLocation" path: File Not Found`.
Harmless — a rejected config is never applied, so the reader keeps its current
connection.

**2. The reader certificate must be signed by the same CA as the broker's.** Our
broker trusts `Local RFID Test CA`. The AWS certificate in `FXR60-LAB/` is signed
by Amazon's CA and will be rejected — correct behaviour, not a fault.

**3. Three fields change together for TLS.** `enableSecurity: true`,
`port: 8883`/`8884`, and `protocol: "ssl"`. Setting the port without changing the
protocol attempts a plain connection against a TLS listener and fails.

---

## Alternative: certificate store instead of files

Instead of file paths, the reader can reference a certificate already installed in
its own store:

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

The certificate is installed beforehand via `set_updateCertificate`, which
downloads a `.pfx` over HTTPS.

Worth knowing: this method failed repeatedly during the AWS work with
`connection initialization failed with return code (255), retry count (0)`. That
turned out to be a blocked port rather than a problem with the method itself, but
it has not been independently confirmed against our own broker. Try the file-path
version first — its error messages are clearer.

---

## Checking it worked

```bash
# broker log for the mTLS listener
sudo tail -20 /var/log/mosquitto/fxr60-mtls.log

# did the reader's clients connect?
sudo grep -E "fxr60-lab-(ctrl|data|mcmd|mevents)" \
  /var/log/mosquitto/fxr60-mtls.log | tail

# send a command over mTLS
mosquitto_sub -h 10.117.229.18 -p 8884 --cafile ca/ca.crt \
  --cert broker-certs/fxr60-client.crt \
  --key broker-certs/fxr60-client.key \
  -t fxr60-lab/mrsp &

mosquitto_pub -h 10.117.229.18 -p 8884 --cafile ca/ca.crt \
  --cert broker-certs/fxr60-client.crt \
  --key broker-certs/fxr60-client.key \
  -t fxr60-lab/mcmd \
  -m '{"command":"get_status","command_id":"mtls-1","payload":{}}'
```

For mTLS failures the broker log is the most useful source — it reports whether
the reader presented a certificate at all, and if so why it was rejected. Far more
informative than the reader's generic error codes.

---

## Related documents

| File | Contents |
|---|---|
| `CERTIFICATE_GUIDE.md` | Creating the CA and CA-signed certificates |
| `MQTT_BROKER_SETUP_GUIDE.md` | Building the broker from scratch |
| `BROKER_REFERENCE.md` | Operating the four brokers |
| `MQTT example/` | All five reader payloads |
