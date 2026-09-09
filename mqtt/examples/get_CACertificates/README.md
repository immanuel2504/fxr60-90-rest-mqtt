# `get_CACertificates`

REST: `GET /cloud/caCertificates` → `cloud-cacertificates/`

Stable `command_id`: `req-get-CACertificates`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_CACertificates request |
| `response/empty_list.json` | response | `empty_list` | `cloud-cacertificates/GET/empty_list.json` | No CA certificates |
| `response/ca_list.json` | response | `ca_list` | `cloud-cacertificates/GET/ca_list.json` | CA names with `.crt` |
