# `/cloud/gpi`

- **GET only** — Retrieves GPI (input) pin states 1–4  
- No PUT on this path

## GET example (single)

| File | Example name | Summary title |
|---|---|---|
| `GET/gpi_status.json` | `gpi_status` | Current GPI pin states |

Matches GPO style (`gpo_status`).

See **`SUMMARIES.md`**.

## Rebuild

```bash
py -3 rest/scripts/FXR_60-90_api_rest_api.py
py -3 mqtt/scripts/FXR_60-90_mqtt_api.py
```
