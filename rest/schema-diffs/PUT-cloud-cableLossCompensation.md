# PUT `/cloud/cableLossCompensation` — schema difference

**Date:** 25 August 2026  
**operationId:** `setCablelosscompensation`  
**MQTT:** `set_cableLossCompensation`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

Same `oneOf`: **All** ports vs **Each** port. Docs now match the developer Each-branch wrapper.

---

## What is happening

| Branch | Developer | RestDeveloperfile |
|---|---|---|
| All | `{ cableLength, cableLossPerHundredFt }` | same |
| Each | `patternProperties '^[1-8]$'` + `additionalProperties: false` | same |

---

## Trees (Each branch only)

### Developer

```
oneOf[1]                        object
└── pattern ^[1-8]$             { cableLength, cableLossPerHundredFt }
```

### RestDeveloperfile

Same as developer.

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

**Align to developer.** Each branch uses `patternProperties: '^[1-8]$'` and `additionalProperties: false`.
