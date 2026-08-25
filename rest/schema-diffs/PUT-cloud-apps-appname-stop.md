# PUT `/cloud/apps/{appname}/stop` — schema difference

**Date:** 25 August 2026  
**operationId:** `setStopuserapp`  
**MQTT:** `set_stopUserapp`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

Same as [start](PUT-cloud-apps-appname-start.md): developer REST body `{ "appname" }` for MQTT docs; ours is path-only.

---

## What is happening

| Spec | REST body |
|---|---|
| Developer | `{ "appname": "mylogger" }` |
| RestDeveloperfile | none |

---

## Trees

### Developer

```
PUT /cloud/apps/{appname}/stop
└── appname                     string              MQTT; not needed for local REST
```

### RestDeveloperfile

Path only.

---

## Examples

```http
PUT /cloud/apps/mylogger/stop
```

```json
{ "appname": "mylogger" }
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 1 | Added in developer | request body (`appname`) |
| **1** | **Total** | |

---

## Docs work still to do (not applied yet)

Nothing has been merged. Same decision as start/uninstall.
