# GET `/cloud/mode` — schema difference

**Date:** 25 August 2026  
**Updated:** 26 August 2026 (device test)  
**operationId:** `getMode`  
**MQTT:** `get_mode`  
**Decisions:** [DISCUSS-AND-FINALIZE.md](DISCUSS-AND-FINALIZE.md)

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

**Device test (26 August 2026):** sending `{ "verbose": true }` on GET `/cloud/mode` **works**. Keep `verbose` in our docs. Ask the developer to add it to their spec.

Nested response fields (same operatingMode object as PUT):

| Field | Developer | RestDeveloperfile |
|---|---|---|
| `antennaStopCondition[].value.port` | integer (GPI schema max **2**) | integer enum `1`–`4` |
| `radioStartConditions.gpis[].port` | integer (GPI schema max **2**) | integer enum `1`–`4` |
| `radioStopConditions.gpis[].port` | integer (GPI schema max **2**) | integer enum `1`–`4` |

GET `/cloud/gpi` in the same developer file already has ports 1–4. Our docs keep 1–4 until firmware answers.

`tagMetaData`: same names except our docs also list **`READER_LOCATION`** (developer YAML does not). Keep it until they answer.

Copy-paste questions: [DISCUSS-AND-FINALIZE.md](DISCUSS-AND-FINALIZE.md).

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

`verbose` stays. Ports stay 1–4. `READER_LOCATION` stays. Nothing merged until rows in [DISCUSS-AND-FINALIZE.md](DISCUSS-AND-FINALIZE.md) are Final.
