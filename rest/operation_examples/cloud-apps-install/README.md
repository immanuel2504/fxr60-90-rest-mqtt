# `/cloud/apps/install`

- **PUT** — Install a user application (`set_installUserapp`)

## PUT examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `PUT/app-install-none.json` | request | `app-install-none` | HTTPS `NONE` |
| `PUT/app-install-basic.json` | request | `app-install-basic` | HTTPS `BASIC` |
| `PUT/app-install-bearer.json` | request | `app-install-bearer` | HTTPS `NONE` with `Authorization` |
| `PUT/app-install-mtls.json` | request | `app-install-mtls` | HTTPS `BASIC` with installed cert and CA |
| `PUT/sftp_basic.json` | request | `sftp_basic` | SFTP `BASIC` |
| `PUT/success.json` | response 200 | `success` | Empty string on success |
