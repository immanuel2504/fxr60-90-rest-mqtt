# `/cloud/app-led`

- **GET** — application LED status (`DEFAULT` / `NON_DEFAULT`)
- **PUT** — set color / flash / duration

## PUT examples

| File | Direction | Example name | Summary title |
|---|---|---|---|
| `PUT/app_led.json` | request | `app_led` | Amber blink for 60 seconds |
| `PUT/success.json` | response 200 | `success` | Empty string on success |

Swagger may show `"string"` as a placeholder when no response example is present — that is **not** the real body. Docs now show `""`.

**NEED LIVE TEST:** Run `PUT /cloud/app-led` on a real reader and confirm the 200 body is really `""`.

## GET examples

| File | Example name | Summary title |
|---|---|---|
| `GET/default_state.json` | `default_state` | Reader controls LED |
| `GET/overridden_state.json` | `overridden_state` | App controls LED |

See **`SUMMARIES.md`**.
