# `refresh-cert`

REST: `PUT /cloud/certificates/{certname}` → `cloud-certificates-certname/`

MQTT command key: `set_refreshCertificate`

Stable `command_id`: `req-refresh-cert`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/refresh_client.json` | request | `refresh_client` | `cloud-certificates-certname/PUT/refresh_client.json` | Refresh client `mqtt-test-cert-1` |
| `request/refresh_server.json` | request | `refresh_server` | `cloud-certificates-certname/PUT/refresh_server.json` | Refresh `Server` |
| `response/success.json` | response | `success` | `—` | Empty payload on success |
