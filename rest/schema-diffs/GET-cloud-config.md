# GET `/cloud/config` — schema difference

**Date:** 25 August 2026  
**operationId:** `getConfig`  
**MQTT:** `get_config`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path is the same**. Developer adds `xml` on the 200 body. GPIO-LED empty-state representation also differs.

---

## What is happening

| Field | Developer | RestDeveloperfile |
|---|---|---|
| `xml` | string — RFID operational XML profile (“Cloud Connect” RFID profile). Returned only on supported models (developer text mentions STARFISH/FX series). | not present |
| `GPIO-LED` | `oneOf`: string `"NOT_CONFIGURED"` when unset. (Developer GET schema does not `$ref` the full GPIOLEDConfig object in this oneOf.) | `allOf` `$ref` GPIOLEDConfig. Empty object `{}` when unset. |

READER-GATEWAY matches.

---

## Trees

### Developer 200

```
GET /cloud/config
├── xml                         string              [developer only]
├── GPIO-LED                    string              "NOT_CONFIGURED" when unset
└── READER-GATEWAY              object
```

### RestDeveloperfile 200

```
GET /cloud/config
├── GPIO-LED                    object              GPIOLEDConfig; {} when unset
└── READER-GATEWAY              object
```

---

## Examples

### Developer — GPIO-LED not configured

```json
{ "GPIO-LED": "NOT_CONFIGURED" }
```

### RestDeveloperfile — GPIO-LED not configured

```json
{ "GPIO-LED": {} }
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 1 | Added in developer | `xml` |
| 1 | Changed | `GPIO-LED` string vs object |
| **2** | **Total** | |

---

## Docs work still to do (not applied yet)

Nothing has been merged. Add `xml` if FXR firmware returns it. Confirm the unset GPIO-LED value (`"NOT_CONFIGURED"` vs `{}`) on a real reader before changing examples.
