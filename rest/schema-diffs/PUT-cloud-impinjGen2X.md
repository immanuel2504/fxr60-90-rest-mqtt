# PUT `/cloud/impinjGen2X` — schema difference

**Date:** 25 August 2026  
**operationId:** `setImpinjGen2X`  
**MQTT:** `set_impinjGen2X`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **request schema matches**. The **200 success body** does not.

---

## What is happening

| Spec | 200 body |
|---|---|
| Developer | empty string `""` |
| RestDeveloperfile | object `{ "message": "Success: Gen2X configured. …" }` required |

Request features (fastID, tagProtect, tagFocus, tagQuieting) are the same. Ours added a confirmation message so Swagger/Scalar can show what “applied on next start” means.

---

## Trees

### Developer 200

```
""                              string
```

### RestDeveloperfile 200

```
message                         string   required
```

---

## Examples

### Developer

```json
""
```

### RestDeveloperfile

```json
{
  "message": "Success: Gen2X configured. Use applyImpinjGen2X flag in start command to apply features."
}
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 1 | Only in RestDeveloperfile | `message` |
| **1** | **Total** | |

---

## Docs work still to do (not applied yet)

Nothing has been merged. Keep the message only if firmware actually returns that JSON. If the reader returns `""`, align RestDeveloperfile with developer.
