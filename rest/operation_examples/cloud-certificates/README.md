# `/cloud/certificates`

- **GET** — Installed certificates (`get_certificates`)
- **PUT** — Install a certificate (`set_updateCertificate`)

## GET examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `GET/lab_client_and_server.json` | response 200 | `lab_client_and_server` | Client `FXR60-LAB-CLIENT` and `Server` |

## PUT examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `PUT/https_basic.json` | request | `https_basic` | HTTPS BASIC download |
| `PUT/mtls.json` | request | `mtls` | HTTPS BASIC with installed client cert and CA |
| `PUT/success.json` | response 200 | `success` | Empty string on success |
