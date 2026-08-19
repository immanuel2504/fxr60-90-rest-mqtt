# Operation examples (reviewed-by-me format)

Examples for the final FXR60 / FXR90 REST API build. Layout matches
`FXR-Series/reviewed-by-me/cloud-app-led`.

```bash
python FXR60-90/scripts/FXR_60-90_api_rest_api.py
```

## Layout

One folder per endpoint path slug. Inside each endpoint, **methods are separate subfolders**:

```text
operation_examples/
  cloud-app-led/
    README.md
    SUMMARIES.md
    GET/
      default_reader_controls_led.json
      non_default_app_controls_led.json
    PUT/
      set_led.json
```

Each JSON file is a **bare payload** (not wrapped in OpenAPI `examples:`).

## Metadata

| File | Role |
|------|------|
| `SUMMARIES.md` | Example name + summary title for the Swagger dropdown |
| `README.md` | Why customers use each example |

The build reads `SUMMARIES.md` for OpenAPI `examples.<name>.summary`.  
If a file is missing from `SUMMARIES.md`, the filename stem is used.

## Behavior

- The build uses **only** these folders for Swagger examples.
- YAML `example` / `examples` from `RestDeveloperfile.yaml` are stripped first.
- Missing a pack/method folder for an operation is a **build error**.

## Conventions

- `GET/*.json` → response `200` examples
- `PUT|POST|PATCH/*.json` → request body examples (unless the summary starts with `Response:`)
- `DELETE/*.json` → response `200` by default
