# NEED LIVE TEST — `PUT /cloud/os`

**Excel status:** NEED LIVE TEST — installed cert vs inline CA for HTTPS firmware download

## Question

For HTTPS firmware download, which TLS trust method works on the reader?

| Approach | Fields |
|---|---|
| Installed certificate | `installedCertificateName` + `installedCertificateType` (from `GET /cloud/certificates`) |
| Inline / file CA | `CACertificateFileContent` and/or `CACertificateFileLocation` |
| Verify flags | `verifyPeer` / `verifyHost` |

Draft `PUT/os_https_pinned_ca.json` uses installed cert:

```json
{
  "installedCertificateType": "server",
  "installedCertificateName": "reader-server-cert",
  "verifyPeer": true,
  "verifyHost": true
}
```

Same open question as `PUT /cloud/apps/install`.

## What to confirm on a reader

1. Does installed cert reference work for OS update HTTPS?
2. Is inline PEM / CA file path required instead (or in addition)?
3. Which `installedCertificateType` values work (`server` / `client` / `app`)?
4. Or should trust come from `GET /cloud/caCertificates`?

Until confirmed: prefer non-TLS-pin examples (`os.json` / `os_basic_auth.json` / `os_scp.json`); do not finalize `os_https_pinned_ca.json`.

Recorded: 2026-08-09
