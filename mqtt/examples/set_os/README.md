# `set_os`

REST: `PUT /cloud/os` → `cloud-os/`

Stable `command_id`: `req-set-os`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/os.json` | request | `os` | `cloud-os/PUT/os.json` | HTTPS OS update (NONE auth) |
| `request/os_https_retry.json` | request | `os_https_retry` | `cloud-os/PUT/os_https_retry.json` | HTTPS OS update with retry (always async) |
| `request/os_basic_auth.json` | request | `os_basic_auth` | `cloud-os/PUT/os_basic_auth.json` | HTTPS + BASIC |
| `request/os_scp.json` | request | `os_scp` | `cloud-os/PUT/os_scp.json` | SCP transfer |
| `request/os_https_pinned_ca.json` | request | `os_https_pinned_ca` | `cloud-os/PUT/os_https_pinned_ca.json` | HTTPS with pinned CA + retry |
| `response/success.json` | response | `success` | `—` | Command succeeded |

