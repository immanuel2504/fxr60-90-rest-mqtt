# FXR60 settings endpoints — PUT test report

Six PUT endpoints, tested against a live reader. Every request body and response
in this report is verbatim from a real call; the numbered folders beside each
endpoint hold them individually.

## Scope

| | |
|---|---|
| Reader | `10.233.48.36`, reader app 5.0.7 |
| Date | 2026-09-05 |
| Endpoints | `/cloud/app-led`, `/cloud/displayConfig`, `/cloud/gpo`, `/cloud/region`, `/cloud/timeZone`, `/cloud/ntpServer` |
| Tests | 47 |
| Auth | `GET /cloud/localRestLogin` with `admin:Zebra@123`; tokens not stored |

Pre-test state was captured for all six and **restored afterwards** — see
[Reader state](#reader-state-after-testing).

---

## Results

| Endpoint | Tests | Accepted | Rejected | Verdict |
|---|---|---|---|---|
| `/cloud/gpo` | 9 | 3 | 6 | ✅ **Exemplary** — writes verified, bounds and types enforced, precise errors |
| `/cloud/timeZone` | 7 | 4 | 3 | ✅ Working, clock confirmed to move — ⚠️ undocumented input vocabulary |
| `/cloud/displayConfig` | 7 | 3 | 4 | ✅ Working, best error messages on the API — ⚠️ one misleading error |
| `/cloud/region` | 9 | 5 | 4 | ✅ Working, changes verified — ⚠️ two fields silently ignored |
| `/cloud/app-led` | 8 | 4 | 4 | ⚠️ Accepted, but **not verifiable** and no way back to `DEFAULT` |
| `/cloud/ntpServer` | 7 | 4 | 3 | 🐛 **Defect** — an unresolvable hostname returns 200 and wipes the setting |

All six endpoints function. One firmware defect was found, and four
spec-vs-firmware mismatches.

---

## Findings

### 1. 🐛 `ntpServer`: an unresolvable hostname returns HTTP 200 and wipes the setting

The most serious finding in this batch.

```
before: {"server":"pool.ntp.org"}
PUT     {"server":"nosuch1.invalid.example"}   → HTTP 200, empty body
after:  {"server":""}
```

The reader is left with **no NTP server configured**, and the caller is told the
request succeeded. Reproduced 3/3 runs per key, on both `server` and `server1`,
each run using a different unresolvable name:

| Key | Runs | Before | Response | After |
|---|---|---|---|---|
| `server` | 3/3 | `pool.ntp.org` | **200** | `""` 🐛 |
| `server1` | 3/3 | `pool.ntp.org` | **200** | `""` 🐛 |

**The endpoint already gets this right for another class of bad input.** A
*malformed* hostname is rejected and the previous value survives:

```json
PUT {"server":"not..a..host"}
→ 422 {"code":3,"message":"CS:'setNTPServerRsp' failed,Reason: SNTP_INVALID_SERVER_FORMAT"}
GET → {"server":"pool.ntp.org"}     previous value INTACT ✅
```

So the correct behaviour exists; it just isn't applied to names that are
syntactically valid but do not resolve.

Two separable problems:

1. **The response is wrong.** An input the reader cannot use should be a 4xx, as
   the malformed case already is — not HTTP 200.
2. **The failure is destructive.** Whether or not the new value is rejected, a
   failed update should leave the previous working value in place. Wiping to `""`
   is worse than either accepting or rejecting.

Impact is silent and delayed: the caller has no reason to re-check, and the
consequence — a reader that cannot synchronise its clock — surfaces later as
certificate validity failures and wrong event timestamps, far from the cause. A
single typo in a hostname is enough.

Note `server2` is effectively **write-only** — `GET /cloud/ntpServer` returns
only `server`, so whether a secondary was ever stored cannot be determined
through the API.

### 1b. Both `oneOf` branches work — a correction

An earlier version of this report named the documented `server1` ("legacy") key
as the cause of the wipe. **That was wrong**, and the correction is instructive.

The original test alternated `server` and `server1` payloads and saw a clean
split, 5/5 runs. But it had confounded two variables: every hostname used with
`server1` (`timeA.google.com`, `solo.google.com`, `verify.google.com`) is
NXDOMAIN, while the one used with `server` (`time1.google.com`) resolves.

Re-tested as a 2×2 over key × resolvability:

| | `time.cloudflare.com` (resolves) | `nosuch.invalid.example` (NXDOMAIN) |
|---|---|---|
| `server` | `time.cloudflare.com` ✅ | `""` 🐛 |
| `server1` | `time.cloudflare.com` ✅ | `""` 🐛 |

The key makes no difference; resolvability decides. `server1` works correctly
(3/3 with a resolvable host), so **the schema's `oneOf` is accurate** — both
conventions are honoured, and the response normalises either to `server`.

The lesson for the rest of this exercise: when a split looks clean, check that
only one variable actually differs between the two arms.

### 2. Two endpoints declare no required fields; both are wrong, in opposite directions

Neither schema has a `required` array, so every field reads as optional. Each was
tested by dropping one field at a time from a known-good payload:

| Endpoint | Schema says | Actually mandatory |
|---|---|---|
| `/cloud/app-led` | nothing required | **all three** — `color`, `flash`, `seconds` |
| `/cloud/displayConfig` | nothing required | **one** — `enable` only |

```
app-led   {"color":"green","flash":true,"seconds":5}  → 200
          {"color":"green","flash":true}              → 422 Required Fields not provided
          {"color":"green","seconds":5}               → 422
          {"flash":true,"seconds":5}                  → 422

display   full seven-field payload                    → 200
          without enable                              → 422 Missing required parameters
          without any of the other six                → 200  (each tested separately)
```

Two endpoints make the same declaration and behave oppositely, so a client cannot
infer either from the spec. Suggested: `required: ["color","flash","seconds"]`
and `required: ["enable"]`.

### 3. `timeZone` accepts an undocumented input vocabulary, and returns it

The schema defines `timeZone` as a closed enum of 100+ display names
(`"Kolkata"`, `"Pacific Time (US & Canada)"`, `"London"`, …).

The reader accepts those — and also accepts IANA identifiers, which appear
nowhere in the enum:

| Sent | Accepted | `GET` returns |
|---|---|---|
| `"Kolkata"` (documented) | ✅ | `"Asia/Kolkata"` |
| `"Pacific Time (US & Canada)"` (documented) | ✅ | `"America/Los_Angeles"` |
| `"Asia/Kolkata"` (**not** in enum) | ✅ | `"Asia/Kolkata"` |
| `"UTC"` (documented) | ✅ | `"UTC"` |

So `GET` returns a form the schema does not document as valid input. A client
written strictly to the spec would treat the value it reads back as invalid.
Round-tripping happens to work, but only via undocumented behaviour.

Either document the IANA forms as accepted input, or have `GET` return the
documented display name.

Matching is also **case-sensitive** (`"utc"` → `Invalid Time Zone specified.`),
and the error is identical to the one for a wholly non-existent zone, so it gives
no hint that case is the problem.

**The changes are real**, not merely stored — the reader's clock moved correctly
each time:

| Zone | `systemTime` | Offset |
|---|---|---|
| UTC | 16:49 | — |
| Asia/Kolkata | 22:18 | +5:30 ✅ |
| America/Los_Angeles | 09:48 | −7:00 ✅ |

### 4. `region` silently ignores fields it cannot apply

`GET /cloud/supportedStandardList?region=United States/Canada` reports for
`US_FCC_15`:

```
isLBTConfigurable    "false"
isChannelSelectable  "false"
isHoppingConfigurable "false"
```

Both optional fields were sent anyway:

| Sent | Response | Effect |
|---|---|---|
| `isLBT: true` | **200** | none — `lbtEnabled` still `false` |
| `channeldata: [915750,915250,903250]` | **200** | none — still all 50 channels |

The behaviour is arguably correct, since the standard genuinely does not support
them. **The silence is the problem**: a caller enabling Listen-Before-Talk gets
HTTP 200 and reasonably concludes LBT is on. Better to reject with something like
`isLBT not configurable for standard US_FCC_15`.

Checking the channel *count* matters here, not the first few entries — the three
channels sent are already the first three of the standard's own list, so a
spot-check of `channelData[:3]` looks like it worked. Only `len() == 50` reveals
it did not.

Two typing issues on the same field:

| | Input | Output |
|---|---|---|
| Name | `channeldata` | `channelData` |
| Element type | `integer` (per schema) | **string** — `["915750",…]` |

So it cannot be round-tripped without transforming both the name and the element
type. `isLBTConfigurable` is likewise the string `"false"`, not a boolean.

**Region changes themselves work and are fully verifiable:**

| | `regulatoryStandard` | `region` |
|---|---|---|
| before | `US_FCC_15` | `FCC_Generic` |
| after `US_FCC_A` | `US_FCC_A` | `FCC_A` |
| after `US_FCC_C` | `US_FCC_C` | `FCC_C` |
| restored | `US_FCC_15` | `FCC_Generic` |

Switching works repeatedly without a reboot, and `channelData` updates to match.

### 5. The spec's `region` example does not work on a US/Canada reader

```json
{"country": "Canada", "standardname": "CANADA_FCC_15"}
→ 422 {"code":3,"message":"CS:'regionStandardRsp' failed,Reason: RADIO REGION NOT AVAILABLE"}
```

Neither value exists on this unit. It reports the single combined region
`"United States/Canada"`, with standards `US_FCC_15 / _A / _B / _C / _CUSTOM` —
there is no bare `"Canada"` and no `"CANADA_FCC_15"`.

Most likely a SKU difference rather than a defect. But the documented example
fails on a US/Canada reader with no indication in the spec that it is
region-specific. Either use a universally valid example, or state that valid
values are per-device and must be read from `supportedRegionList` /
`supportedStandardList` first.

### 6. `app-led` cannot be verified, and cannot be reset to `DEFAULT`

All four enum colours are accepted. But `GET /cloud/app-led` returns only:

```json
{"status": "DEFAULT"}  |  {"status": "NON_DEFAULT"}
```

No colour, no flash flag, no remaining duration. So the only thing confirmable
over the API is that *some* non-default state is active — which colour is
actually lit needs physical access.

And `{"color":"off"}` does **not** restore `DEFAULT`:

| Action | `status` |
|---|---|
| initial | `DEFAULT` |
| any PUT | `NON_DEFAULT` |
| `{"color":"off","flash":false,"seconds":0}` | `NON_DEFAULT` |

Once any PUT is made, the endpoint reports `NON_DEFAULT` thereafter. "off" turns
the LED off but still counts as an application-set state, and there is no
documented route back. This reader was left `NON_DEFAULT` for that reason.

Also note `seconds: 0` means "indefinite" and is accepted, while `-5` is rejected
as `seconds (expected positive number)` — so 0 is a special value, not a
duration, and is not covered by the "positive" wording.

### 7. `displayConfig` merges partial updates — the opposite of `/cloud/config`

Sending two fields preserves the other five:

```
before  enable:true  onscreenKb:false  layout:French  orientation:portrait
        resolution:1280x720  timeout:45  url:https://10.117.229.18/

PUT     {"enable":true,"orientation":"landscape-flipped"}   → 200

after   enable:true  onscreenKb:false  layout:French  orientation:landscape-flipped
        resolution:1280x720  timeout:45  url:https://10.117.229.18/
```

Only `orientation` changed. This is the **opposite** of the `GPIO-LED` object in
`PUT /cloud/config`, which replaces wholesale and silently discards events not
named in the request (see `cloud-config-PUT/`, finding 3).

Two endpoints on the same API with opposite update semantics, neither documented.
Please state the semantics per endpoint.

This also corrected an earlier reading of test 03: a single-field PUT of
`{"orientation":...}` is rejected for lacking `enable`, **not** because partial
updates are unsupported.

### 8. `displayConfig` has the best error messages on this API — and one bad one

The good ones name the field *and* enumerate the valid values:

```json
{"code":1,"message":"field 'orientation' must be one of: landscape, portrait, landscape-flipped, portrait-flipped"}
{"code":1,"message":"field 'keyboardLayout' has an supported values: English-US, English-UK, German, Spanish, Italian, French, Brazilian, Swedish, Japanese"}
{"code":1,"message":"field 'screenTimeoutSec' must be between 0 (display always on) and 3600 seconds (display always on for 1 hour)."}
{"code":1,"message":"field 'resolution' format is invalid. Must contain 'x' (e.g., '1920x1080')"}
```

This is the standard the rest of the API should meet — compare `app-led`'s bare
`Invalid color`, or error 255 in the cloudConfig report. Both enum sets and the
0–3600 range match the schema exactly.

Two wording bugs: *"has an supported values"* should read "has unsupported
value", and the gloss *"3600 seconds (display always on for 1 hour)"* is
self-contradictory — 3600 is a timeout; 0 is always-on.

The bad one — a well-formed but unsupported resolution:

```json
{"resolution": "9999x9999"}
→ {"code":3,"message":"CS:'setDisplayConfig' failed, Reason: Missing required parameters"}
```

Nothing is missing. `"9999x9999"` passes the format check (it contains `x`) and
then fails at the Core Service, which reports a missing-parameter error. That
same message is also what a genuinely incomplete payload returns, so it cannot be
acted on. No `GET` exposes the supported resolution list either.

The two-layer validation is visible throughout: **code 1** is the REST layer
(specific, helpful) and **code 3** is the Core Service (generic). Enum and range
checks run first at the REST layer, which is why single-field probes in test 06
return precise messages rather than the required-field error.

### 9. `/cloud/gpo` is the model the other endpoints should follow

The only endpoint of the six with a genuine read-back of what was written, and
strict throughout:

| Probe | Response |
|---|---|
| `{"port":3,"state":true}` | 200 — pin 3 LOW→HIGH, confirmed, no other pin touched |
| `{"port":0,…}` / `{"port":5,…}` | 422 `Invalid GPO pin` |
| `{"port":1}` / `{"state":true}` | 422 `Required Fields not provided.Expected port/state` |
| `{"port":1,"state":"true"}` | 422 `state (expected boolean)` |
| `{"port":"1","state":true}` | 422 `port (expected positive number)` |

Bounds match the schema's 1–4, types are checked on both fields with no silent
coercion, and every message names the offending field. All four pins are
individually writable in both directions.

There is no bulk form — one pin per request, so setting four pins is four PUTs.

This endpoint is what made the GPIO-LED findings in `cloud-config-PUT/` possible:
when a GPIO-LED event failed to move a pin, `PUT /cloud/gpo` proved the pin
itself was fine. It is also the reset used to establish a clean baseline before
each of those observations — GPO state persists across configuration changes, so
the reset must always be **read back** to confirm, or leftover state from an
earlier test reads as a fresh event.

---

## Questions for Zebra

1. **`ntpServer` unresolvable hostname (highest priority).** A well-formed but
   unresolvable hostname returns HTTP 200 and leaves the reader with
   `{"server":""}` — no NTP server at all. Reproduced 3/3 on each key. A
   *malformed* hostname is correctly rejected with `SNTP_INVALID_SERVER_FORMAT`
   and the previous value survives, so the right behaviour already exists in the
   endpoint. Two asks: return a 4xx for a hostname the reader cannot use, and
   never destroy the previous working value on a failed update. A single typo
   currently costs clock sync silently, and the symptoms (certificate validity,
   event timestamps) surface far from the cause.

2. **`server2`.** Is a secondary NTP server stored at all? It cannot be read back
   from `GET /cloud/ntpServer`, so there is no way to confirm.

3. **Intermittent empty GET.** `GET /cloud/ntpServer` occasionally returns a
   completely empty response body instead of a JSON object — roughly 2 times in
   ~40 GETs, with a valid token and no accompanying error. Is this known?

4. **Required fields.** Neither `app-led` nor `displayConfig` declares any
   required field, yet `app-led` requires all three and `displayConfig` requires
   `enable`. Please add the `required` arrays.

5. **`timeZone` vocabulary.** Are IANA identifiers (`Asia/Kolkata`) officially
   supported input? They are accepted and are what `GET` returns, but appear
   nowhere in the enum. Also — is case-sensitivity intended, and could the error
   distinguish a casing mistake from an unknown zone?

6. **`region` silent drops.** Should `isLBT` and `channeldata` be rejected when
   the selected standard reports them unconfigurable, rather than accepted with
   HTTP 200 and discarded?

7. **`region` field naming and types.** Input `channeldata` (integers) vs output
   `channelData` (strings) — the field cannot be round-tripped without
   transforming both. Is that intended? Likewise `isLBTConfigurable` is the
   string `"false"` rather than a boolean.

8. **`region` example.** The spec's `{"country":"Canada","standardname":"CANADA_FCC_15"}`
   is rejected on a reader whose only supported region is `"United States/Canada"`.
   Is the example SKU-specific? If so, please say so.

9. **`app-led` observability and reset.** Can `GET /cloud/app-led` return the
   active colour, flash state and remaining duration rather than just
   `DEFAULT`/`NON_DEFAULT`? And is there any way to return to `DEFAULT` —
   `{"color":"off"}` does not do it.

10. **`displayConfig` on a reader with no display.** The FXR60/FXR90 have no
   built-in screen. These settings are accepted and stored correctly; do they
   apply to an attached monitor, and is there a way to tell whether a display is
   present?

11. **Update semantics.** `displayConfig` merges partial updates; `GPIO-LED` in
    `PUT /cloud/config` replaces wholesale. Neither is documented. Please state
    it per endpoint.

12. **Unsupported resolution.** `{"resolution":"9999x9999"}` returns
    `Missing required parameters`, which is also what an incomplete payload
    returns. Could it report the real cause, and could the supported resolutions
    be exposed via a `GET`?

---

## Reader state after testing

Captured before testing and restored afterwards:

| Endpoint | Pre-test | Post-test | |
|---|---|---|---|
| `app-led` | `DEFAULT` | `NON_DEFAULT` | ⚠️ no way back — finding 6 |
| `displayConfig` | `enable:true, English-US, landscape, 1920x1080, timeout 0, https://localhost/` | identical | ✅ |
| `gpo` | `{"1":"HIGH","2":"LOW","3":"LOW","4":"LOW"}` | identical | ✅ |
| `region` | `United States/Canada, US_FCC_15, FCC_Generic, 50 channels` | identical | ✅ |
| `timeZone` | `UTC` | `UTC` | ✅ |
| `ntpServer` | `pool.ntp.org` | `pool.ntp.org` | ✅ |

Five of six byte-identical. `app-led` cannot be restored to `DEFAULT` through the
API — that is finding 6, not an oversight.

`region` was deliberately changed and restored, since it governs radio regulatory
compliance. It was verified back on `US_FCC_15` / `FCC_Generic` with all 50
original channels.

---

## Folder contents

```
cloud-app-led-PUT/        8 tests
cloud-displayConfig-PUT/  7 tests
cloud-gpo-PUT/            9 tests
cloud-ntpServer-PUT/      7 tests
cloud-region-PUT/         9 tests
cloud-timeZone-PUT/       7 tests
```

Each numbered folder holds:

| Path | Contents |
|---|---|
| `request body/request.json` | The real request — method, URL, reader, headers, body |
| `response body/response.json` | The response verbatim, or `(empty body)` for a 200 |
| `response body/http_status.txt` | HTTP status code |
| `response body/verification.txt` | How the result was confirmed, and what it revealed |

Successful PUTs return HTTP 200 with an **empty body** on all six endpoints.

A few folders cover a sweep rather than one request — `04-which-fields-are-mandatory`,
`06-validation-enums-and-ranges-REJECTED`, `06-missing-fields-REJECTED`,
`02-all-four-high` / `03-all-four-low`. Their `request.json` records the probe set
and `verification.txt` gives the response for each.

Bearer tokens are not stored; each `request.json` records the command that mints
one. Every other value is verbatim as sent.

---

## Related

| File | Contents |
|---|---|
| [`../findings/settings-endpoints/`](../findings/settings-endpoints/) | **Each finding here as its own folder**, with the request/response that proves it |
| `cloud-config-PUT/CONFIG_TEST_REPORT.md` | `PUT /cloud/config` — GPIO-LED and READER-GATEWAY, 20 tests |
| `cloud-cloudConfig-PUT/CLOUDCONFIG_TEST_REPORT.md` | `PUT /cloud/cloudConfig` — endpoint connection types |
| `cloud-certificates-PUT/` | Certificate installation |
| `../MQTT_API_Findings.xlsx` | All findings across REST and MQTT |
