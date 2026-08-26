# Three download APIs — same schema problem

**Date:** 25 August 2026

Three REST APIs share one documentation problem: `RestDeveloperfile.yaml` still uses the **old download-control schema**, while `openAPISpec 10.yaml` has the **new firmware/developer schema**.

| API | Path | Per-endpoint note |
|---|---|---|
| Apps | `PUT /cloud/apps/install` | [PUT-cloud-apps-install.md](PUT-cloud-apps-install.md) |
| Certificates | `PUT /cloud/certificates` | [PUT-cloud-certificates.md](PUT-cloud-certificates.md) |
| OS | `PUT /cloud/os` | [PUT-cloud-os.md](PUT-cloud-os.md) |

Install retry/timeouts/`options` are merged. Certificates and OS still document `authenticationOptions`.

---

## 1. The common problem

The biggest common change in the developer YAML:

```
Our docs / reader — certs and OS           Developer YAML / install
────────────────────────────────────────────────────────
authenticationOptions                     options
```

**PUT `/cloud/apps/install` (HTTPS, later 26 Aug 2026):** `options` works. Docs aligned. Certificates and OS still use `authenticationOptions`. Decisions: [DISCUSS-AND-FINALIZE.md](DISCUSS-AND-FINALIZE.md).

The new specification also introduces HTTPS download controls:

```
retry
 ├── type: randomWait
 └── policy
      ├── retries
      └── wait
           ├── min
           └── max

timeouts
 ├── connection
 └── read
```

Current documentation either has the old retry structure (`retry.count` / `retry.delayInSec`) or does not document retry/timeouts at all (OS).

---

## 2. Retry is only for HTTPS

For all three APIs:

```
HTTPS
  ↓
retry can be used
timeouts can be used
```

For the other protocols:

```
SFTP
FTPS
SCP (where supported — OS only)
  ↓
do NOT use retry
do NOT use timeouts
```

Retry is **not** a general retry mechanism for every download protocol.

| API | Supported URL schemes | Retry / timeouts |
|---|---|---|
| Apps | `https://`, `ftps://`, `sftp://` | HTTPS only |
| Certificates | `https://`, `ftps://`, `sftp://` | HTTPS only |
| OS | `https://`, `ftps://`, `sftp://`, `scp://` | HTTPS only |

---

## 3. The big difference: synchronous vs asynchronous

This is where the three APIs differ.

### Apps

```
PUT /cloud/apps/install

HTTPS + NO retry
        ↓
    SYNCHRONOUS

HTTPS + retry
        ↓
   ASYNCHRONOUS
```

### Certificates

```
PUT /cloud/certificates

HTTPS + NO retry
        ↓
    SYNCHRONOUS

HTTPS + retry
        ↓
   ASYNCHRONOUS
```

Apps and certificates behave the **same way**.

### OS

```
PUT /cloud/os

Any supported protocol
        ↓
   ASYNCHRONOUS
```

OS updates are **always asynchronous**.

Adding `retry` does **not** make OS asynchronous — the OS operation was already asynchronous.

For OS:

```
HTTPS
  ├── retry optional
  └── timeouts optional

SCP / SFTP / FTPS
  ├── no retry
  └── no timeouts
```

---

## 4. What asynchronous means

```
Client
  │
  │ PUT request
  ↓
Reader
  │
  └── Immediate acknowledgment
          │
          ↓
    Download in background
          ↓
        Retry
       if needed
          ↓
     Install / update
          ↓
    Final result
          ↓
 Management events
```

The client **does not keep the original HTTP request waiting** for the entire download and install/update.

| Mode | HTTP response | Final success / failure |
|---|---|---|
| Synchronous | Waits until download + install finish | This REST/MQTT call |
| Asynchronous | Immediate acknowledgment | Management events channel (OS: also `GET /cloud/status`) |

---

## 5. The documentation problem

**Credentials:** PUT `/cloud/apps/install` uses `options` (HTTPS, later 26 Aug 2026). PUT `/cloud/certificates` and PUT `/cloud/os` still use `authenticationOptions`. See [DISCUSS-AND-FINALIZE.md](DISCUSS-AND-FINALIZE.md).

Retry / timeouts (install, certificates, and OS, 26 Aug 2026): **aligned to developer**. OS is always asynchronous.

---

## Final picture

```
                 THREE APIs
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
       Apps     Certificates      OS
        │            │            │
        └────────────┼────────────┘
                     │
              SAME SCHEMA ISSUE
                     │
        authenticationOptions  (certs / OS)
                  ↓
                options         (install aligned)
                     │
              HTTPS controls
                     │
          retry + timeouts
                     │
             ┌───────┴────────┐
             │                │
           Apps / Certs       OS
             │                │
       retry controls     always async
       sync → async       retry optional
             │                │
             └───────┬────────┘
                     │
             Docs need updating
```

---

## In one sentence

Install uses `options` and the new HTTPS `retry`/`timeouts` model. Certificates and OS still document `authenticationOptions`; apps and certificates become asynchronous when HTTPS retry is configured, while OS updates are always asynchronous.
