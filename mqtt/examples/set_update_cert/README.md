# `set_update_cert`

REST: `PUT /cloud/certificates` → `cloud-certificates/`

Wire `command` (developer MQTT API): `set_updateCertificate` (alias `set_update_cert`)

Stable `command_id`: `req-set-update-cert`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/basic_https.json` | request | `basic_https` | `cloud-certificates/PUT/basic_https.json` | Install client cert over HTTPS with BASIC auth |
| `request/mtls_optional.json` | request | `mtls_optional` | `cloud-certificates/PUT/mtls_optional.json` | Install cert with optional mTLS |
| `response/success.json` | response | `success` | `—` | Command succeeded |
