# `start_user_app`

REST: `PUT /cloud/apps/{appname}/start` → `cloud-apps-appname-start/`

MQTT command key: `set_startUserapp`

Stable `command_id`: `req-start-user-app`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/startUserapp.json` | request | `startUserapp` | `—` | Payload `appname` `mylogger` |
| `response/success.json` | response | `success` | `cloud-apps-appname-start/PUT/success.json` | Empty payload on success |
