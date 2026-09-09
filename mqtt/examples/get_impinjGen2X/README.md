# `get_impinjGen2X`

REST: `GET /cloud/impinjGen2X` → `cloud-impinjgen2x/`

Stable `command_id`: `req-get-impinjGen2X`

GET returns the last saved feature only. Never-configured is an empty HTTP body, not `{}` — that case is not published as a JSON example.

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_impinjGen2X request |
| `response/fastID_disabled.json` | response | `fastID_disabled` | `cloud-impinjgen2x/GET/fastID_disabled.json` | Live 8 Sep 2026, FXR60 and FXR90 5.0.7 |
| `response/fastID_configured.json` | response | `fastID_configured` | `cloud-impinjgen2x/GET/fastID_configured.json` | Last PUT was FastID enabled |
| `response/tagFocus_configured.json` | response | `tagFocus_configured` | `cloud-impinjgen2x/GET/tagFocus_configured.json` | Last PUT was TagFocus |
| `response/tagProtect_configured.json` | response | `tagProtect_configured` | `cloud-impinjgen2x/GET/tagProtect_configured.json` | Last PUT was TagProtect |
| `response/tagQuieting_basic_configured.json` | response | `tagQuieting_basic_configured` | `cloud-impinjgen2x/GET/tagQuieting_basic_configured.json` | Last PUT was basic quieting |
| `response/tagQuieting_advanced_configured.json` | response | `tagQuieting_advanced_configured` | `cloud-impinjgen2x/GET/tagQuieting_advanced_configured.json` | Last PUT was advanced quieting |
