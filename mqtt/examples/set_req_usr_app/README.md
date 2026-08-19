# `set_req_usr_app`

REST: `PUT /cloud/apps/{appname}/pass-through` → `cloud-apps-appname-pass-through/`

Stable `command_id`: `req-set-req-usr-app`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/reqToUserapp.json` | request | `reqToUserapp` | `cloud-apps-appname-pass-through/PUT/reqToUserapp.json` |  |
| `request/reqToUserapp_command.json` | request | `reqToUserapp_command` | `cloud-apps-appname-pass-through/PUT/reqToUserapp_command.json` | Command message variant |
| `request/reqToUserapp_reload.json` | request | `reqToUserapp_reload` | `cloud-apps-appname-pass-through/PUT/reqToUserapp_reload.json` | Alternate userapp payload |
| `response/app_reply.json` | response | `app_reply` | `cloud-apps-appname-pass-through/PUT/app_reply.json` | App-defined response shape |

