# PUT `/cloud/stop` — schema difference

**Date:** 25 August 2026  
**Updated:** 26 August 2026 (align to developer)  
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
| RestDeveloperfile | Same |

---

## Trees

### Developer

```
scanType (object)
└── *                           array   ble | rfid
```

### RestDeveloperfile

Same as developer.

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

## Docs work

**Align to developer.** Same as start: `additionalProperties` only. Example names: `stop_Global_*`, `stop_Targeted`.
