# `/cloud/certificates/{certname}`

- **PUT** — Refresh certificate (`set_refreshCertificate`)
- **DELETE** — Delete certificate (`del_certificate`)

## PUT examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `PUT/refresh_client.json` | request | `refresh_client` | Refresh `type` client |
| `PUT/refresh_server.json` | request | `refresh_server` | Refresh `type` server |
| `PUT/success.json` | response 200 | `success` | Empty string on success |

## DELETE examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `DELETE/delete_client.json` | request | `delete_client` | Delete `type` client |
| `DELETE/success.json` | response 200 | `success` | Empty string on success |
