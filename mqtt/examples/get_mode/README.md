# `get_mode`

REST: `GET /cloud/mode` → `cloud-mode/`

Stable `command_id`: `req-get-mode`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/verbose_false.json` | request | `verbose_false` | `cloud-mode/GET/verbose_false_request.json` | Configured values only |
| `request/verbose_true.json` | request | `verbose_true` | `cloud-mode/GET/verbose_true_request.json` | Full configuration including defaults |
| `response/verbose_false.json` | response | `verbose_false` | `cloud-mode/GET/verbose_false.json` | CUSTOM configured values only |
| `response/verbose_true.json` | response | `verbose_true` | `cloud-mode/GET/verbose_true.json` | INVENTORY full configuration |
| `response/SIMPLE.json` | response | `SIMPLE` | `cloud-mode/GET/SIMPLE.json` | SIMPLE |
| `response/INVENTORY.json` | response | `INVENTORY` | `cloud-mode/GET/INVENTORY.json` | INVENTORY |
| `response/PORTAL.json` | response | `PORTAL` | `cloud-mode/GET/PORTAL.json` | PORTAL |
| `response/CONVEYOR.json` | response | `CONVEYOR` | `cloud-mode/GET/CONVEYOR.json` | CONVEYOR |
| `response/CUSTOM.json` | response | `CUSTOM` | `cloud-mode/GET/CUSTOM.json` | CUSTOM |
