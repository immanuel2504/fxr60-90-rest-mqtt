# `stop_user_app`

REST: `PUT /cloud/apps/{appname}/stop` → `cloud-apps-appname-stop/`

MQTT command key: `set_stopUserapp`

Stable `command_id`: `req-stop-user-app`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/stopUserapp.json` | request | `stopUserapp` | `—` | Payload `appname` `mylogger` |
| `response/success.json` | response | `success` | `cloud-apps-appname-stop/PUT/success.json` | Empty payload on success |
