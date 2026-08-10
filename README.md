# FXR60-90 API packages

Self-contained final packages for **REST** and **MQTT** (FXR60 / FXR90).

For full session history and decisions, see **[CONTEXT.md](CONTEXT.md)**.

```text
FXR60-90/
  rest/       # REST OpenAPI package (includes RestDeveloperfile.yaml + build helpers)
  mqtt/       # MQTT OpenAPI package (self-contained build script + docs UI)
  README.md
  CONTEXT.md  # what happened / current state
```

## REST

```bash
.venv\Scripts\python.exe FXR60-90/rest/scripts/FXR_60-90_api_rest_api.py
```

Needs: Python + `PyYAML`.  
Sources are inside `rest/` (`RestDeveloperfile.yaml`, descriptions, examples).

See `rest/README.md`.

## MQTT

```bash
.venv\Scripts\python.exe FXR60-90/mqtt/scripts/FXR_60-90_mqtt_api.py
```

Needs: Python stdlib only.  
Sources are inside `mqtt/` (`openapi_md.json`, `examples/`).

See `mqtt/README.md`.
