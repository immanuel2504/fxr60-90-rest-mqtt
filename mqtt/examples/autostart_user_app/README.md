# `autostart_user_app`

REST: `PUT /cloud/apps/{appname}/autostart` → `cloud-apps-appname-autostart/`

MQTT command key: `set_autostartUserapp`

Stable `command_id`: `req-autostart-user-app`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/autostart_true.json` | request | `autostart_true` | `cloud-apps-appname-autostart/PUT/autostart_true.json` | `autostart` true |
| `request/autostart_false.json` | request | `autostart_false` | `cloud-apps-appname-autostart/PUT/autostart_false.json` | `autostart` false |
| `response/success.json` | response | `success` | `—` | Empty payload on success |
