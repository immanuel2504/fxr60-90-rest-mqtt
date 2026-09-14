# `get_impinjGen2X`

REST: `GET /cloud/impinjGen2X` → `cloud-impinjgen2x/`

GET returns the last saved feature only. Never-configured returns an empty body.

| File | Direction | Example name | Summary title |
|---|---|---|---|
| `request/get_configuration.json` | request | `get_configuration` | Get configuration |
| `response/never_configured.json` | response | `never_configured` | Never configured |
| `response/fastID_disabled.json` | response | `fastID_disabled` | FastID disabled |
| `response/fastID_configured.json` | response | `fastID_configured` | FastID enabled |
| `response/tagFocus_configured.json` | response | `tagFocus_configured` | TagFocus configured |
| `response/tagProtect_configured.json` | response | `tagProtect_configured` | TagProtect configured |
| `response/tagQuieting_basic_configured.json` | response | `tagQuieting_basic_configured` | Basic tag quieting |
| `response/tagQuieting_advanced_configured.json` | response | `tagQuieting_advanced_configured` | Advanced tag quieting |
