# PUT `/cloud/certificates` — schema difference

**Date:** 25 August 2026  
**operationId:** `setUpdatecertificate`  
**MQTT:** `set_updateCertificate`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path is the same**. Certificate identity fields (`name`, `type`, `url`) are the same. HTTPS **download control** is not.

This is the same pattern as [PUT `/cloud/apps/install`](PUT-cloud-apps-install.md).

---

## What is happening

Firmware changed how download **credentials**, **retry**, and **timeouts** are sent.

| Client follows | Body keys | What the reader does |
|---|---|---|
|---|---|---|
| RestDeveloperfile | `authenticationOptions` | **Works** (same as install; `options` does not) |
| openAPISpec 10 | `options` | **Does not work** on the reader |

**3a Final:** keep `authenticationOptions`. Do not rename to `options`. See [DISCUSS-AND-FINALIZE.md](DISCUSS-AND-FINALIZE.md).

Required fields are unchanged: `url`, `type`, `name`.

---

## Runtime (developer spec)

```
PUT /cloud/certificates
        │
        ├── retry omitted
        │     → SYNCHRONOUS
        │     → download + install finish during this call
        │     → HTTPS, FTPS, SFTP
        │
        ├── retry present AND url is https://
        │     → ASYNCHRONOUS
        │     → API returns an immediate acknowledgment
        │     → final success/failure on the management events channel
        │     → retry.type must be randomWait
        │     → wait is random between policy.wait.min and policy.wait.max
        │
        └── retry present AND url is ftps:// or sftp://
              → async is not supported
              → do not send retry or timeouts
```

`RestDeveloperfile.yaml` does **not** document this sync/async split.

---

## Request-body tree — developer (`openAPISpec 10.yaml`)

```
PUT /cloud/certificates
├── url                         string   required   https:// | ftps:// | sftp://
├── type                        string   required   server | client | app
├── name                        string   required
├── authenticationType          string              NONE | BASIC
├── options                     object              BASIC credentials  [NEW KEY]
│   ├── username                string   required
│   └── password                string   required
├── pfxPassword                 string
├── transfer_protocol           string              HTTPS | FTPS | SFTP
├── verifyPeer / verifyHost     boolean
├── CACertificateFileLocation / Content
├── publicKeyFileLocation / Content
├── privateKeyFileLocation / Content
├── installedCertificateType / Name
├── headers                     object              named Authorization  [SHAPE CHANGED]
│   └── Authorization           string              Bearer JWT
├── retry                       object              HTTPS only; presence ⇒ async  [NEW SHAPE]
│   ├── type                    string              randomWait
│   └── policy
│       ├── retries             integer             1–50, default 1
│       └── wait
│           ├── min             integer             seconds, default 30
│           └── max             integer             seconds, default 300
└── timeouts                    object              HTTPS only  [NEW]
    ├── connection              integer             seconds, default 60
    └── read                    integer             seconds, default 600
```

---

## Request-body tree — RestDeveloperfile (current docs)

```
PUT /cloud/certificates
├── url / type / name           required (unchanged)
├── authenticationType          NONE | BASIC
├── authenticationOptions       object              [OLD KEY — not in developer]
│   ├── username / password
├── headers                     object              additionalProperties string
└── retry
    ├── count                   integer             [OLD SHAPE]
    └── delayInSec              integer             [OLD SHAPE]
```

No `timeouts`. No `retry.type` / `policy`.

---

## Field mapping

| RestDeveloperfile | Developer | Action |
|---|---|---|
| `authenticationOptions` | `options` | Rename |
| `retry.count` | `retry.policy.retries` | Rename + nest |
| `retry.delayInSec` | `retry.policy.wait.min` / `max` | Replace with random range |
| — | `retry.type` = `randomWait` | Add |
| — | `timeouts.connection` / `read` | Add |
| `headers` additionalProperties | `headers.Authorization` | Name the JWT header |

---

## Examples

### RestDeveloperfile (current)

```json
{
  "authenticationType": "BASIC",
  "authenticationOptions": {
    "username": "labuser",
    "password": "L@bu$3rs"
  },
  "name": "DOCK01",
  "pfxPassword": "password123456",
  "type": "client",
  "url": "sftp://10.117.229.15/data2/home/labuser/Certs/testuser-2026.pfx"
}
```

### Developer — synchronous (no `retry`)

```json
{
  "authenticationType": "BASIC",
  "options": {
    "username": "labuser",
    "password": "demo-password"
  },
  "name": "reader",
  "type": "client",
  "url": "https://example.com/certs/reader.pfx",
  "pfxPassword": "abcd12345"
}
```

### Developer — asynchronous (`retry` on HTTPS)

```json
{
  "authenticationType": "BASIC",
  "options": {
    "username": "labuser",
    "password": "demo-password"
  },
  "name": "reader",
  "type": "client",
  "url": "https://example.com/certs/reader.pfx",
  "retry": {
    "type": "randomWait",
    "policy": {
      "retries": 3,
      "wait": { "min": 60, "max": 600 }
    }
  },
  "timeouts": {
    "connection": 120,
    "read": 180
  }
}
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 4 | Added in developer | `options`, `retry.policy`, `retry.type`, `timeouts` |
| 3 | Only in RestDeveloperfile | `authenticationOptions`, `retry.count`, `retry.delayInSec` |
| 1 | Changed | `headers` |
| **8** | **Total** | |

---

## Docs work still to do (not applied yet)

1. **`authenticationOptions` stays** (3a Final). Do not rename to `options`.
2. **3b done.** Retry / timeouts / `headers.Authorization` aligned to developer.
