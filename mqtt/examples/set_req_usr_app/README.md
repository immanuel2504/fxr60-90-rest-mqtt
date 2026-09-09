# `set_req_usr_app`

REST: `PUT /cloud/apps/{appname}/pass-through` → `cloud-apps-appname-pass-through/`

MQTT command key: `set_reqToUserapp`

Stable `command_id`: `req-set-req-usr-app`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/pass_through.json` | request | `pass_through` | `cloud-apps-appname-pass-through/PUT/pass_through.json` | `userapp` `mylogger` with `command.message` |
| `response/app_reply.json` | response | `app_reply` | `—` | Application-defined reply |
