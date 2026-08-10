# FXR60-90 MQTT API (final)

Self-contained MQTT package for Swagger UI / API reference.

## Layout

```text
mqtt/
  openapi_md.json                  # applied OpenAPI (kept in sync with final)
  examples/<command>/{request,response}/*.json
  scripts/FXR_60-90_mqtt_api.py    # self-contained build (no repo imports)
  FXR_60-90_mqtt_api.json          # generated final
  tag_config.json                  # docs viewer support
  docs/                            # local API reference UI
    index.html
    swagger.html
    openapi_md.json
    css/ js/ assets/
  README.md
```

## Rebuild

```bash
.venv\Scripts\python.exe FXR60-90/mqtt/scripts/FXR_60-90_mqtt_api.py
```

Requires Python stdlib only.

Final build overlays `examples/` → writes `FXR_60-90_mqtt_api.json`, and syncs `openapi_md.json` + `docs/openapi_md.json`.

## View locally

Serve the package folder, then open:

- `docs/index.html` — custom reference viewer
- `docs/swagger.html` — Swagger UI
