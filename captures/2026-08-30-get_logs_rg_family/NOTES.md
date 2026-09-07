# get_logs_rgWarningLog / get_logs_rgErrorLog — live capture vs docs

## Compared against
- `mqtt/examples/get_rg_warn_logs/` and `mqtt/examples/get_rg_error_logs/` (previously marked "NEED LIVE TEST on a reader")
- `rest/operation_descriptions/getRgWarningLog.md`, `getRgErrorLog.md`
- `rest/FXR_60-90_rest_api.yaml` (`GetRgWarningLogResponse` / `GetRgErrorLogResponse` schemas)
- `mqtt/FXR_60-90_mqtt_api.json` (`/get_rg_warn_logs`, `/get_rg_error_logs` request/response schemas)

## Result: structure matches

Live response for `get_logs_rgWarningLog` matches the documented shape exactly:
- `command` = `get_logs_rgWarningLog` (enum-matched)
- `command_id` echoed back (`req-get-rg-warn-logs`)
- `response` = `success` (matches `success`/`failure` enum)
- `payload.binary` (string) + `payload.filename` (string) — both present, matches schema

`get_logs_rgErrorLog` request payload also matches the documented empty-payload request shape.

## Mismatch found: filename convention

- Docs/spec YAML example value: `rg_warning.log.gz` / `rg_error.log.gz` (snake_case, `.log.gz`)
- Live reader capture: `rgWarningLog.tar.gz` (camelCase, `.tar.gz`)
- Note the operation_descriptions prose already anticipated the camelCase form ("is a filename returned (for example, `rgWarningLog.tar.gz`)?"), so the prose and the live reader agree — only the YAML `example:` field under `GetRgWarningLogResponse`/`GetRgErrorLogResponse` (and the matching MQTT JSON example) is stale.

**Fixed 2026-08-30** — updated `filename` example values to `rgWarningLog.tar.gz` / `rgErrorLog.tar.gz` in:
- `rest/FXR_60-90_rest_api.yaml`, `rest/FXR_60-90_scalar_api.yaml` (`example:` blocks)
- `rest/operation_examples/cloud-logs-rgwarninglog/GET/download.json`, `rest/operation_examples/cloud-logs-rgerrorlog/GET/download.json`
- `mqtt/FXR_60-90_mqtt_api.json`, `mqtt/openapi_md.json`, `mqtt/docs/openapi_md.json` (`download` example `filename` values)
- `mqtt/examples/get_rg_warn_logs/response/download.json`, `mqtt/examples/get_rg_error_logs/response/download.json`

Not touched (per instruction): `rest/openAPISpec 10.yaml`, `rest/RestDeveloperfile.yaml`.

## Update — `get_logs_rgErrorLog` response now captured

Live response received: `filename` = `rgErrorLog.tar.gz`, matching the fix applied above (which was originally inferred by analogy, not yet confirmed at the time). Now confirmed correct by a real response. Both `RgWarningLog` and `RgErrorLog` are fully verified — request and response, both directions.

Not checking `binary` content byte-for-byte for this pair (out of scope per current instruction) — filename and envelope structure only.

## Files in this capture
- `mqtt/get_logs_rgWarningLog_response.json` — full live response (command/command_id/payload/response)
- `mqtt/get_logs_rgErrorLog_request.json` — live request
- `mqtt/get_logs_rgErrorLog_response.json` — full live response, confirms filename fix
