# Connecting the FXR60/FXR90 Reader to AWS IoT Core

This is a walkthrough for pointing a reader's `mqtt-AWS` cloud connection at a
real AWS IoT Core account, based on work done while testing `set_importCloudConfig`
against the lab FXR60 reader.

## Why this is different from the plain MQTT setup

The lab setup used so far in this project (`lab_mqtt.json`, `test_mqtt_api.py`)
talks to a local Mosquitto-style broker with no TLS and no per-device identity -
any client that can reach the broker can publish/subscribe.

AWS IoT Core requires **mutual TLS**: the reader authenticates to AWS using a
unique X.509 certificate + private key, and AWS Root CA to trust the server. This
means each reader needs its own certificate before it can connect, and an IoT
Policy authorizing what that certificate is allowed to do (connect / publish /
subscribe / receive, and on which topics).

## What you need before writing the cloudConfig payload

| Item | Where it comes from | Secret? |
|---|---|---|
| Device data endpoint | AWS IoT Core console -> Settings | No - safe to note down anywhere |
| Device certificate (`.pem.crt`) | Created when you create an IoT "Thing" | No - public half of the keypair |
| Private key (`.pem.key`) | Created at the same time as the cert | **Yes** - only downloadable once, never share it |
| Amazon Root CA 1 (`AmazonRootCA1.pem`) | Public, same file for every AWS account | No |
| IoT Policy | Written by you, attached to the certificate | No |
| AWS account ID + region | AWS console top-right corner | Account ID isn't fully secret but avoid posting it publicly |

## Step-by-step: creating the Thing and certificate

1. **Find your account's endpoint.**
   Easiest path: **Test -> MQTT test client** (left sidebar) - the "Connection
   details" panel on that page shows your real endpoint under **Endpoint**
   once connected (e.g. `a2fvbpwwdngail-ats.iot.eu-north-1.amazonaws.com`).
   It's the same value you'd find under **Settings -> "Device data endpoint"**.
   It looks like `<random-id>-ats.iot.<region>.amazonaws.com`.
   Do **not** use the sample/placeholder endpoint `test-ats.iot.us-east-1.amazonaws.com`
   that shows up in generic examples - every account has its own.

2. **Create a Thing.**
   **Manage -> All devices -> Things -> Create things -> Create single thing.**
   Give it a name matching the reader, e.g. `FXR60-LAB`.
   Skip the device shadow step.

3. **Generate a certificate.**
   On the "Configure device certificate" step, choose
   **Auto-generate a new certificate (recommended)**.
   Download all three files immediately - the private key cannot be
   retrieved again later if you lose it:
   - `xxxxxxxxxx-certificate.pem.crt` -> device certificate
   - `xxxxxxxxxx-private.pem.key` -> private key
   - The Amazon Root CA 1 link on the same page -> `AmazonRootCA1.pem`

4. **Attach an IoT Policy.**
   Either attach one during Thing creation, or later under
   **Security -> Policies**. The policy needs to allow, at minimum:
   - `iot:Connect` for the reader's client IDs
   - `iot:Publish` / `iot:Subscribe` / `iot:Receive` on the reader's topics

   Example policy shape (replace `<account-id>`, `<region>`, and the
   client-id/topic patterns with the real values):

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": "iot:Connect",
         "Resource": "arn:aws:iot:<region>:<account-id>:client/FXR60-LAB-*"
       },
       {
         "Effect": "Allow",
         "Action": ["iot:Publish", "iot:Receive"],
         "Resource": "arn:aws:iot:<region>:<account-id>:topic/FXR60-LAB/*"
       },
       {
         "Effect": "Allow",
         "Action": "iot:Subscribe",
         "Resource": "arn:aws:iot:<region>:<account-id>:topicfilter/FXR60-LAB/*"
       }
     ]
   }
   ```

5. **Activate the certificate.**
   Should be **Active** by default - confirm under **Security -> Certificates**.
   A disabled/revoked certificate will make the reader's TLS handshake fail.

## What NOT to reuse

The AWS IoT Core console has a browser-based **MQTT test client**
(Test -> MQTT test client) that shows a `Client ID` like
`iotconsole-xxxxxxxx-...` when you connect through it. That client ID and
its connection settings (MQTT version, clean start, keep alive) belong to
the *browser tool's own session* - they authenticate via your AWS login,
not a device certificate. Do not reuse that client ID for the reader; the
reader needs its own client IDs matching the cloudConfig
(e.g. `FXR60-LAB-CTRL`, `FXR60-LAB-MCMD`, `FXR60-LAB-DATA`, `FXR60-LAB-MEVENTS`).

## Getting the cert files onto the reader

The reader's cloudConfig `security` block references **local file paths on
the reader's own filesystem** (e.g. `/data/AmazonRootCA1.pem`,
`/data/aws-pvt.key`, `/data/aws-pub.crt`) - not URLs. These files have to be
present on the reader before `set_importCloudConfig` / `PUT /cloud/cloudConfig`
is called with a `type: mqtt-AWS` connection, or the reader has nothing to load
and the connection will fail. How the files get onto the reader (SFTP,
`set_installCACertificate`-style upload, or physical provisioning) needs to be
confirmed against Zebra's device provisioning docs for this reader model - the
REST/MQTT API surface in this repo covers CA/client certificate installation for
the `/cloud/certificates` and `/cloud/caCertificates` endpoints, but not
provisioning-time file drops.

## cloudConfig payload shape for mqtt-AWS

Once the above exists, the connection block looks like this (values shown are
placeholders for the FXR60-LAB naming used in this project):

```json
{
  "name": "CTRL_AWS",
  "description": "Control cmd/rsp through AWS IoT Core",
  "type": "mqtt-AWS",
  "options": {
    "enableSecurity": true,
    "endpoint": {
      "hostName": "<your-account-id>-ats.iot.<region>.amazonaws.com",
      "port": 8883,
      "protocol": "ssl"
    },
    "additional": {
      "cleanSession": true,
      "clientId": "FXR60-LAB-CTRL",
      "keepAlive": 30,
      "qos": 1,
      "reconnectDelay": 1,
      "reconnectDelayMax": 30
    },
    "publishTopic": ["FXR60-LAB/rsp"],
    "subscribeTopic": ["FXR60-LAB/cmd"],
    "security": {
      "CACertificateFileLocation": "/data/AmazonRootCA1.pem",
      "privateKeyFileLocation": "/data/aws-pvt.key",
      "publicKeyFileLocation": "/data/aws-pub.crt",
      "keyAlgorithm": "RS256",
      "keyFormat": "PEM",
      "verifyHostName": true,
      "verifyPeer": true
    }
  }
}
```

This repeats per channel (control, management command/response, management
events, data events) with different `name`, `clientId`, and topics - see
`FXR_60-90_rest_api.yaml`'s `set_importCloudConfig` examples
(`mqtt_aws_all_channels`) for the full multi-channel shape.

## Verifying before sending set_importCloudConfig for real

`set_importCloudConfig` (`PUT /cloud/cloudConfig`) overwrites the reader's
*entire* cloud connection config in one call, including whatever we're
currently using to talk to the reader over local MQTT. Before sending an
AWS-pointed cloudConfig for real:

1. Confirm the cert files are actually present at the referenced paths on
   the reader (no live command in this API surface currently reports that -
   would need to be confirmed via `get_config` output or a support channel).
2. Have a fallback plan to restore the current working `lab_mqtt.json`-style
   config if the AWS connection doesn't come up (e.g. keep the current,
   confirmed-working cloudConfig JSON on hand to re-import).
3. Test with the lowest-risk channel first if possible, rather than all four
   connections (control, data, management events, management cmd/rsp) at once.

## Status as of this session

- Endpoint confirmed: `a2fvbpwwdngail-ats.iot.eu-north-1.amazonaws.com`
  (region: `eu-north-1`), found via the MQTT test client's connection panel.
- Certificate created: AWS confirmed creation with certificate ID
  `0e45e82812dfa432797089d8bd85dd813160f82cdc8db8e99893e0e896448666`
  (download the cert + private key + Amazon Root CA 1 files from the
  "View certificate" link before leaving that page - the private key is only
  downloadable once).
- IoT Policy: not yet confirmed attached to this certificate - check
  **Security -> Certificates -> (this cert) -> Policies** and attach one if
  missing (see the example policy above).
- Cert files not yet placed on the reader's filesystem.
- `set_importCloudConfig` has not been tested with a real `mqtt-AWS` block
  against the live reader yet - remains on the untested danger-tier list
  alongside the plain-MQTT `set_importCloudConfig`/`set_config` entries in
  `MQTT_Untested_Commands.xlsx`.
