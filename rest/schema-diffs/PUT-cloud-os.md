# PUT `/cloud/os` — schema difference

**Date:** 25 August 2026  
**operationId:** `setOs`  
**MQTT:** `set_os`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path is the same**. OS updates always run in the background. The **credential key** and optional HTTPS **retry / timeouts** differ.

Related: [PUT `/cloud/apps/install`](PUT-cloud-apps-install.md), [PUT `/cloud/certificates`](PUT-cloud-certificates.md).

---

## What is happening

| Client follows | Body keys | What the reader does (developer spec) |
|---|---|---|
| RestDeveloperfile (old) | `authenticationOptions` | Key is not in the developer schema. |
| openAPISpec 10 (new) | `options`, optional `retry` + `timeouts` on HTTPS | Matches current download contract. |

Required fields are unchanged: `url`, `authenticationType`.

**OS is not like install/certificates.** Firmware updates are **always asynchronous**. Sending `retry` does not switch sync/async; it only configures HTTPS backoff. SCP, FTPS, and SFTP stay async but do not support `retry` or `timeouts`.

---

## Runtime (developer spec)

```
PUT /cloud/os
        │
        └── always ASYNCHRONOUS
              → API returns an immediate acknowledgment
              → download + update run in the background
              → final result on management events (or GET /cloud/status)

              retry / timeouts:
                ├── url is https://  → optional backoff + connection/read timeouts
                └── scp://, sftp://, ftps://  → do not send retry or timeouts
```

`RestDeveloperfile.yaml` has no `retry` or `timeouts` on this operation at all.

---

## Request-body tree — developer

```
PUT /cloud/os
├── url                         string   required   scp:// | https:// | sftp:// | ftps://
├── authenticationType          string   required   NONE | BASIC
├── options                     object              BASIC credentials  [NEW KEY]
│   ├── username                string   required
│   └── password                string   required
├── transfer_protocol           string              SCP | HTTPS | SFTP | FTPS
├── verifyPeer / verifyHost     boolean
├── CA / public / private key file location or content
├── installedCertificateType    string              unconstrained in developer
├── installedCertificateName    string
├── headers                     object              additionalProperties string
├── retry                       object              HTTPS only  [NEW]
│   ├── type                    string              randomWait
│   └── policy.retries / wait.min / wait.max
└── timeouts                    object              HTTPS only  [NEW]
    ├── connection              integer
    └── read                    integer
```

---

## Request-body tree — RestDeveloperfile

```
PUT /cloud/os
├── url / authenticationType    required (unchanged)
├── authenticationOptions       object              [OLD KEY]
│   ├── username / password
├── installedCertificateType    string              enum=server | client | app
└── headers                     additionalProperties
```

No `retry`. No `timeouts`.

---

## Field mapping

| RestDeveloperfile | Developer | Action |
|---|---|---|
| `authenticationOptions` | `options` | Rename |
| — | `retry.type` + `retry.policy` | Add (HTTPS only) |
| — | `timeouts.connection` / `read` | Add (HTTPS only) |
| `installedCertificateType` enum server/client/app | unconstrained string | Ours is FXR docs polish |

---

## Examples

### RestDeveloperfile (current)

```json
{
  "authenticationType": "BASIC",
  "authenticationOptions": {
    "username": "test",
    "password": "XXXX"
  },
  "url": "https://10.17.231.168:8003/3_20_4"
}
```

### Developer — HTTPS with retry

```json
{
  "authenticationType": "BASIC",
  "options": {
    "username": "test",
    "password": "XXXX"
  },
  "url": "https://10.17.231.168:8003/3_20_4",
  "retry": {
    "type": "randomWait",
    "policy": {
      "retries": 3,
      "wait": { "min": 10, "max": 30 }
    }
  },
  "timeouts": {
    "connection": 5,
    "read": 600
  }
}
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 3 | Added in developer | `options`, `retry`, `timeouts` |
| 1 | Only in RestDeveloperfile | `authenticationOptions` |
| 1 | Changed | `installedCertificateType` |
| **5** | **Total** | |

---

## Docs work still to do (not applied yet)

Nothing has been merged into `RestDeveloperfile.yaml`. Align with the developer column when firmware is the source of truth, then update `rest/operation_descriptions/`, `rest/operation_examples/`, MQTT `openapi_md.json`, and rebuild.
