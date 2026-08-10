# `install_user_app`

REST: `PUT /cloud/apps/install` → `cloud-apps-install/`

Stable `command_id`: `req-install-user-app`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/installUserapp.json` | request | `installUserapp` | `cloud-apps-install/PUT/installUserapp.json` |  |
| `request/installUserapp_no_auth.json` | request | `installUserapp_no_auth` | `cloud-apps-install/PUT/installUserapp_no_auth.json` | NONE auth |
| `request/installUserapp_pinned_ca.json` | request | `installUserapp_pinned_ca` | `cloud-apps-install/PUT/installUserapp_pinned_ca.json` | BASIC + TLS pin |
| `response/success.json` | response | `success` | `—` | Command succeeded |

