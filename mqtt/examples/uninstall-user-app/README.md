# `uninstall-user-app`

REST: `PUT /cloud/apps/{appname}/uninstall` → `cloud-apps-appname-uninstall/`

MQTT command key: `set_uninstallUserapp`

Stable `command_id`: `req-uninstall-user-app`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/uninstallUserapp.json` | request | `uninstallUserapp` | `—` | Payload `appname` `mylogger` |
| `response/success.json` | response | `success` | `cloud-apps-appname-uninstall/PUT/success.json` | Empty payload on success |
