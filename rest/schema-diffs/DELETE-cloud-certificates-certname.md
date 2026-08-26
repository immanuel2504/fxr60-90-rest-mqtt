# DELETE `/cloud/certificates/{certname}` — schema difference

**Date:** 25 August 2026  
**operationId:** `delCertificate`  
**MQTT:** `del_certificate`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path is the same**. **Where `type` is sent is not.** Clients that follow the wrong place will fail.

Scenario-style walkthrough: [DELETE-certificate-type-location.md](DELETE-certificate-type-location.md)

---

## What is happening

Both specs require `type` = `client` or `app` (server certificates cannot be deleted). They disagree on the wire location:

| Spec | Where `type` goes |
|---|---|
| Developer | **Request body** `{ "type": "client" }` — **matches the reader (26 Aug 2026)** |
| RestDeveloperfile | **Request body** `{ "type": "client" }` (was query; now aligned) |

MQTT has no query string, so the developer REST body matches MQTT payload shape.

PUT refresh on the same path (`setRefreshcertificate`) already uses a body `{ "type": "server"|"client"|"app" }` in **both** files. Delete is the inconsistent one in RestDeveloperfile.

---

## Trees

### Developer — request body

```
DELETE /cloud/certificates/{certname}
└── body
    └── type                    string   required   client | app
```

No query parameter.

### RestDeveloperfile — query parameter

```
DELETE /cloud/certificates/{certname}?type=client
└── query
    └── type                    string   required   client | app
```

No request body.

---

## Examples

### Developer

```http
DELETE /cloud/certificates/mqtt-client-cert
Content-Type: application/json

{ "type": "client" }
```

### RestDeveloperfile

```http
DELETE /cloud/certificates/mqtt-client-cert?type=client
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 1 | Added in developer | request body `$` (`type`) |
| **1** | **Total** | |

The generator only saw the body. The matching RestDeveloperfile query param is the other half of the same change.

---

## Docs work still to do (not applied yet)

**5 Final (26 Aug 2026).** `type` is in the JSON body. Query `?type=` was removed. Build script keeps this DELETE body (does not convert it to query).
