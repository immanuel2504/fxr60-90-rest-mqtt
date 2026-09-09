# `set_eSimConfig`

REST: `PUT /cloud/eSimConfig` → `cloud-esimconfig/`

Stable `command_id`: `req-set-eSimConfig`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/enable_profile.json` | request | `enable_profile` | `cloud-esimconfig/PUT/enable_profile.json` | `operation` enable |
| `request/disable_profile.json` | request | `disable_profile` | `cloud-esimconfig/PUT/disable_profile.json` | `operation` disable |
| `request/add_profile.json` | request | `add_profile` | `cloud-esimconfig/PUT/add_profile.json` | `operation` add with `activationID` |
| `request/delete_profile.json` | request | `delete_profile` | `cloud-esimconfig/PUT/delete_profile.json` | `operation` delete |
| `response/success.json` | response | `success` | `—` | Empty payload on success |
