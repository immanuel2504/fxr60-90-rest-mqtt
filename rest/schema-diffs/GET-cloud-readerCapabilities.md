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
| Developer GET | `DC` \| `POE` \| `POE+` \| `POWERBRICK` \| `BATTERY` |
| RestDeveloperfile | same |

FXR examples still show `POWERBRICK`, `POE`, `POE+`. `DC` is listed because the developer GET enum includes it.

Note: developer **components** schema for the same field is `DC` \| `POE` \| `POE+` \| `BATTERY` (no `POWERBRICK`). Our GET path and shared component keep `POWERBRICK` (as on the developer GET path) and now also include `DC`.

---

## Trees

```
capabilities.supportedPowerSource[]
    DC | POE | POE+ | POWERBRICK | BATTERY
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 1 | Changed | `supportedPowerSource[]` |
| **1** | **Total** | |

---

**Align to developer.** GET `supportedPowerSource` includes `DC`.
