# FXR60 Impinj Gen2X — all 12 examples from `openAPISpec 11.yaml`

Every `impinjGen2X` example from the latest spec, tested against a live reader
with real tags in range.

## Scope

| | |
|---|---|
| Spec | `openAPISpec 11.yaml` — **IoT Connector REST API v3.0.0** |
| Endpoint | `PUT /cloud/impinjGen2X` (`setImpinjGen2X`) |
| Reader | `10.233.48.36`, reader app 5.0.7 |
| Date | 2026-09-06 |
| Spec examples | **12** — 2 fastID, 2 tagFocus, 4 tagQuieting, 4 tagProtect |
| Extra tests | 2 — mutual exclusion, validation probes |
| Tags in range | 22–29 unique, incl. Impinj Monza X-2K and R6 |

TagProtect's *functional* testing — the access-password prerequisite and what
could and could not be concluded — is in the sibling
[`TAG_PROTECT_REPORT.md`](../TAG_PROTECT_REPORT.md) and
[`WHAT_WE_DID.md`](../WHAT_WE_DID.md). This report covers all four features'
examples.

---

## Results

**12 / 12 examples accepted (HTTP 200) and stored correctly.** Effects vary:

| # | Example | Accepted | Effect observed |
|---|---|---|---|
| 1 | `enable_fastID` | ✅ | ✅ **works** — TID appended to `idHex` ([resolved](#3--fastid-produces-no-tid-in-the-tag-data)) |
| 2 | `disable_fastID` | ✅ | — (baseline config) |
| 3 | `enable_tagFocus` | ✅ | ⚪ not measurable through this API |
| 4 | `disable_tagFocus` | ✅ | — |
| 5 | `quiet_tags` | ✅ | ✅ **WORKS — proven 0/5 vs 5/5** |
| 6 | `unquiet_tags` | ✅ | ❌ **does not restore visibility** |
| 7 | `advanced_quiet_tags` | ✅ | ⚪ stored verbatim; masks match no local tag |
| 8 | `advanced_unquiet_tags` | ✅ | ⚪ stored verbatim |
| 9 | `protect_tag` | ✅ | see `TAG_PROTECT_REPORT.md` |
| 10 | `unprotect_tag` | ✅ | ⚠️ reader injects `enableShortRange:false` |
| 11 | `enable_protect_read` | ✅ | stored, activates |
| 12 | `disable_protect_read` | ✅ | stored, activates |

✅ works · ❌ documented effect not seen · ⚪ untested/unmeasurable

Every example is schema-accurate — **no casing bugs, no missing fields, no
rejected examples.** That's better than `bleConfig`, where the most detailed
example is rejected outright.

---

## The tested payloads

Every JSON below was sent verbatim to `PUT /cloud/impinjGen2X` on
`10.233.48.36`. These are extracted from the stored `request body/request.json`
files in the numbered folders, so they are exactly what went over the wire.

All twelve returned **HTTP 200** with:

```json
{"message":"Success: Gen2X configured. Use applyImpinjGen2X flag in start command to apply features."}
```

Each was then activated with `PUT /cloud/start {"applyImpinjGen2X": true}`.

---

### fastID

**01 · `enable_fastID`** — ✅ 200 — but no TID appears in tag data ([finding 3](#3--fastid-produces-no-tid-in-the-tag-data))

```json
{
  "fastID": {
    "enabled": true
  }
}
```

**02 · `disable_fastID`** — ✅ 200 — also the reader's baseline/idle config

```json
{
  "fastID": {
    "enabled": false
  }
}
```

---

### tagFocus

**03 · `enable_tagFocus`** — ✅ 200 — effect not measurable ([finding 4](#4--tagfocus--effect-not-measurable-through-this-api))

```json
{
  "tagFocus": {
    "enabled": true
  }
}
```

**04 · `disable_tagFocus`** — ✅ 200

```json
{
  "tagFocus": {
    "enabled": false
  }
}
```

---

### tagQuieting basic

**05 · `quiet_tags`** — ✅ 200 — **feature proven to work** ([finding 1](#1--tagquieting-basic-works--proven-over-repeated-trials))

```json
{
  "tagQuieting": {
    "basic": {
      "action": "quiet",
      "tagIDs": [
        "e2801191a5030069073b426d",
        "e2801191a5030069073b426e"
      ]
    }
  }
}
```

**06 · `unquiet_tags`** — ✅ 200 — but does **not** restore visibility ([finding 2](#2--unquiet-does-not-restore-visibility))

```json
{
  "tagQuieting": {
    "basic": {
      "action": "unquiet",
      "tagIDs": [
        "e2801191a5030069073b426d"
      ]
    }
  }
}
```

---

### tagQuieting advanced

**07 · `advanced_quiet_tags`** — ✅ 200 — stored verbatim ([finding 10](#10--complex-nested-payloads-round-trip-exactly))

```json
{
  "tagQuieting": {
    "advanced": {
      "preSelect": [
        {
          "target": "SL",
          "action": "ASSERTSL_NOTHING",
          "mask": {
            "bank": "EPC",
            "pointer": 32,
            "length": 96,
            "value": "E280123456789012345678AB"
          }
        },
        {
          "target": "S2",
          "action": "INVB_INVA",
          "mask": {
            "bank": "EPC",
            "pointer": 32,
            "length": 96,
            "value": "E280AABBCCDDEEFF11223344"
          }
        }
      ],
      "tagQuietMasks": [
        "SL_ASSERT",
        "S2B"
      ],
      "target": "SL",
      "stateAwareAction": "ASSERTSL_DEASSERTSL"
    }
  }
}
```

**08 · `advanced_unquiet_tags`** — ✅ 200 — stored verbatim

```json
{
  "tagQuieting": {
    "advanced": {
      "preSelect": [
        {
          "target": "SL",
          "action": "DEASSERTSL_NOTHING",
          "mask": {
            "bank": "EPC",
            "pointer": 32,
            "length": 96,
            "value": "E280123456789012345678AB"
          }
        },
        {
          "target": "S2",
          "action": "INVA_INVB",
          "mask": {
            "bank": "EPC",
            "pointer": 32,
            "length": 96,
            "value": "E280AABBCCDDEEFF11223344"
          }
        }
      ],
      "tagQuietMasks": [
        "SL_DEASSERT",
        "S2A"
      ],
      "target": "SL",
      "stateAwareAction": "DEASSERTSL_ASSERTSL"
    }
  }
}
```

---

### tagProtect

**09 · `protect_tag`** — ✅ 200 — `enableShortRange:true` round-trips

```json
{
  "tagProtect": {
    "action": "enableTagProtection",
    "password": "77777777",
    "tagID": "e2801191a5030069073b426d",
    "enableShortRange": true
  }
}
```

**10 · `unprotect_tag`** — ✅ 200 — reader injects `enableShortRange:false` ([finding 7](#7--the-reader-injects-enableshortrange-false))

```json
{
  "tagProtect": {
    "action": "disableTagProtection",
    "password": "77777777",
    "tagID": "e2801191a5030069073b426d"
  }
}
```

**11 · `enable_protect_read`** — ✅ 200 — reader-scoped, no `tagID`

```json
{
  "tagProtect": {
    "action": "enableTagVisibility",
    "password": "77777777"
  }
}
```

**12 · `disable_protect_read`** — ✅ 200 — reader-scoped, no `tagID`

```json
{
  "tagProtect": {
    "action": "disableTagVisibility",
    "password": "77777777"
  }
}
```

---

### Extra tests — not spec examples

**13 · mutual exclusion** — all five combinations rejected with HTTP 422
([finding 5](#5--the-mutual-exclusion-rule-is-broader-than-documented--and-now-undocumented))

```json
{"fastID": {"enabled": true}, "tagFocus": {"enabled": true}}
{"fastID": {"enabled": true}, "tagQuieting": {"basic": {"action": "quiet", "tagIDs": ["e2801191a5030069073b426d"]}}}
{"tagFocus": {"enabled": true}, "tagQuieting": {"basic": {"action": "quiet", "tagIDs": ["e2801191a5030069073b426d"]}}}
{"fastID": {"enabled": true}, "tagFocus": {"enabled": true}, "tagQuieting": {"basic": {"action": "quiet", "tagIDs": ["e2801191a5030069073b426d"]}}}
{"fastID": {"enabled": true}, "tagProtect": {"action": "enableTagVisibility", "password": "77777777"}}
```

Each returned:

```json
{"code":3,"message":"\"set_impinjGen2X\" Failed to apply. Description: unsuccessful rc response: Failure: Only one Impinj Gen2X feature can be configured at a time (fastID, tagProtect, tagFocus, or tagQuieting)"}
```

**14 · validation probes** — all six rejected
([finding 8](#8--validation-is-the-strongest-in-the-whole-test-programme))

| Sent | Response message |
|---|---|
| `{}` | `Invalid payload for set_impinjGen2X api` |
| `{"tagProtect":{"action":"nosuch","password":"77777777"}}` | `value provided for "action" must be a string containing one of the following values: enableTagProtection, disableTagProtection, enableTagVisibility, disableTagVisibility` |
| `{"tagProtect":{"action":"enableTagVisibility","password":"7777777"}}` | `tagProtect.password must be 8 hex characters (32-bit)` |
| `{"tagProtect":{"action":"enableTagVisibility","password":"ZZZZZZZZ"}}` | `tagProtect.password contains invalid hex character: 'Z'` |
| `{"tagProtect":{"action":"enableTagVisibility","password":"77777777","tagID":"e2801191a5030069073b426d"}}` | `tagProtect.tagID is not allowed for action: enableTagVisibility` |
| `{"tagProtect":{"action":"enableTagProtection","password":"77777777"}}` | `tagProtect.tagID is required for action: enableTagProtection` |

---

### The real-tag payloads used for the functional proof

The spec's `quiet_tags` / `unquiet_tags` EPCs are not present in our field, so
the same payload shape was used with a **real** tag to prove the feature. These
are the exact bodies behind the 5-trial measurement in
[finding 1](#1--tagquieting-basic-works--proven-over-repeated-trials):

```json
{"tagQuieting":{"basic":{"action":"quiet","tagIDs":["e2806894000040017790ac71"]}}}
{"tagQuieting":{"basic":{"action":"unquiet","tagIDs":["e2806894000040017790ac71"]}}}
```

Target `e2806894000040017790ac71`; control `e2806894000040017790e471` (never
listed). The mode used for every scan was:

```json
{"type":"CUSTOM","antennas":[1],"transmitPower":30,"tagMetaData":["ANTENNA","RSSI"]}
```

And for the FastID A/B in [finding 3](#3--fastid-produces-no-tid-in-the-tag-data),
the same mode plus an explicit TID request — accepted with HTTP 200, yet no `tid`
field ever appeared:

```json
{"type":"CUSTOM","antennas":[1],"transmitPower":30,"tagMetaData":["ANTENNA","RSSI","TID"]}
```

For the TagFocus A/B in [finding 4](#4--tagfocus--effect-not-measurable-through-this-api),
session S1 was set explicitly per Zebra's MAUI guidance:

```json
{"type":"CUSTOM","antennas":[1],"transmitPower":30,
 "query":{"sel":"ALL","session":"S1","tagPopulation":256,"target":"A"},
 "tagMetaData":["ANTENNA","RSSI"]}
```
---

## Findings

### 1. ✅ `tagQuieting` basic works — proven over repeated trials

The clearest positive result. The spec's EPCs aren't in our field, so the same
payload shape was used with a real tag, `e2806894000040017790ac71`:

| Arm | Target seen |
|---|---|
| `PLAIN start {}` (no Gen2X) | **5/5** trials |
| `quiet` + `applyImpinjGen2X` | **0/5** trials |

12-second inventory per trial, alternating. A control tag
(`e2806894000040017790e471`) stayed visible in every run, so the effect is
specific to the EPC in `tagIDs`.

**Why repeated trials were necessary — and a correction.** A single-shot
comparison looked convincing early on, but a 40-second plain scan then revealed:

```
29 unique tags, read-count distribution = Counter({1: 29})
```

**Every tag is reported exactly once per session**, however long the scan runs —
the reader de-duplicates before the data endpoint. With one read per tag,
absence in a single window is weak evidence and can't separate "quieted" from
"not singulated this time". The 5-trial repetition is what makes this solid; I
did not report the single-shot version as proof.

**Session-scoped, not persistent.** After clearing Gen2X and running a plain
inventory, the quieted tag reappeared. Nothing permanent is written to the tag —
confirmed again as the final post-test check.

### 2. ❌ `unquiet` does not restore visibility

| Arm | Target seen |
|---|---|
| `PLAIN start {}` | 5/5 |
| `quiet` + apply | 0/5 |
| **`unquiet` + apply** | **0/5** ← expected 5/5 |

If `unquiet` reversed `quiet`, the third row should match the first. It matches
the second.

**How the tag actually recovers:** clear the Gen2X config entirely and start
without the flag.

```
PUT /cloud/impinjGen2X {"fastID":{"enabled":false}}
PUT /cloud/start {}          ← no applyImpinjGen2X
→ target VISIBLE again
```

So visibility returns by *not applying* tagQuieting, not by applying `unquiet`.

**Interpretation, offered cautiously:** applying any tagQuieting config appears
to run a pre-select that silences the listed tags for that session, and the
quiet/unquiet action doesn't invert it the way the naming implies. The underlying
Gen2 mechanism is session-flag manipulation, so `unquiet` may need the tag
already asserted from a prior session — which can't happen, since quieting is
session-scoped (finding 1).

**Not established:** whether `unquiet` works on a tag genuinely quieted *within
the same session*. The API can't express that — each Gen2X change needs a
stop/start cycle, which ends the session.

**Ask:** what is basic `unquiet` for, given quieting doesn't persist across
sessions?

### 3. ❌ FastID produces no TID in the tag data

FastID is documented as embedding the TID alongside the EPC in every inventory
response. Tested A/B in a plain CUSTOM mode with **no** `accesses`, so any TID
could only come from FastID:

| | Tag events | Events with a `tid` field |
|---|---|---|
| FastID **ON** | 22 | **0** |
| FastID **OFF** | 23 | **0** |

Identical field sets both runs: `['antenna','eventNum','format','idHex','peakRssi']`

Also requested explicitly — `tagMetaData: ["ANTENNA","RSSI","TID"]` is accepted
(HTTP 200), and still no `tid` field appears. Sample event:

```json
{"antenna":1,"eventNum":3995,"format":"epc",
 "idHex":"e2806894000040017790ac71","peakRssi":-45}
```

The TID **does** exist and is readable — a separate `accesses` READ of the TID
bank returns `e2806894200040017790ac71` for this same tag.

**Not established:** whether FastID is genuinely inactive, or active but the TID
isn't surfaced into the data-endpoint payload. Distinguishing them needs Zebra
confirming which field should carry it, or a throughput comparison (FastID's
other benefit is fewer operations).

> ## ✅ RESOLVED 2026-09-08 — FastID works; there is no defect
>
> Re-tested on **genuine Impinj Monza 4i** tags (MDID `0x801`, TMN `0x1B0`) on
> FXR90 app 5.0.7. FastID returns the TID — but **not in a `tid` field**. It is
> **appended to `idHex`**, and `format` changes from `"epc"` to `"fastID"`:
>
> ```json
> {"antenna":5,"eventNum":95,"format":"fastID",
>  "idHex":"e28011b0a5050076c4d7530ae28011b02000b30a26ba03b6","peakRssi":-24}
> ```
>
> 48 hex chars = 24 EPC + 24 TID. The TID half matches a separate `accesses`
> READ of the TID bank byte for byte, on both tags.
>
> **Two reasons this test missed it.** The tags used here were not Gen2X-capable,
> so FastID never engaged — note `format` stayed `"epc"`, which was the visible
> signal. And the search was for a `tid` field, which does not exist.
>
> The A/B measurement above was sound; the conclusion drawn from it was too
> narrow. Corrected in
> [`../all-features-VERIFIED-507/GEN2X_ALL_FEATURES_507.md`](../all-features-VERIFIED-507/GEN2X_ALL_FEATURES_507.md) §2.

### 4. ⚪ TagFocus — effect not measurable through this API

| | Events | Unique | Avg reads/tag |
|---|---|---|---|
| TagFocus **ON** | 20 | 20 | 1.0 |
| TagFocus **OFF** | 26 | 26 | 1.0 |

Session S1 was set explicitly, per Zebra's MAUI guidance.

> ## ✅ RESOLVED 2026-09-08 — TagFocus works; the measurement was masked
>
> "Avg reads/tag 1.0" in **both** states is the tell: the reader's default report
> filter de-duplicates, so every tag appears once regardless. The feature's whole
> effect is on *repeat* reads, which were being collapsed before they were counted.
>
> Adding `reportFilter: {"duration": 0, "type": "PER_ANTENNA"}` — report every
> individual read — exposes it immediately on Monza 4i tags:
>
> | Trial | `tagFocus:false` | `tagFocus:true` |
> |---|---|---|
> | 1 | **16** reads (8/tag) | **2** reads (1/tag) |
> | 2 | **16** | **2** |
> | 3 | **16** | **2** |
>
> Zero variance across three A/B pairs. **Anyone testing TagFocus needs
> `reportFilter.duration = 0`, or the feature looks inert.** Full detail in
> [`../all-features-VERIFIED-507/GEN2X_ALL_FEATURES_507.md`](../all-features-VERIFIED-507/GEN2X_ALL_FEATURES_507.md) §3.

Both show exactly 1.0 reads per tag — the same de-duplication as finding 1.
TagFocus reduces redundant reads at the **air-protocol** layer; the reporting
layer has already collapsed them to one event per tag per session. **There's no
headroom left to measure.**

This is a limitation of the measurement, **not** evidence TagFocus is broken.
Testing it properly needs a reporting mode that emits raw reads, or a read-rate
comparison in a dense population where weak tags are being starved.

### 5. 🐛 The mutual-exclusion rule is broader than documented — and now undocumented

All five combinations rejected:

```
fastID + tagFocus         → 422
fastID + tagQuieting      → 422
tagFocus + tagQuieting    → 422
all three                 → 422
fastID + tagProtect       → 422
```

```
"Only one Impinj Gen2X feature can be configured at a time
 (fastID, tagProtect, tagFocus, or tagQuieting)"
```

The **previous** spec revision said:

> Mutually Exclusive Features | `fastID`, `tagFocus`, `tagQuieting` (only one
> reader-scoped feature active at a time)

That names **three** and calls them "reader-scoped", implying `tagProtect` —
being tag-scoped — could be combined with one. **It cannot.** The reader's own
message lists all **four**.

And **v3.0.0 removed that table entirely.** The PUT description is now 262
characters and mentions no constraints at all. So the corrected rule is
documented *nowhere* — it exists only in this error message.

**Ask:** document "only one of `fastID` / `tagProtect` / `tagFocus` /
`tagQuieting` per request" in v3.0.0. The old text was wrong; the new text is
absent.

### 6. ⚠️ `status.impinjGen2X` doesn't tell you whether a feature is *on*

With `{"fastID":{"enabled":false}}` applied:

```
GET /cloud/status → "impinjGen2X": {"feature":"fastID","isActive":true}
```

So `feature` + `isActive` mean *"a fastID config is loaded and Gen2X is
running"* — **not** *"FastID is switched on"*. The `enabled` flag inside the
config is what distinguishes on from off, and status doesn't expose it. Same for
`tagFocus`.

Consequence: status can't be used to check whether a feature is actually enabled,
only which feature object was last configured. `GET /cloud/impinjGen2X` is the
only way to see `enabled`.

### 7. ⚠️ The reader injects `enableShortRange: false`

```
sent:   {"action":"disableTagProtection","password":"77777777","tagID":"..."}
stored: {"action":"disableTagProtection","enableShortRange":false,"password":"77777777","tagID":"..."}
                                         ^^^^^^^^^^^^^^^^^^^^^^^ not sent
```

Observed on all three tagProtect actions where it was omitted. Harmless and
arguably a sensible default — but a client doing read-modify-write will see a
field it never set, and one comparing sent-vs-stored will see a spurious
difference. The schema declares no default for it.

### 8. ✅ Validation is the strongest in the whole test programme

| Probe | Response |
|---|---|
| `{}` | `Invalid payload for set_impinjGen2X api` |
| bad `action` | *lists all four valid values* |
| `password` 7 chars | `must be 8 hex characters (32-bit)` |
| `password "ZZZZZZZZ"` | **`contains invalid hex character: 'Z'`** |
| `tagID` + `enableTagVisibility` | `tagID is not allowed for action: enableTagVisibility` |
| `enableTagProtection` no `tagID` | `tagID is required for action: enableTagProtection` |

The `oneOf` branch rule is enforced **both** ways — `tagID` required for
tag-scoped actions, forbidden for reader-scoped ones — and each message names the
field *and* the action.

Naming the offending character (`'Z'`) is the best error message anywhere in this
API. Compare `app-led`'s bare `Invalid color`, `logs`' generic `Invalid payload
fields`, or error 255 in the cloudConfig report which covers three unrelated
causes. **This is the style the rest of the API should adopt.**

### 9. ✅ v3.0.0 fixed the two-step-flow documentation gap

The PUT description now reads:

> Note - start command with `applyImpinjGen2X` flag should be used to start the
> Gen2X operations.

The previous revision never mentioned this on the `impinjGen2X` page — only under
`/cloud/start` — which was finding 3.1 in
[`TAG_PROTECT_REPORT.md`](../TAG_PROTECT_REPORT.md). **That finding is now
resolved.**

Still undocumented: the activation is **per-session**. After `PUT /cloud/stop`,
status returns to `feature:none, isActive:false`, and a later plain `start {}`
does not re-apply it. The flag must be re-sent every time.

### 10. ✅ Complex nested payloads round-trip exactly

The two `advanced` tagQuieting examples are the most structurally complex in the
set — two pre-select entries with masks, a mask-combination array, a target and a
state-aware action. Both stored **verbatim**, every nested field preserved, no
normalisation.

Eight distinct enum values across four enum fields all accepted:
`SL_ASSERT`, `S2B`, `SL_DEASSERT`, `S2A`, `ASSERTSL_NOTHING`,
`DEASSERTSL_NOTHING`, `INVB_INVA`, `INVA_INVB`, plus `ASSERTSL_DEASSERTSL` /
`DEASSERTSL_ASSERTSL`.

The masks match no tag in our field, so the radio-level effect is unverified —
but the schema is accurate and the payloads are preserved.

---

## Questions for Zebra

1. **FastID (highest priority).** No TID appears in tag data with FastID enabled,
   in either the default payload or with `tagMetaData: ["TID"]`. Which field
   should carry it, and is FastID applied on 5.0.7? The TID is readable via a
   normal `accesses` READ on the same tags.

2. **Basic `unquiet`.** It hides the tag rather than restoring it (0/5 trials,
   vs 5/5 with no Gen2X). Given quieting is session-scoped, what state is
   `unquiet` intended to reverse, and can that state be reached through this API?

3. **Mutual exclusion is undocumented in v3.0.0.** The rule covers all four
   features (the old spec said three and mis-described them as "reader-scoped");
   the new spec removed the table entirely. Please restore it, corrected.

4. **`status.impinjGen2X` semantics.** `isActive: true` with `enabled: false`.
   Could status expose the enabled flag, or is `feature` intended to mean only
   "which config is loaded"?

5. **`enableShortRange` default.** The reader injects `false` when omitted. Please
   declare the default in the schema.

6. **Per-session activation.** `applyImpinjGen2X: true` must be re-sent on every
   start. v3.0.0 now mentions the flag — please also state that it doesn't persist
   across inventory sessions.

7. **Testing TagFocus and FastID.** Both operate at the air-protocol layer, and
   the reader de-duplicates to one event per tag per session before the data
   endpoint. Is there a reporting configuration that exposes raw reads, so
   integrators can verify these features are working?

---

## Reader state after testing

| | Pre-test | Post-test | |
|---|---|---|---|
| `impinjGen2X` config | `{"fastID":{"enabled":false}}` | same | ✅ |
| `status.impinjGen2X` | `{"feature":"none","isActive":false}` | same | ✅ |
| `radioActivity` | `inactive` | `inactive` | ✅ |
| Data endpoint | `DATA_AWS_CLOUD_EVENTS` connected | same | ✅ |
| Quieted tag `…ac71` | visible | **visible again** | ✅ |

The quieted tag was explicitly re-verified readable at the end — quieting leaves
no persistent tag state. The data endpoint was temporarily routed to the local
MQTT broker for the measurements, then restored to AWS.

---

## Folder contents

```
v3-all-examples/
├── GEN2X_ALL_EXAMPLES_REPORT.md   ← this file
├── 01-enable_fastID-ACCEPTED-no-TID-in-data/
├── 02-disable_fastID-ACCEPTED/
├── 03-enable_tagFocus-ACCEPTED-effect-not-measurable/
├── 04-disable_tagFocus-ACCEPTED/
├── 05-quiet_tags-WORKS-PROVEN/
│   └── response body/trial-evidence.txt   ← the 5-trial measurement
├── 06-unquiet_tags-DOES-NOT-RESTORE/
├── 07-advanced_quiet_tags-ACCEPTED/
├── 08-advanced_unquiet_tags-ACCEPTED/
├── 09-protect_tag-ACCEPTED/
├── 10-unprotect_tag-ACCEPTED-default-injected/
├── 11-enable_protect_read-ACCEPTED/
├── 12-disable_protect_read-ACCEPTED/
├── 13-mutual-exclusion-ENFORCED/
└── 14-validation-probes/
```

Each holds `request body/request.json` (with the spec example name in
`specExampleName`), `response body/response.json`, `http_status.txt` and
`verification.txt`.

The runner is [`../../../g2x_test.sh`](../../../g2x_test.sh): it applies a
payload, reads the config back, activates it via
`start {"applyImpinjGen2X":true}` and reports which feature the reader makes
active.

---

## Related

| File | Contents |
|---|---|
| [`../TAG_PROTECT_REPORT.md`](../TAG_PROTECT_REPORT.md) | TagProtect procedure + the access-password prerequisite |
| [`../WHAT_WE_DID.md`](../WHAT_WE_DID.md) | Chronological TagProtect record and method flaws |
| [`../../cloud-start-PUT/START_STOP_TEST_REPORT.md`](../../cloud-start-PUT/START_STOP_TEST_REPORT.md) | The `applyImpinjGen2X` flag on `/cloud/start` |
| [`../../cloud-mode-PUT/MODE_TEST_REPORT.md`](../../cloud-mode-PUT/MODE_TEST_REPORT.md) | `PUT /cloud/mode` — `accesses`, filters, all five modes |
