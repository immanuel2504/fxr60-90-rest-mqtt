# `set_passthru`

REST: `PUT /cloud/pass-through` → `cloud-pass-through/`

| File | Direction | Example | Summary |
|---|---|---|---|
| `request/status.json` | request | `status` | RC status command |
| `request/passthru.json` | request | `passthru` | RC mode command |
| `response/success.json` | response | `success` | RC status reply (pairs with `request/status.json`) |
| `response/mode_success.json` | response | `mode_success` | RC mode reply (pairs with `request/passthru.json`) |
