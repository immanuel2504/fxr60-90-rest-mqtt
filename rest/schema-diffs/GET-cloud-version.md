# GET `/cloud/version` — schema difference

**Date:** 25 August 2026  
**operationId:** `getVersion`  
**MQTT:** `get_version`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path is the same**. `model` enum is platform vs FXR-only. Upgrade objects are unconstrained vs `additionalProperties`.

---

## What is happening

| Field | Developer | RestDeveloperfile |
|---|---|---|
| `model` | `FXR90` \| `FX7500` \| `FX9600` \| `ATR7000` \| `FXR60` | `FXR60` \| `FXR90` |
| `availableOsUpgrades` | object | object + `additionalProperties: true` |
| `revertBackFirmware` | object | object + `additionalProperties: true` (empty on FXR) |

FXR docs correctly drop FX7500 / FX9600 / ATR7000 from `model`. That is product scope, not a firmware field change.

---

## Trees

```
model
    developer:          FXR90 | FX7500 | FX9600 | ATR7000 | FXR60
    RestDeveloperfile:  FXR60 | FXR90

availableOsUpgrades / revertBackFirmware
    developer:          object
    RestDeveloperfile:  object additionalProperties
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 3 | Changed | `model`, `availableOsUpgrades`, `revertBackFirmware` |
| **3** | **Total** | |

---

## Docs work still to do (not applied yet)

Nothing has been merged. Keep FXR-only `model` unless these docs must cover the shared platform.
