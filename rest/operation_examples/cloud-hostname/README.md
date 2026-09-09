# `/cloud/hostName`

- **GET** — Retrieves the reader hostname (`get_hostName`). Response field is `hostName`.
- **PUT** — Sets the reader hostname (`set_hostName`). Request field is `hostname`.

## GET examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `GET/configured.json` | response 200 | `configured` | Current hostname |

## PUT examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `PUT/hostName.json` | request | `hostName` | Set hostname |
