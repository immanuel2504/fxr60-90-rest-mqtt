# Scalar REST API docs

Parallel Scalar track. Does **not** change the Swagger UI sources:

- `rest/RestDeveloperfile.yaml`
- `rest/operation_descriptions/*.md`
- `rest/FXR_60-90_rest_api.yaml`

## Layout

```text
rest/scalar/
  info.md                              # Scalar intro (info.description)
  operation_descriptions/*.md          # overlays Swagger descriptions by stem
  README.md
```

A file in `operation_descriptions/` is used **instead of** the matching Swagger markdown (`updateNetwork.md` overlays `rest/operation_descriptions/updateNetwork.md`). Operations with no Scalar file keep the existing Swagger description.

## Rebuild

```bash
python rest/scripts/FXR_60-90_api_scalar.py
```

**Output:** `rest/FXR_60-90_scalar_api.yaml`

YAML matches the Scalar Galaxy dump (`api-1.yaml`):

- `openapi: 3.1.1`
- `description: |` literal blocks (not quoted `\\n` strings)
- indented lists (`  - name:`)
- double-quoted `$ref` values
- `info.description` with a short Overview and Authentication section
- heading numbers stripped (`## 1. Description` → `## Description`)
- `servers` placeholder (`YOUR_READER_IP`) so the user can enter the reader address

Open that file in the [Scalar Swagger Editor](https://docs.scalar.com/swagger-editor).
