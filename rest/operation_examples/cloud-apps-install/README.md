# `/cloud/apps/install`

- **PUT** — Install user application (`setInstalluserapp`)

Live examples from `pfx_server/app` (reader installed `sampleAntenna_1.0.4.deb` from `https://10.117.229.18/`).

| File | Example name | Auth |
|---|---|---|
| `PUT/app-install-basic.json` | `app-install-basic` | BASIC |
| `PUT/app-install-none.json` | `app-install-none` | NONE |
| `PUT/app-install-bearer.json` | `app-install-bearer` | NONE + Bearer header |
| `PUT/app-install-mtls.json` | `app-install-mtls` | BASIC + client cert + CA |
