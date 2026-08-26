# PUT `/cloud/apps/{appname}/pass-through` — schema difference

**Date:** 25 August 2026  
**Updated:** 26 August 2026 (align to developer)  
**operationId:** `setReqtouserapp`  
**MQTT:** `set_reqToUserapp`  
**Decisions:** [DISCUSS-AND-FINALIZE.md](DISCUSS-AND-FINALIZE.md)

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path is the same**. Docs now match the developer request body: `userapp` required, `command` optional.

---

## What is happening

Docs now match the developer spec.

| Field | Developer | RestDeveloperfile |
|---|---|---|
| `command` | object, **not** required | same |
| `userapp` | string, **required** | same |

---

## Trees

### Developer

```
PUT /cloud/apps/{appname}/pass-through
├── userapp                     string   required
└── command                     object
    └── message                 string
```

### RestDeveloperfile

Same as developer: `userapp` required, `command` optional.

---

## Examples

### Developer

```json
{
  "userapp": "mylogger",
  "command": { "message": "Hello World!!!" }
}
```

### Ours (now matches developer)

```json
{
  "userapp": "mylogger",
  "command": { "message": "Hello World!!!" }
}
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 2 | Changed | `command` required flag, `userapp` required flag |
| **2** | **Total** | |

---

## Docs work

**Align to developer.** Body requires `userapp`. `command` is optional. REST still uses `{appname}` in the path.
