# `set_installCACertificate`

REST: `PUT /cloud/caCertificates` → `cloud-cacertificates/`

MQTT command key: `set_InstallCACertificate`

Stable `command_id`: `req-set-installCACertificate`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/install_ca.json` | request | `install_ca` | `cloud-cacertificates/PUT/install_ca.json` | Install a CA (`name` + PEM `content`) |
| `response/success.json` | response | `success` | `—` | Empty payload on success |
