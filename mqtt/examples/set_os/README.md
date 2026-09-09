# `set_os`

REST: `PUT /cloud/os` → `cloud-os/`

Stable `command_id`: `req-set-os`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/https_none.json` | request | `https_none` | `cloud-os/PUT/https_none.json` | `authenticationType` NONE |
| `request/https_basic.json` | request | `https_basic` | `cloud-os/PUT/https_basic.json` | `authenticationType` BASIC |
| `request/https_basic_retry.json` | request | `https_basic_retry` | `cloud-os/PUT/https_basic_retry.json` | `BASIC` with `retry` and `timeouts` |
| `response/success.json` | response | `success` | `—` | Empty payload on success |
