# `del_certs`

REST: `DELETE /cloud/certificates/{certname}` → `cloud-certificates-certname/`

MQTT command key: `del_certificate`

Stable `command_id`: `req-del-certs`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/delete_client.json` | request | `delete_client` | `cloud-certificates-certname/DELETE/delete_client.json` | Delete `type` client |
| `response/success.json` | response | `success` | `—` | Empty payload on success |
