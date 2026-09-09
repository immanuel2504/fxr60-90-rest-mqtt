# `/cloud/caCertificates`

- **GET** — List CA certificates (`get_CACertificates`)
- **PUT** — Install a CA certificate (`set_InstallCACertificate`)
- **DELETE** — Delete a CA certificate (`del_CACertificate`)

## GET examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `GET/empty_list.json` | response 200 | `empty_list` | No CA certificates |
| `GET/ca_list.json` | response 200 | `ca_list` | CA names with `.crt` |

## PUT examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `PUT/install_ca.json` | request | `install_ca` | Install a CA (`name` + PEM `content`) |
| `PUT/success.json` | response 200 | `success` | Empty string on success |

## DELETE examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `DELETE/delete_ca.json` | request | `delete_ca` | Delete by install name, without `.crt` |
| `DELETE/success.json` | response 200 | `success` | Empty string on success |
