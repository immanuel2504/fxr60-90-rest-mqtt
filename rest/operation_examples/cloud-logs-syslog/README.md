# `/cloud/logs/syslog`

- **GET** — System log archive (`get_logs_syslog`)
- **DELETE** — Delete stored syslog files (`del_logs_syslog`)

## GET examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `GET/syslog.json` | response 200 | `syslog` | syslog.tar.gz archive |

## DELETE examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `DELETE/success.json` | response 200 | `success` | Empty string on success |
