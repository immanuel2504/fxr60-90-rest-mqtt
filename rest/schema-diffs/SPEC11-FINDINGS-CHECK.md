# Spec 11 vs developer findings (22 questions)

**Date:** 6 September 2026  
**Findings shared:** `FXR-API-Findings-For-Developer_2026-09-feedback .xlsx`  
**Developer YAML:** `rest/openAPISpec 11.yaml`  
**Our source:** `rest/RestDeveloperfile.yaml` (then rebuild `FXR_60-90_rest_api.yaml`)

Checked every Excel row against spec 11 **before** updating our docs.

| # | Topic | Developer reply | In spec 11? | Our docs after this pass |
|---|---|---|---|---|
| 1 | GET `/cloud/mode` `verbose` | updated schema | Yes — request body `verbose` | Already had it |
| 2 | GPI ports 1–4 on mode start/stop | updated schema | **No** — `gpi.v1.port` still `maximum: 2` | Keep 1–4 |
| 3 | `READER_LOCATION` in `tagMetaData` | updated schema | **No** — still missing | Keep `READER_LOCATION` |
| 4 | `802_1XEAP` spelling | updated schema | Yes (2 leftover `802_1xEAP` examples) | Already `802_1XEAP` |
| 5 | `MSCHAPV2` spelling | updated schema | Yes in enums (descriptions still say MSCHAPv2) | Already `MSCHAPV2` |
| 6 | security `enable` fields | no update required | Unchanged | Keep reader-tested `enable` fields |
| 7 | GPIO-LED unset `{}` | updated schema | Yes — empty object or config | Already `{}` |
| 8 | `postActionColor` `OFF` | updated schema | Yes — enum includes `OFF` | Added `OFF` |
| 9 | `impinjGen2X.feature` `none` | updated schema | Yes | Already had `none` |
| 10 | `powerSource` enum | updated schema | Yes — `PWR_BRICK`, `POE`, `POE+` | Already had it |
| 11 | `supportedPowerSource` / `DC` | keep `DC`; note FXR60/90 | Partial — note added, still `POWERBRICK` not `PWR_BRICK` | Description note added; enum unchanged |
| 12 | certs `options` vs `authenticationOptions` | will test later | Still `options` only | Keep `authenticationOptions` |
| 13 | OS `options` vs `authenticationOptions` | will test later | Still `options` only | Keep `authenticationOptions` |
| 14 | PUT Gen2X 200 `{ message }` | updated schema | Yes | Already had the message |
| 15 | `impinjGen2X.isActive` | updated schema | Yes | Renamed `active` → `isActive` |
| 16 | `gen2xFeaturesSupported` + `stackLED` | updated schema | Yes | Added both |
| 17 | `channelData` strings | updated schema | Yes on GET `/cloud/region` | GET items are now strings |
| 18 | app-led / stack-led `required` | updated schema | Yes — `color`, `flash`, `seconds` | Added `required` |
| 19 | `get_supportedRegionList` lowercase s | updated schema | Yes | MQTT command text updated |
| 20 | timeZone GET IANA / PUT both | explained | **Schema not changed** (GET enum still GMT) | Descriptions/examples updated |
| 21 | drop `blescan`; add `all` | `all` added; blescan later | Enum is `eth0/mlan0/bnep0/wan0/uap0/all` | Enum + example updated |
| 22 | `get_displayConfig` typo | updated schema | Yes | Already correct |

**Not in spec 11 despite “updated schema”:** #2 GPI max 2, #3 `READER_LOCATION`, #20 timeZone enums.

**Left open on purpose:** #6, #12, #13 (developer will not change, or will retest).
