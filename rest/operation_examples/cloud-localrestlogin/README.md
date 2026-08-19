# `/cloud/localRestLogin`

- **GET only** — Reader login (HTTP Basic Auth → bearer token)
- REST-only (no MQTT equivalent)

## GET example (single)

| File | Example name | Summary title |
|---|---|---|
| `GET/login_success.json` | `login_success` | Bearer token returned |

See **`SUMMARIES.md`**.

## Rebuild

```bash
py -3 rest/scripts/FXR_60-90_api_rest_api.py
```
