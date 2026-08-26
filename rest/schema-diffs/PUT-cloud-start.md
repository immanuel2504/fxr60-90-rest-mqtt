# PUT `/cloud/start` — schema difference

**Date:** 25 August 2026  
**Updated:** 26 August 2026 (align to developer)  
**operationId:** `startInventory`  
**MQTT:** `start`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path is the same**. Both support `scanType` as an **array** (global) or an **object** (per data endpoint). Developer leaves object keys open (`additionalProperties`). Ours also **names** `dataEndpoint1` and `dataEndpoint2`.

---

## What is happening

Behaviour is the same: omit `scanType` → RFID only; array → same scan types on every data endpoint; object → scan types per endpoint name.

Docs now match the developer spec.

| Spec | Targeted object keys |
|---|---|
| Developer | Any endpoint name (`additionalProperties` of `ble`/`rfid` arrays). Example uses `dataEndpoint1` / `dataEndpoint2`. |
| RestDeveloperfile | Same |

Do not document `nw-mngr` / `ipc:///tmp/nw-mngr-data-pub` as public endpoint names.

---

## Trees

### Developer — `scanType` object branch

```
scanType                        array | object
└── (object)
    └── *                       array   ble | rfid     additionalProperties
```

### RestDeveloperfile — `scanType` object branch

Same as developer: `additionalProperties` only.

---

## Examples

Both accept:

```json
{ "scanType": ["ble", "rfid"] }
```

```json
{
  "scanType": {
    "dataEndpoint1": ["ble", "rfid"],
    "dataEndpoint2": ["rfid"]
  }
}
```

YAML example **names** differ (`start_Global_BLE_only` vs `start_BLE_only`). That is overlay/example naming, not a schema field.

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 2 | Only in RestDeveloperfile | `dataEndpoint1`, `dataEndpoint2` |
| 1 | Changed | `scanType` object `*` |
| **3** | **Total** | |

---

## Docs work

**Align to developer.** Targeted `scanType` is `additionalProperties` only. Named `dataEndpoint1` / `dataEndpoint2` stay as examples, not schema properties. Example names: `start_Global_*`, `start_Targeted`.
