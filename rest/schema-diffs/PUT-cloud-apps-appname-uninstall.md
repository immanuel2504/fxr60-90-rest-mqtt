# PUT `/cloud/apps/{appname}/uninstall` — schema difference

**Date:** 25 August 2026  
**operationId:** `setUninstalluserapp`  
**MQTT:** `set_uninstallUserapp`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

Same as [start](PUT-cloud-apps-appname-start.md) / [stop](PUT-cloud-apps-appname-stop.md): developer added body `{ "appname" }`; ours is path-only.

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
PUT /cloud/apps/{appname}/uninstall
└── appname                     string              MQTT; not needed for local REST
```

### RestDeveloperfile

Path only.

---

## Examples

```http
PUT /cloud/apps/mylogger/uninstall
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

## Docs work

**Keep docs.** Same as start (10): REST is path only. No body.
