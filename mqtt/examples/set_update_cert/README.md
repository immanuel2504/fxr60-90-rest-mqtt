# `set_update_cert`

REST: `PUT /cloud/certificates` → `cloud-certificates/`

Wire `command` (developer MQTT API): `set_updateCertificate` (alias `set_update_cert`)

Stable `command_id`: `req-set-update-cert`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/updateCertificate.json` | request | `updateCertificate` | `cloud-certificates/PUT/updateCertificate.json` |  |
| `request/updateCertificate_async.json` | request | `updateCertificate_async` | `cloud-certificates/PUT/updateCertificate_async.json` | Install certificate over HTTPS with retry (async) |
| `request/updateCertificate_client.json` | request | `updateCertificate_client` | `cloud-certificates/PUT/updateCertificate_client.json` | Client cert for mTLS MQTT |
| `request/updateCertificate_app.json` | request | `updateCertificate_app` | `cloud-certificates/PUT/updateCertificate_app.json` | App certificate, no download auth |
| `request/updateCertificate_inline_pem.json` | request | `updateCertificate_inline_pem` | `cloud-certificates/PUT/updateCertificate_inline_pem.json` | Inline CA content |
| `response/success.json` | response | `success` | `—` | Command succeeded |

