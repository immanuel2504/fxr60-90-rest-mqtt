# Finding 09 — `displayConfig` has the best error messages on this API — and one bad one

**Endpoint** `PUT /cloud/displayConfig`
**Type** Error-reporting quality (both directions)
**Status** Confirmed

## The good — name the field *and* enumerate valid values

```json
{"code":1,"message":"field 'orientation' must be one of: landscape, portrait, landscape-flipped, portrait-flipped"}
{"code":1,"message":"field 'keyboardLayout' has an supported values: English-US, English-UK, German, Spanish, Italian, French, Brazilian, Swedish, Japanese"}
{"code":1,"message":"field 'screenTimeoutSec' must be between 0 (display always on) and 3600 seconds (display always on for 1 hour)."}
{"code":1,"message":"field 'resolution' format is invalid. Must contain 'x' (e.g., '1920x1080')"}
{"code":1,"message":"payload must be a non-empty JSON object"}
```

**This is the standard the rest of the API should meet.** Compare `app-led`'s bare
`Invalid color`, or error 255 in the cloudConfig report, which is returned for
three unrelated causes.

Both enum sets and the 0–3600 range match the schema exactly.

Two wording bugs: *"has an supported values"* should read "has unsupported
value", and the gloss *"3600 seconds (display always on for 1 hour)"* is
self-contradictory — 3600 is a timeout; `0` is always-on.

## The bad — a well-formed but unsupported resolution

```json
{"resolution": "9999x9999"}
→ {"code":3,"message":"CS:'setDisplayConfig' failed, Reason: Missing required parameters"}
```

**Nothing is missing.** `"9999x9999"` passes the format check (it contains `x`)
and then fails at the Core Service, which reports a missing-parameter error.

That same message is what a genuinely incomplete payload returns, so it cannot be
acted on. No `GET` exposes the supported resolution list either.

Note this payload also omits `enable`, which alone produces the same message — so
strictly the two causes cannot be separated from the response. **That is itself
the finding**: one message for at least two unrelated problems.

## The two-layer validator, visible

| Code | Layer | Character |
|---|---|---|
| **1** | REST | specific, names the field, lists valid values |
| **3** | Core Service | generic (`Missing required parameters`) |

Enum and range checks run first at the REST layer, which is why the single-field
probes above return precise messages rather than the required-field error.

## Ask

Report unsupported resolutions distinctly, and expose the supported list via a
`GET`.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-excellent-enum-and-range-errors/` | `rest/cloud-displayConfig-PUT/06-validation-enums-and-ranges-REJECTED/` |
| `evidence-2-misleading-resolution-error/` | `rest/cloud-displayConfig-PUT/07-resolution-unsupported-MISLEADING-ERROR/` |
