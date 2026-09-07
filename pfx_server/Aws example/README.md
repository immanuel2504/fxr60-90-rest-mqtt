# AWS IoT Core cloudConfig examples (FXR60-LAB)

REST payloads for `PUT /cloud/cloudConfig` (MQTT equivalent: `set_importCloudConfig`,
wrapped as `{"command": "set_importCloudConfig", "payload": <file contents>}`).

Both files configure all four channels — control, data, management events,
management command/response — against AWS IoT Core.

## Request

```
PUT https://10.117.229.9/cloud/cloudConfig
Authorization: Bearer <token from GET /cloud/localRestLogin>
Content-Type: application/json
```

## The two files

| File | Certificate method | Status |
|---|---|---|
| `01-aws-installedCertificate-port443-REST.json` | `installedCertificateName` — references a cert already installed on the reader | **Confirmed working** |
| `02-aws-fileLocation-dataapps-port443-REST.json` | `*FileLocation` — points at cert files on the reader's filesystem under `/data/apps/` | Untested — needs the files present on the reader |

### 01 — installedCertificateName (confirmed working)

Requires the certificate to be installed on the reader first, via
`set_updateCertificate` (see `../mqtt/verified/set_updateCertificate_aws_client_install.json`),
which downloads a `.pfx` from an HTTPS server using Basic auth. Confirm it landed
with `get_certificates` — it should appear as `FXR60-LAB-AWS-CLIENT`.

Verified end to end: a `get_status` command published to `FXR60-LAB/mcmd` over AWS
returned a full, correct response on `FXR60-LAB/mrsp`.

### 02 — FileLocation (untested)

Expects three files to already exist on the reader:

```
/data/apps/AmazonRootCA1.pem
/data/apps/0e45e82812dfa432797089d8bd85dd813160f82cdc8db8e99893e0e896448666-private.pem.key
/data/apps/0e45e82812dfa432797089d8bd85dd813160f82cdc8db8e99893e0e896448666-certificate.pem.crt
```

`/data/apps` is used because writes to `/data` directly are denied on this reader.
The source files are in `../FXR60-LAB/`. If you copy them over with shorter names,
update the three `*FileLocation` values to match.

If the files are missing, the config is rejected with
`invalid "publicKeyFileLocation" path: File Not Found` — harmless, since a rejected
config is never applied and the reader keeps its current connection.

## Two things that were essential to get this working

**Port 443, not 8883.** Port 8883 is blocked on this reader's network path to AWS.
Every attempt on 8883 failed with `connection initialization failed with return
code (255), retry count (0)` — a generic error that looks identical to a
certificate problem, which made this expensive to diagnose. Port 443 works.

**ALPN.** AWS IoT needs `alpnProtocolNames: ["x-amzn-mqtt-ca"]` to carry MQTT over
port 443, since 443 is normally HTTPS.

Do **not** put this in the payload — `alpnProtocolNames` is not a valid field in
the `additional` schema (which allows only `cleanSession`, `clientId`, `debug`,
`keepAlive`, `qos`, `reconnectDelay`, `reconnectDelayMax`). The reader adds it
itself when the port is 443; you can see it in the `get_config` response, but it
is output-only. Both files here omit it, matching the schema.

## AWS-side prerequisites

- An IoT Policy attached to the certificate permitting `iot:Connect` for client IDs
  `FXR60-LAB-*`, plus `iot:Publish`/`iot:Receive`/`iot:Subscribe` on `FXR60-LAB/*`
  and `datacollection_aws/FXR60-LAB`.
  AWS's default SDK sample policy does **not** cover these — it only allows
  `sdk-java` / `basicPubSub` / `sdk-nodejs-*` client IDs and `sdk/test/*` topics.
- Certificate status must be **Active**.

A missing or too-narrow policy shows up as: TLS handshake succeeds, then AWS
immediately drops the MQTT connection.

## Not supported

Inline certificate content — `CACertificateFileContent`, `privateKeyFileContent`,
`publicKeyFileContent` — is rejected with
`invalid "security" JSON object`. These fields do not exist in any of the nine
`security` schemas in `FXR_60-90_rest_api.yaml`; they belong only to the
file-download commands (`set_updateCertificate`, `set_os`, `set_installUserapp`).

Note that the spec's own `mqtt_aws_all_channels` example uses these fields, which
contradicts its own schema — a documentation bug, logged in
`../MQTT_API_Findings.xlsx`.

## Recovering local MQTT access

If a config is applied but the reader fails to connect, it drops off both AWS and
the local broker. Restore it with `../mqtt/verified/rollback_local_mqtt_fxr60.json`
via the reader's local web UI (reachable because `enableLocalRest: true`) or Postman.
