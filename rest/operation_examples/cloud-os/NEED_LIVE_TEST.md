# NEED LIVE TEST — `PUT /cloud/os`

Confirm HTTPS firmware download with **installed** certificate fields works on reader:

- `installedCertificateType`: `server`
- `installedCertificateName`: `reader-server-cert`
- `verifyPeer` / `verifyHost`: `true`

Do not finalize additional auth/SCP/pinned-CA variants until this path is confirmed.
