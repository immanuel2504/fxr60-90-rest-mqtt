# `get_gpsCoordinates`

REST: `GET /cloud/readerLocation` → `cloud-readerlocation/`

Stable `command_id`: `req-get-gpsCoordinates`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/default.json` | request | `default` | `—` | Empty get_gpsCoordinates request |
| `response/fix_acquired.json` | response | `fix_acquired` | `cloud-readerlocation/GET/fix_acquired.json` | GPS fix with latitude and longitude |
| `response/no_fix.json` | response | `no_fix` | `cloud-readerlocation/GET/no_fix.json` | No satellites locked |

