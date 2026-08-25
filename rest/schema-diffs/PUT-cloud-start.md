# PUT `/cloud/start` — schema difference

**Date:** 25 August 2026  
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

| Spec | Targeted object keys |
|---|---|
| Developer | Any endpoint name (`additionalProperties` of `ble`/`rfid` arrays). Example uses `dataEndpoint1` / `dataEndpoint2`. |
| RestDeveloperfile | Same `additionalProperties`, **plus** named properties `dataEndpoint1` / `dataEndpoint2`. Extra targeted examples (BLE-only, RFID-only, mixed). |

Clients sending `dataEndpoint1` / `dataEndpoint2` match both. Other connection names are valid in the developer schema; ours documents the two default names explicitly.

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

```
scanType                        array | object
└── (object)
    ├── dataEndpoint1           array   ble | rfid     [named]
    ├── dataEndpoint2           array   ble | rfid     [named]
    └── *                       array   ble | rfid     additionalProperties
```

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

## Docs work still to do (not applied yet)

Nothing has been merged. Named `dataEndpoint1` / `dataEndpoint2` can stay as documentation of the default connections if firmware still uses those names. Align example names with the developer file if you want YAML parity.
