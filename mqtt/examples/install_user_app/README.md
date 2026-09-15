# `install_user_app`

REST: `PUT /cloud/apps/install` → `cloud-apps-install/`

| File | Direction | Example name | Summary title |
|---|---|---|---|
| `request/app-install-none.json` | request | `app-install-none` | HTTPS NONE |
| `request/app-install-basic.json` | request | `app-install-basic` | HTTPS BASIC |
| `request/app-install-bearer.json` | request | `app-install-bearer` | HTTPS NONE with Authorization |
| `request/app-install-mtls.json` | request | `app-install-mtls` | HTTPS BASIC with installed cert and CA |
| `request/sftp_basic.json` | request | `sftp_basic` | SFTP BASIC |
| `response/success.json` | response | `success` | Command succeeded |
