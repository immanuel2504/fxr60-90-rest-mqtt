# FXR60-90 REST API (final)

Self-contained REST package for Swagger UI.

## Layout

```text
rest/
  RestDeveloperfile.yaml           # source schemas + paths (copied into package)
  operation_descriptions/*.md
  operation_examples/<path>/<METHOD>/*.json
  scripts/
    FXR_60-90_api_rest_api.py      # package build
    build_fxr90_rest_api.py        # local helpers (copied into package)
  FXR_60-90_rest_api.yaml          # generated (do not edit)
  README.md
```

## Rebuild

```bash
.venv\Scripts\python.exe FXR60-90/rest/scripts/FXR_60-90_api_rest_api.py
```

Requires Python + `PyYAML`.

| Source | Role |
|--------|------|
| `RestDeveloperfile.yaml` | schemas + paths |
| `operation_descriptions/*.md` | operation descriptions |
| `operation_examples/<path>/<METHOD>/*.json` | Swagger examples |

**Output:** `FXR_60-90_rest_api.yaml`
