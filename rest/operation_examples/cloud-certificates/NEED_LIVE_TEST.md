# NEED LIVE TEST — `PUT /cloud/certificates`

**Excel status:** NEED LIVE TEST — install/update certificate on reader

## What to confirm on a real reader

1. Download + install PFX via `url` + `type` (`client` / `server` / `app`) works.
2. `authenticationType` `NONE` vs `BASIC` (`options.username` / `password`).
3. `pfxPassword` required when PFX is password-protected.
4. Success response shape (schema may be empty / no body — confirm).
5. Optional TLS fields (`verifyPeer`, `CACertificateFileContent`) if used for HTTPS download of the PFX.
6. After install, `GET /cloud/certificates` shows the new cert.

Draft packs exist under `PUT/` (`updateCertificate.json`, client/app/inline variants) — do not finalize until live test.

Recorded: 2026-08-09
