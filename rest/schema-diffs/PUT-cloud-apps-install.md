# PUT `/cloud/apps/install` — schema difference

**Date:** 25 August 2026  
**Updated:** 26 August 2026 (device test)  
**operationId:** `setInstalluserapp`  
**MQTT:** `set_installUserapp`  
**Decisions:** [DISCUSS-AND-FINALIZE.md](DISCUSS-AND-FINALIZE.md)

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path is the same**. The **request-body schema for HTTPS download control is not**.

---

## What is happening

The reader still installs a user application from `url` using `filename`. Firmware changed how download **credentials**, **retry**, and **timeouts** are sent.

| Client follows | Body keys | What the reader does |
|---|---|---|
| RestDeveloperfile | `options` | **Works** (HTTPS install, later 26 Aug 2026) |
| openAPISpec 10 | `options` | **Works** |

Install (2a + 2b): aligned to developer. BASIC credentials are `options`. Certificates and OS still use `authenticationOptions` — [DISCUSS-AND-FINALIZE.md](DISCUSS-AND-FINALIZE.md).

Required fields are unchanged in both files: `url`, `filename`, `authenticationType`.

---

## Runtime (developer spec)

```
PUT /cloud/apps/install
        │
        ├── retry omitted
        │     → SYNCHRONOUS
        │     → download + install finish during this call
        │     → HTTP 200 is the final result (empty string)
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

`RestDeveloperfile.yaml` does **not** document this sync/async split. It only describes a flat `retry.count` / `retry.delayInSec` object.

---

## Request-body tree — developer (`openAPISpec 10.yaml`)

```
PUT /cloud/apps/install
├── authenticationType          string   required   NONE | BASIC
├── options                     object              BASIC credentials  [NEW KEY]
│   ├── username                string   required
│   └── password                string   required
├── filename                    string   required
├── url                         string   required
├── verifyPeer                  boolean
├── verifyHost                  boolean
├── CACertificateFileLocation   string
├── CACertificateFileContent    string
├── publicKeyFileLocation       string
├── publicKeyFileContent        string
├── privateKeyFileLocation      string
├── privateKeyFileContent       string
├── installedCertificateType    string
├── installedCertificateName    string
├── headers                     object              named Authorization  [SHAPE CHANGED]
│   └── Authorization           string              Bearer JWT
├── retry                       object              HTTPS only; presence ⇒ async  [NEW SHAPE]
│   ├── type                    string              enum: randomWait
│   └── policy                  object
│       ├── retries             integer             1–50, default 1
│       └── wait                object
│           ├── min             integer seconds     0–3600, default 30
│           └── max             integer seconds     1–3600, default 300
└── timeouts                    object              HTTPS only  [NEW]
    ├── connection              integer seconds     1–3600, default 60
    └── read                    integer seconds     1–3600, default 600
```

200 response: empty string `""` (same as ours).

---

## Request-body tree — ours (`RestDeveloperfile.yaml`)

Now matches developer: `options`, `retry.type` / `retry.policy`, `timeouts`, named `headers.Authorization`.

---

## Field mapping

| Developer JSON path | RestDeveloperfile JSON path | Notes |
|---|---|---|
| `options` | `options` | Same. Device (HTTPS, later 26 Aug 2026) accepts `options` |
| `options.username` | `options.username` | Same |
| `options.password` | `options.password` | Same |
| `retry.type` | — | New. Must be `randomWait` |
| `retry.policy.retries` | `retry.count` | Closest old field |
| `retry.policy.wait.min` | `retry.delayInSec` | Not 1:1. Old = fixed delay. New = random range |
| `retry.policy.wait.max` | — | New |
| `timeouts.connection` | — | New, HTTPS only |
| `timeouts.read` | — | New, HTTPS only |
| `headers.Authorization` | `headers` additionalProperties | Developer names the Authorization header |

Unchanged in both:

`authenticationType`, `filename`, `url`, `verifyPeer`, `verifyHost`, `CACertificateFileLocation`, `CACertificateFileContent`, `publicKeyFileLocation`, `publicKeyFileContent`, `privateKeyFileLocation`, `privateKeyFileContent`, `installedCertificateType`, `installedCertificateName`.

---

## Example bodies

### Ours (current RestDeveloperfile)

```json
{
  "authenticationType": "BASIC",
  "options": {
    "username": "labuser",
    "password": "L@bu$3rs"
  },
  "filename": "mylogger_1.0.1.deb",
  "url": "sftp://10.117.229.15/home/labuser/EV1/"
}
```

Async HTTPS example: `installUserapp_async.json` (`retry` + `timeouts`).

### Developer — synchronous (no `retry`)

```json
{
  "authenticationType": "BASIC",
  "options": {
    "username": "demo-user",
    "password": "demo-password"
  },
  "filename": "sample-app.deb",
  "url": "https://example.com/packages/sample-app.deb"
}
```

### Developer — asynchronous (`retry` on HTTPS)

```json
{
  "authenticationType": "BASIC",
  "options": {
    "username": "demo-user",
    "password": "demo-password"
  },
  "filename": "sample-app.deb",
  "url": "https://example.com/packages/sample-app.deb",
  "retry": {
    "type": "randomWait",
    "policy": {
      "retries": 3,
      "wait": { "min": 10, "max": 30 }
    }
  },
  "timeouts": {
    "connection": 5,
    "read": 20
  }
}
```

---

## Spreadsheet row (what the 8 means)

From `FXR-REST-Schema-by-endpoint_2026-08-25.xlsx`:

| Count | Kind | Fields |
|---:|---|---|
| 4 | Added in developer | `options`, `retry.policy`, `retry.type`, `timeouts` |
| 3 | Only in RestDeveloperfile | `authenticationOptions`, `retry.count`, `retry.delayInSec` |
| 1 | Changed | `headers` |
| **8** | **Total** | |

---

## Same pattern on other endpoints

Certificates and OS already have the retry/timeouts shape. BASIC credentials there stay `authenticationOptions` until retested:

- `PUT /cloud/certificates` (`setUpdatecertificate`)
- `PUT /cloud/os` (`setOs`)

---

## Docs work

1. **2a done.** Install BASIC credentials are `options` (HTTPS device test, later 26 Aug 2026).
2. **2b done.** Retry / timeouts / `headers.Authorization` aligned to developer.
3. Certificates and OS still use `authenticationOptions` until those endpoints are retested.
