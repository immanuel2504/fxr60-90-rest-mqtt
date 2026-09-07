# Finding 03 — Two endpoints declare no required fields; both are wrong, in opposite directions

**Endpoints** `PUT /cloud/app-led`, `PUT /cloud/displayConfig`
**Type** Spec-vs-firmware mismatch
**Status** Established by drop-one-field sweeps

Neither schema has a `required` array, so every field reads as optional to a
client. Both are wrong — and they are wrong in *opposite* directions.

| Endpoint | Schema says | Actually mandatory |
|---|---|---|
| `/cloud/app-led` | nothing required | **all three** — `color`, `flash`, `seconds` |
| `/cloud/displayConfig` | nothing required | **one** — `enable` only |

## Method

Start from a known-good payload that returns 200, then drop one field at a time.

**app-led** — every field is mandatory:

```
{"color":"green","flash":true,"seconds":5}  → 200
{"color":"green","flash":true}              → 422 Required Fields not provided
{"color":"green","seconds":5}               → 422 Required Fields not provided
{"flash":true,"seconds":5}                  → 422 Required Fields not provided
```

**displayConfig** — only `enable` is mandatory:

```
full seven-field payload           → 200
without enable                     → 422 Missing required parameters
without enableOnscreenKeyboard     → 200
without startUrl                   → 200
without resolution                 → 200
without orientation                → 200
without screenTimeoutSec           → 200
without keyboardLayout             → 200
```

## Why it matters

Two endpoints make the identical declaration and behave oppositely, so a client
cannot infer either one's requirements from the spec. Guessing from `app-led`
gives you the wrong answer for `displayConfig`, and vice versa.

## Ask

Add the arrays: `required: ["color","flash","seconds"]` and
`required: ["enable"]`.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-app-led-needs-all-three/` | `rest/cloud-app-led-PUT/08-color-only-REJECTED-schema-says-optional/` |
| `evidence-2-displayconfig-needs-only-enable/` | `rest/cloud-displayConfig-PUT/04-which-fields-are-mandatory/` |

## Related

[[08-displayconfig-merges-partial-updates]] — the `enable` requirement is why a
single-field PUT looked like "no partial updates".
