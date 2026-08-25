# GET `/cloud/network` — schema difference

**Date:** 25 August 2026  
**operationId:** `getNetwork`  
**MQTT:** `get_network`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path is the same**. Developer added an optional GET **request body** to return one interface. Response 802.1X enum **casing** also differs.

---

## What is happening

| Spec | GET behaviour |
|---|---|
| Developer | No body → all interfaces. Body `{ "interface": "<name>" }` → that interface only. |
| RestDeveloperfile | No GET body. Always all interfaces. |

Supported interface names in the developer body: `eth0`, `mlan0`, `bnep0`, `wan0`, `uap0`, `blescan`.

On the 200 response, ethernet `securityType` casing:

| Spec | Enum |
|---|---|
| Developer | `802_1xEAP` (lowercase x) |
| RestDeveloperfile | `802_1XEAP` (uppercase X) |

Same casing split as [PUT `/cloud/network`](PUT-cloud-network.md).

---

## Request-body tree — developer

```
GET /cloud/network
└── interface                   string   optional   eth0 | mlan0 | bnep0 | wan0 | uap0 | blescan
```

Omit the body (or send `{}`) to return every interface.

### RestDeveloperfile

No request body.

---

## Response field that changed

```
200.networkInterface.eth0.security.securityType
    developer:          802_1xEAP
    RestDeveloperfile:  802_1XEAP
```

---

## Examples

### Developer — all interfaces

```http
GET /cloud/network
```

or

```json
{}
```

### Developer — ethernet only

```json
{ "interface": "eth0" }
```

### RestDeveloperfile

GET with no body. No per-interface filter in the spec.

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 1 | Added in developer | request body (`interface`) |
| 1 | Changed | `securityType` enum casing |
| **2** | **Total** | |

---

## Docs work still to do (not applied yet)

Nothing has been merged into `RestDeveloperfile.yaml`. Align with the developer column when firmware is the source of truth, then update `rest/operation_descriptions/`, `rest/operation_examples/`, MQTT `openapi_md.json`, and rebuild.
