# PUT `/cloud/cableLossCompensation` — schema difference

**Date:** 25 August 2026  
**operationId:** `setCablelosscompensation`  
**MQTT:** `set_cableLossCompensation`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

Same `oneOf`: **All** ports vs **Each** port. The “Each” branch wrapper differs (`patternProperties` vs `cableLossPort.v1`).

---

## What is happening

| Branch | Developer | RestDeveloperfile |
|---|---|---|
| All | `{ cableLength, cableLossPerHundredFt }` | same |
| Each | `patternProperties '^[1-8]$'` + `additionalProperties: false` | `additionalProperties` → `cableLossPort.v1` |

JSON a client sends is the same.

---

## Trees (Each branch only)

### Developer

```
oneOf[1]                        object
└── pattern ^[1-8]$             { cableLength, cableLossPerHundredFt }
```

### RestDeveloperfile

```
oneOf[1]                        object additionalProperties
└── *                           $ref cableLossPort.v1
```

---

## Examples (both)

All ports:

```json
{ "cableLength": 90, "cableLossPerHundredFt": 18 }
```

Per port:

```json
{
  "1": { "cableLength": 90, "cableLossPerHundredFt": 18 },
  "2": { "cableLength": 18, "cableLossPerHundredFt": 19 }
}
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 1 | Changed | `oneOf[1]` wrapper |
| **1** | **Total** | |

---

## Docs work still to do (not applied yet)

Nothing has been merged. Wrapper-only, same as GET.
