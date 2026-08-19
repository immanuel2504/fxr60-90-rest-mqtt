# NEED LIVE TEST / discuss with developer — `/cloud/apps/install`

## Question

Can app package download over HTTPS use a certificate already installed on the reader?

Spec fields:

- `installedCertificateName`
- `installedCertificateType`
- also `verifyPeer` / `verifyHost`
- also `CACertificateFileLocation` / `CACertificateFileContent`

Draft example `PUT/installUserapp_pinned_ca.json` references:

```json
{
  "installedCertificateType": "server",
  "installedCertificateName": "reader-server-cert"
}
```

(`reader-server-cert` matches the GET `/cloud/certificates` sample.)

## What to confirm on a reader

1. Does `installedCertificateName` + `installedCertificateType` work for HTTPS `.deb` download?
2. Which types are valid: `server`, `client`, `app`?
3. Or should TLS trust use `GET /cloud/caCertificates` / CA PEM fields instead of `/cloud/certificates`?
4. Until confirmed: prefer the simple SFTP + BASIC example (`installUserapp.json`) as the reviewed one-example.

**Status (Excel Reviewed by me):** NEED LIVE TEST — installedCertificateName/Type vs CA store

Recorded: 2026-08-09
