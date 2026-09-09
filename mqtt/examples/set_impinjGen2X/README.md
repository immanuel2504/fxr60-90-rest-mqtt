# `set_impinjGen2X`

REST: `PUT /cloud/impinjGen2X` → `cloud-impinjgen2x/`

Stable `command_id`: `req-set-impinjGen2X`

All 12 request bodies were accepted live on 6 September 2026 (FXR60 5.0.7). Rejected combination and validation probes are not published.

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/enable_fastID.json` | request | `enable_fastID` | `cloud-impinjgen2x/PUT/enable_fastID.json` | Enable FastID (live 6 Sep 2026) |
| `request/disable_fastID.json` | request | `disable_fastID` | `cloud-impinjgen2x/PUT/disable_fastID.json` | Disable FastID (live 6 Sep 2026) |
| `request/protect_tag.json` | request | `protect_tag` | `cloud-impinjgen2x/PUT/protect_tag.json` | Protect tag (live 6 Sep 2026) |
| `request/unprotect_tag.json` | request | `unprotect_tag` | `cloud-impinjgen2x/PUT/unprotect_tag.json` | Unprotect tag (live 6 Sep 2026) |
| `request/enable_protect_read.json` | request | `enable_protect_read` | `cloud-impinjgen2x/PUT/enable_protect_read.json` | Enable protected-tag visibility (live 6 Sep 2026) |
| `request/disable_protect_read.json` | request | `disable_protect_read` | `cloud-impinjgen2x/PUT/disable_protect_read.json` | Disable protected-tag visibility (live 6 Sep 2026) |
| `request/enable_tagFocus.json` | request | `enable_tagFocus` | `cloud-impinjgen2x/PUT/enable_tagFocus.json` | Enable TagFocus (live 6 Sep 2026) |
| `request/disable_tagFocus.json` | request | `disable_tagFocus` | `cloud-impinjgen2x/PUT/disable_tagFocus.json` | Disable TagFocus (live 6 Sep 2026) |
| `request/quiet_tags.json` | request | `quiet_tags` | `cloud-impinjgen2x/PUT/quiet_tags.json` | Quiet tags by EPC list (live 6 Sep 2026) |
| `request/unquiet_tags.json` | request | `unquiet_tags` | `cloud-impinjgen2x/PUT/unquiet_tags.json` | Unquiet tags by EPC list (accepted 6 Sep 2026) |
| `request/advanced_quiet_tags.json` | request | `advanced_quiet_tags` | `cloud-impinjgen2x/PUT/advanced_quiet_tags.json` | Advanced quiet tags (live 6 Sep 2026) |
| `request/advanced_unquiet_tags.json` | request | `advanced_unquiet_tags` | `cloud-impinjgen2x/PUT/advanced_unquiet_tags.json` | Advanced unquiet tags (live 6 Sep 2026) |
| `response/success.json` | response | `success` | `cloud-impinjgen2x/PUT/response_200_success.json` | Response: Gen2X configured (apply on start) |
