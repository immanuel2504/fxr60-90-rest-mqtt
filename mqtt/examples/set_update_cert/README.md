# `set_update_cert`

REST: `PUT /cloud/certificates` → `cloud-certificates/`

MQTT command key: `set_updateCertificate`

Stable `command_id`: `req-set-update-cert`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/https_basic.json` | request | `https_basic` | `cloud-certificates/PUT/https_basic.json` | HTTPS BASIC download |
| `request/mtls.json` | request | `mtls` | `cloud-certificates/PUT/mtls.json` | HTTPS BASIC with installed client cert and CA |
| `response/success.json` | response | `success` | `—` | Empty payload on success |
