# GET `/cloud/cableLossCompensation` — schema difference

**Date:** 25 August 2026  
**operationId:** `getCablelosscompensation`  
**MQTT:** `get_cableLossCompensation`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path and JSON values are the same**. How per-port objects are declared in OpenAPI differs.

---

## What is happening

Both return a map keyed by read-point `"1"` … `"8"` with `cableLength` and `cableLossPerHundredFt`.

| Spec | How the map is typed |
|---|---|
| Developer | `patternProperties: '^[1-8]$'` + `additionalProperties: false` |
| RestDeveloperfile | `additionalProperties` → helper schema `cableLossPort.v1` |

Same numbers. Ours is easier to `$ref` from PUT. Not a client-breaking field change.

---

## Trees

### Developer 200

```
{ "1" | "2" | … | "8" }
└── object required [cableLength, cableLossPerHundredFt]
```

### RestDeveloperfile 200

```
*  (additionalProperties)
└── $ref cableLossPort.v1   required [cableLength, cableLossPerHundredFt]
```

---

## Example (both)

```json
{
  "1": { "cableLength": 10, "cableLossPerHundredFt": 10 },
  "2": { "cableLength": 10, "cableLossPerHundredFt": 10 }
}
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 1 | Only in RestDeveloperfile | `*` → `cableLossPort.v1` |
| **1** | **Total** | |

---

## Docs work still to do (not applied yet)

Nothing has been merged. Wrapper-only. Keep `cableLossPort.v1` unless you need byte-for-byte OpenAPI parity with `patternProperties`.
