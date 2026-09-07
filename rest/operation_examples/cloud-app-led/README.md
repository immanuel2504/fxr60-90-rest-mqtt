# `/cloud/app-led`

- **GET** — `DEFAULT` / `NON_DEFAULT`
- **PUT** — set color, flash, seconds

Only live SUCCESS bodies from `pfx_server/rest/cloud-app-led-PUT`. Rejected cases are not published.

| Example name | File | Result |
|---|---|---|
| `amber_flash_60s` | `PUT/amber_flash_60s.json` | SUCCESS 200 |
| `red_flash_indefinite` | `PUT/red_flash_indefinite.json` | SUCCESS 200 |
| `green_solid_10s` | `PUT/green_solid_10s.json` | SUCCESS 200 |
| `off` | `PUT/off.json` | SUCCESS 200 |
| `success` | `PUT/success.json` | 200 empty body `""` |
