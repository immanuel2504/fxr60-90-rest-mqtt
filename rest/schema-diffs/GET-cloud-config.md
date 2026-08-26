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
| `xml` | string — RFID operational XML profile (“Cloud Connect” RFID profile) | **Same (8a Final).** Optional when present. |
| `GPIO-LED` | string `"NOT_CONFIGURED"` when unset | **Keep `{}` (8b Final).** `allOf` GPIOLEDConfig object. |

READER-GATEWAY matches.

---

## Trees

### Developer 200

```
GET /cloud/config
├── xml                         string
├── GPIO-LED                    string              "NOT_CONFIGURED" when unset
└── READER-GATEWAY              object
```

### RestDeveloperfile 200

```
GET /cloud/config
├── xml                         string              optional Cloud Connect RFID profile
├── GPIO-LED                    object              GPIOLEDConfig; {} when unset
└── READER-GATEWAY              object
```

---

## Examples

### Developer — GPIO-LED not configured

```json
{ "GPIO-LED": "NOT_CONFIGURED" }
```

### RestDeveloperfile — GPIO-LED not configured (8b)

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

## Status

**8a Final.** Optional `xml` is in the docs (GET / MQTT `get_config`).  
**8b Final.** Device (26 Aug 2026): unset GPIO-LED is `{}`. Ask developer to drop `"NOT_CONFIGURED"`.
