# `/cloud/ntpServer`

- **GET** — Retrieve configured NTP server
- **PUT** — Set NTP server(s)

## GET example (single)

| File | Example name | Summary title |
|---|---|---|
| `GET/ntp_server.json` | `ntp_server` | Current NTP server |

See **`SUMMARIES.md`**.

## Rebuild

```bash
py -3 rest/scripts/FXR_60-90_api_rest_api.py
py -3 mqtt/scripts/FXR_60-90_mqtt_api.py
```
