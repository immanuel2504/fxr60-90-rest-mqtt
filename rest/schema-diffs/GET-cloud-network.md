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
| RestDeveloperfile | **Same (7a Final).** Response `securityType` stays `802_1XEAP`. |

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

Same optional `interface` body as the developer spec. Response `securityType` stays `802_1XEAP`.

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

Same as developer: omit body / `{}` for all interfaces, or `{ "interface": "eth0" }` for one.

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 1 | Added in developer | request body (`interface`) |
| 1 | Changed | `securityType` enum casing |
| **2** | **Total** | |

---

## Status

**7a Final.** Optional GET / MQTT body `{ "interface": "<name>" }` is in the docs.  
**7b Final.** Response `securityType` stays `802_1XEAP`.
