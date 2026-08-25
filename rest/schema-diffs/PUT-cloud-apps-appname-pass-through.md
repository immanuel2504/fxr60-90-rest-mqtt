# PUT `/cloud/apps/{appname}/pass-through` — schema difference

**Date:** 25 August 2026  
**operationId:** `setReqtouserapp`  
**MQTT:** `set_reqToUserapp`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path is the same**. **Which body field is required** disagrees.

---

## What is happening

| Field | Developer | RestDeveloperfile |
|---|---|---|
| `command` | object, **not** required | object, **required** |
| `userapp` | string, **required** | string, optional (MQTT only; REST uses `{appname}`) |

Developer requires `userapp` even on REST (redundant with the path). Ours requires `command` and treats `userapp` as MQTT-only.

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

```
PUT /cloud/apps/{appname}/pass-through
├── command                     object   required
│   └── message                 string
└── userapp                     string              MQTT only
```

---

## Examples

### Developer

```json
{
  "userapp": "mylogger",
  "command": { "message": "Hello World!!!" }
}
```

### RestDeveloperfile

```json
{
  "command": { "message": "status" }
}
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 2 | Changed | `command` required flag, `userapp` required flag |
| **2** | **Total** | |

---

## Docs work still to do (not applied yet)

Nothing has been merged. For local REST, requiring `command` and ignoring `userapp` matches how autostart documents MQTT vs path. Confirm with firmware whether REST rejects a body that omits `userapp`.
