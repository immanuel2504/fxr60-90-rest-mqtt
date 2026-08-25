# GET `/cloud/stack-led` — schema difference

**Date:** 25 August 2026  
**operationId:** `getStackled`  
**MQTT:** `get_stackled`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path is the same**. Ours added **enums** that the developer file leaves as unconstrained strings. Not a new firmware field.

PUT `/cloud/stack-led` already documents the same color/brightness values in both files.

---

## What is happening

| Field | Developer | RestDeveloperfile |
|---|---|---|
| `status` | string (example `NON_DEFAULT`) | enum `DEFAULT` \| `NON_DEFAULT` |
| `color` | string (example `amber`) | enum `red` \| `amber` \| `green` \| `blue` \| `off` |
| `brightness` | string (example `high`) | enum `low` \| `med` \| `high` |

---

## Trees

```
status / color / brightness
    developer:          string
    RestDeveloperfile:  enums matching PUT /cloud/stack-led
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 3 | Changed | `status`, `color`, `brightness` |
| **3** | **Total** | |

---

## Docs work still to do (not applied yet)

Nothing has been merged. Enums are docs polish aligned with PUT. Keep them for FXR; they do not require a firmware schema change.
