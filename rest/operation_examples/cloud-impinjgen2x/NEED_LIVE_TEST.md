# `/cloud/impinjGen2X` — live test status

**Status:** all 12 spec examples accepted (HTTP 200) on reader 5.0.7, 2026-09-06.

See `pfx_server/rest/cloud-impinjGen2X-PUT/TAG_PROTECT_REPORT.md` for TagProtect procedure.

PUT only saves. Apply with `PUT /cloud/start` `{ "applyImpinjGen2X": true }` each session.
Exactly one feature per request. Combinations return 422.
