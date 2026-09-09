# `/cloud/impinjGen2X` — live test status

**GET:** re-tested 8 September 2026 on FXR60 and FXR90, reader application 5.0.7.

GET returns the last saved feature only. Never-configured is HTTP 200 with an empty body (not JSON `{}`). After a FastID PUT both readers returned `{"fastID":{"enabled":false}}`. PUT `{}` is rejected (422); the saved config is sticky.

**PUT:** all 12 spec examples accepted 6 September 2026 on FXR60 5.0.7 (`10.233.48.36`). Each returned HTTP 200 with `Success: Gen2X configured. Use applyImpinjGen2X flag in start command to apply features.` Combinations and empty/`{}` bodies return 422 and are not published.

PUT only saves. Apply with `PUT /cloud/start` `{ "applyImpinjGen2X": true }` each session.
Exactly one feature per request. Combinations return 422.
