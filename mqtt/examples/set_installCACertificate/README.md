# `set_installCACertificate`

REST: `PUT /cloud/caCertificates/{caname}` → `cloud-cacertificates-caname/`

Stable `command_id`: `req-set-installCACertificate`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/InstallCACertificate.json` | request | `InstallCACertificate` | `cloud-cacertificates-caname/PUT/InstallCACertificate.json` |  |
| `request/InstallCACertificate_named.json` | request | `InstallCACertificate_named` | `cloud-cacertificates-caname/PUT/InstallCACertificate_named.json` | MQTT-style body includes name; REST uses path {caname} |
| `response/success.json` | response | `success` | `—` | Command succeeded |

