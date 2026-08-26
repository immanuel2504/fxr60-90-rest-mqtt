# PUT `/cloud/apps/{appname}/start` — schema difference

**Date:** 25 August 2026  
**Updated:** 26 August 2026 (device test)  
**operationId:** `setStartuserapp`  
**MQTT:** `set_startUserapp`  
**Decisions:** [DISCUSS-AND-FINALIZE.md](DISCUSS-AND-FINALIZE.md)

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

REST still uses path `{appname}`. Developer added a request body `{ "appname" }` so the **MQTT** payload is visible in the same OpenAPI file. Ours is path-only for local REST.

---

## What is happening

Developer description: for local REST, the app name is the path parameter; for MQTT, `appname` must be in the payload.

| Spec | REST body |
|---|---|
| Developer | `{ "appname": "mylogger" }` (optional for REST; required for MQTT) |
| RestDeveloperfile | none — path only |

Same pattern on [stop](PUT-cloud-apps-appname-stop.md) and [uninstall](PUT-cloud-apps-appname-uninstall.md). Autostart already has this body in **both** files.

---

## Trees

### Developer

```
PUT /cloud/apps/{appname}/start
└── appname                     string              MQTT payload; not needed for local REST
```

### RestDeveloperfile

Path `{appname}` only. No body.

---

## Examples

### Local REST (both)

```http
PUT /cloud/apps/mylogger/start
```

### MQTT / developer REST body

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

**Keep docs.** Device (26 Aug 2026): REST start works with no body. App name stays in the path. MQTT still uses payload `appname`.
