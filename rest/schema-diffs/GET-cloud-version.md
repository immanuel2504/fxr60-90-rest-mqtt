# GET `/cloud/version` — schema difference

**Date:** 25 August 2026  
**Updated:** 26 August 2026 (align to developer)  
**operationId:** `getVersion`  
**MQTT:** `get_version`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path is the same**. Docs now match the developer spec.

---

## What is happening

| Field | Developer | RestDeveloperfile |
|---|---|---|
| `model` | `FXR90` \| `FX7500` \| `FX9600` \| `ATR7000` \| `FXR60` | same |
| `availableOsUpgrades` | object | same |
| `revertBackFirmware` | object | same |

---

## Trees

```
model                           FXR90 | FX7500 | FX9600 | ATR7000 | FXR60
availableOsUpgrades             object
revertBackFirmware              object
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 3 | Changed | `model`, `availableOsUpgrades`, `revertBackFirmware` |
| **3** | **Total** | |

---

## Docs work

**Align to developer.** `model` includes `FXR90`, `FX7500`, `FX9600`, `ATR7000`, `FXR60`. `availableOsUpgrades` and `revertBackFirmware` are plain objects.
