# `install_user_app`

REST: `PUT /cloud/apps/install` → `cloud-apps-install/`

MQTT command key: `set_installUserapp`

Stable `command_id`: `req-install-user-app`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/app-install-none.json` | request | `app-install-none` | `cloud-apps-install/PUT/app-install-none.json` | HTTPS `NONE` |
| `request/app-install-basic.json` | request | `app-install-basic` | `cloud-apps-install/PUT/app-install-basic.json` | HTTPS `BASIC` |
| `request/app-install-bearer.json` | request | `app-install-bearer` | `cloud-apps-install/PUT/app-install-bearer.json` | HTTPS `NONE` with `Authorization` |
| `request/app-install-mtls.json` | request | `app-install-mtls` | `cloud-apps-install/PUT/app-install-mtls.json` | HTTPS `BASIC` with installed cert and CA |
| `request/sftp_basic.json` | request | `sftp_basic` | `cloud-apps-install/PUT/sftp_basic.json` | SFTP `BASIC` |
| `response/success.json` | response | `success` | `—` | Empty payload on success |
