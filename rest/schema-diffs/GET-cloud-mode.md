# GET `/cloud/mode` — schema difference

**Date:** 25 August 2026  
**operationId:** `getMode`  
**MQTT:** `get_mode`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path is the same**. Ours documents an optional GET body `{ "verbose": true }`. Developer GET has **no request body**. Nested GPI/antenna **port** enums are FXR docs polish.

---

## What is happening

| Spec | GET body |
|---|---|
| Developer | None. Always returns the current operating mode. |
| RestDeveloperfile | Optional `{ "verbose": true }` → full config including defaults. Omitted / `false` → configured values only. |

If firmware does not implement `verbose`, that body is docs-only and should not be published as a reader contract.

Nested response fields (same operatingMode object as PUT):

| Field | Developer | RestDeveloperfile |
|---|---|---|
| `antennaStopCondition[].value.port` | integer | integer enum `1`–`4` |
| `radioStartConditions.gpis[].port` | integer | integer enum `1`–`4` |
| `radioStopConditions.gpis[].port` | integer | integer enum `1`–`4` |

`tagMetaData[]` was flagged as changed by schema walk (string/object composition). Enum values match (RSSI, PHASE, ANTENNA, … plus `gpsCoordinates` object). Treat as a shape-walk noise unless a named enum actually diverges.

---

## Trees

### Request body — developer

None.

### Request body — RestDeveloperfile

```
GET /cloud/mode
└── verbose                     boolean   optional   true = include defaults
```

### 200 response — ports

```
antennaStopCondition / radioStartConditions / radioStopConditions
└── …port
        developer:          integer
        RestDeveloperfile:  1 | 2 | 3 | 4
```

---

## Examples

### RestDeveloperfile — full defaults

```json
{ "verbose": true }
```

### Developer

GET with no body.

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 1 | Only in RestDeveloperfile | GET body (`verbose`) |
| 4 | Changed | nested `port` enums (+ tagMetaData walk) |
| **5** | **Total** | (walk counted 6 including tagMetaData) |

---

## Docs work still to do (not applied yet)

Nothing has been merged into `RestDeveloperfile.yaml`. Confirm with firmware whether `verbose` is a real GET parameter. Nested port enums are FXR-facing docs and can stay if firmware only exposes ports 1–4. Then update overlays and rebuild if the GET body is dropped or kept.
