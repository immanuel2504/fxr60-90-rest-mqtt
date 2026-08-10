# `del_certs`

REST: `DELETE /cloud/certificates/{certname}` → `cloud-certificates-certname/`

Stable `command_id`: `req-del-certs`

| File | Direction | Example | REST mapping | Summary |
|---|---|---|---|---|
| `request/del_certs.json` | request | `del_certs` | path `certname` + query `type` | Delete client certificate |
| `response/success.json` | response | `success` | `""` | Command succeeded |

Name and type are both in the MQTT payload (`name` ↔ REST path, `type` ↔ REST query). Server certificates cannot be deleted.
