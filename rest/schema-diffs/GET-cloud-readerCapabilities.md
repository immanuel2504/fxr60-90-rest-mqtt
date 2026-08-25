# GET `/cloud/readerCapabilities` — schema difference

**Date:** 25 August 2026  
**operationId:** `getReadercapabilities`  
**MQTT:** `get_readerCapabilities`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path is the same**. `capabilities.supportedPowerSource[]` enum differs.

---

## What is happening

On this GET operation’s inline schema:

| Spec | `supportedPowerSource` enum |
|---|---|
| Developer | `DC` \| `POE` \| `POE+` \| `POWERBRICK` \| `BATTERY` |
| RestDeveloperfile | `POE` \| `POE+` \| `POWERBRICK` \| `BATTERY` |

Ours dropped `DC` (FXR uses `PWR_BRICK` / `POWERBRICK`, not `DC` — see also [GET `/cloud/status`](GET-cloud-status.md)).

Note: developer **components** schema for the same field is `DC` \| `POE` \| `POE+` \| `BATTERY` (no `POWERBRICK`). The GET path and the shared component are not identical inside the developer file.

---

## Trees

```
capabilities.supportedPowerSource[]
    developer GET:      DC | POE | POE+ | POWERBRICK | BATTERY
    RestDeveloperfile:  POE | POE+ | POWERBRICK | BATTERY
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 1 | Changed | `supportedPowerSource[]` |
| **1** | **Total** | |

---

## Docs work still to do (not applied yet)

Nothing has been merged. Keep FXR enums unless these docs must list `DC` for shared-platform readers.
