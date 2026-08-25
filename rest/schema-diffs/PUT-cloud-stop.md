# PUT `/cloud/stop` — schema difference

**Date:** 25 August 2026  
**operationId:** `stopInventory`  
**MQTT:** `stop`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

Same `scanType` shape difference as [PUT `/cloud/start`](PUT-cloud-start.md).

---

## What is happening

| Spec | Targeted `scanType` object |
|---|---|
| Developer | Any endpoint name (`additionalProperties`). |
| RestDeveloperfile | Named `dataEndpoint1` / `dataEndpoint2` plus the same `additionalProperties`. |

---

## Trees

### Developer

```
scanType (object)
└── *                           array   ble | rfid
```

### RestDeveloperfile

```
scanType (object)
├── dataEndpoint1               array   ble | rfid
├── dataEndpoint2               array   ble | rfid
└── *                           array   ble | rfid
```

---

## Example (both)

```json
{
  "scanType": {
    "dataEndpoint1": ["ble", "rfid"],
    "dataEndpoint2": ["rfid"]
  }
}
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 2 | Only in RestDeveloperfile | `dataEndpoint1`, `dataEndpoint2` |
| 1 | Changed | `scanType` object `*` |
| **3** | **Total** | |

---

## Docs work still to do (not applied yet)

Nothing has been merged. Same decision as start: keep named endpoints as FXR docs, or drop them and rely on `additionalProperties` only.
