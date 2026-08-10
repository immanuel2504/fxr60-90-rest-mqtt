# FXR90 REST — Example Effort vs Effectiveness

Source workbook: [`FXR90-Examples-Effort-Effectiveness.xlsx`](./FXR90-Examples-Effort-Effectiveness.xlsx)  
Sheets: **How to use** · **All endpoints** (73 operations from `FXR90-rest-api.yaml`)  
Sibling audit location: `C:\Users\Admin\Desktop\FXR-Series\docs-examples-audit\`

This markdown is a readable copy of that work order. Prefer updating the **Excel** when marking progress; keep this MD in sync when the list changes.

---

## What this workbook is for

Prioritize which REST operations need **named OpenAPI examples** for Swagger / docs.

| Column | Meaning |
|--------|---------|
| **Tier** | Work order: simple / high-ROI first → complex / optional last |
| **Effort** | How hard to add or merge examples into canonical `FXR90-rest-api.yaml` |
| **Effectiveness** | How much it helps a reader using Swagger / Docusaurus |
| **What's happening** | Current state: exists / missing / schema defects / ready PROPOSED files |
| **Req/Resp examples now** | Counts in the **canonical** YAML (not the with-examples preview) |
| **PROPOSED ready** | Draft JSON already under `grok-examples/` GET\|PUT folders |
| **Recommended action** | What to do next |
| **Reviewed by me** | Your approval status after hand review |

### Suggested sequence

1. **Tier 0** — fix schema bugs before trusting those examples  
2. **Tier 1** — simple GETs with missing response examples (do first)  
3. **Tier 2** — still simple variants / small gaps  
4. **Tier 3** — medium complexity (modes, cloud, certs, OS, etc.)  
5. **Tier 4–5** — already good / optional polish — skip unless spare time  

### Review rules (from CONTEXT)

- Do **not** silently edit `FXR90-rest-api.yaml`.  
- Explain → propose JSON → you approve → save under `reviewed-by-me/` → mark Excel **Reviewed by me**.  
- Merge into canonical YAML **only when you ask**.  
- Filenames: **snake_case**, all lowercase. Summary titles show the **result** (no “Grok Nice-to-Have”).

---

## Counts by tier

| Tier | Meaning | Operations |
|------|---------|------------:|
| 0 | Fix schema first | 3 |
| 1 | Simple / do first | 10 |
| 2 | Still simple | 19 |
| 3 | Medium complexity | 8 |
| 4 | Already good | 26 |
| 5 | Optional polish | 7 |
| | **Total** | **73** |

---

## Tier 0 — Fix schema first (3)

| # | Method | Endpoint | Effort | Effectiveness | What's happening | Action |
|---|--------|----------|--------|---------------|------------------|--------|
| 1 | GET | `/cloud/config` | Medium | Critical | SPEC DEFECT: GPIO-LED `oneOf` string-only; in-spec `{}` invalid; 1 inline response; +1 PROPOSED resp | Fix schema, then keep/adjust |
| 2 | GET | `/cloud/network` | Medium | Critical | SPEC DEFECT: `IPV6.prefix` typed string but examples use integer `64`; 5 response examples | Fix schema, then keep/adjust |
| 3 | PUT | `/cloud/network` | Medium | Critical | Same IPV6.prefix defect; 17 named request examples; empty-string success | Fix schema, then keep/adjust |

---

## Tier 1 — Simple / do first (10)

Missing GET response examples (schema declares JSON). High docs value, low effort.

| # | Method | Endpoint | Tag | PROPOSED resp | Recommended action | Reviewed by me |
|---|--------|----------|-----|---------------|--------------------|----------------|
| 4 | GET | `/cloud/app-led` | App-led | 2 | Reviewed — GET examples approved | **Updated — reviewed-by-me/cloud-app-led/** |
| 5 | GET | `/cloud/gpi` | Gpio | 2 | Reviewed — GET examples approved | **Updated — reviewed-by-me/cloud-gpi/** |
| 6 | GET | `/cloud/gpo` | Gpio | 1 | Reviewed — single GET example (`gpo_status`) | **Updated — reviewed-by-me/cloud-gpo/** |
| 7 | GET | `/cloud/hostName` | System | 1 | Deferred — focus later | **Deferred — focus later** |
| 8 | GET | `/cloud/localRestLogin` | Login | 1 | Reviewed — `login_success` | **Updated — reviewed-by-me/cloud-localrestlogin/** |
| 9 | GET | `/cloud/ntpServer` | Date&Time | 1 | Add response example(s) from grok-examples | |
| 10 | GET | `/cloud/preSelection` | Control | 2 | Add response example(s) from grok-examples | |
| 11 | GET | `/cloud/readerLocation` | Network | 2 | Add response example(s) from grok-examples | |
| 12 | GET | `/cloud/stack-led` | Stack-led | 2 | Deferred — focus later (FXR60 only) | **Deferred — focus later** |
| 13 | GET | `/cloud/timeZone` | Date&Time | 2 | Add response example(s) from grok-examples | |

### Tier 1 ready files (grok-examples)

| Endpoint | Ready files |
|----------|-------------|
| `/cloud/app-led` | `GET/response.200.default_state.json`, `response.200.overridden_state.json` |
| `/cloud/gpi` | `GET/response.200.all_low.json`, `response.200.port_3_asserted.json` → approved as `all_pins_low` / `pin_3_high` |
| `/cloud/gpo` | Approved (1): `gpo_status.json` → `reviewed-by-me/cloud-gpo/` |
| `/cloud/hostName` | `GET/response.200.configured.json` |
| `/cloud/localRestLogin` | Approved (1): `login_success.json` → `reviewed-by-me/cloud-localrestlogin/` |
| `/cloud/ntpServer` | `GET/response.200.configured.json` |
| `/cloud/preSelection` | `GET/response.200.disabled.json`, `response.200.enabled.json` |
| `/cloud/readerLocation` | `GET/response.200.fix_acquired.json`, `response.200.no_fix.json` |
| `/cloud/stack-led` | `GET/response.200.flashing_red_with_countdown.json`, `response.200.solid_green.json` |
| `/cloud/timeZone` | `GET/response.200.india.json`, `response.200.utc.json` |

**Next up after GPI:** typically `/cloud/gpo` (same GPIO family), then remaining Tier 1 GETs.

---

## Tier 2 — Still simple (19)

Mostly PUT variants, log GETs, DELETEs with empty success bodies.

| # | Method | Endpoint | Effort | Effectiveness | Action |
|---|--------|----------|--------|---------------|--------|
| 14 | PUT | `/cloud/app-led` | Low–Medium | High | Add small variants / missing GET samples |
| 15 | DELETE | `/cloud/caCertificates/{caname}` | Low | Medium | Reviewed — `success` empty-string response | **Updated — NEED LIVE TEST path `{caname}` vs body `name`** |
| 16 | PUT | `/cloud/cableLossCompensation` | Low–Medium | High | Reviewed — `cable_loss` + empty-string success | **Updated — reviewed-by-me/cloud-cablelosscompensation/** |
| 17 | GET | `/cloud/certificates` | Low–Medium | High | Reviewed — single `installed` | **Updated — NEED LIVE TEST response shape** |
| 18 | DELETE | `/cloud/certificates/{certname}` | Low | Medium | Reviewed — `success` + MQTT `del_certs` | **Updated — reviewed-by-me/cloud-certificates-certname/** |
| 19 | GET | `/cloud/eSimConfig` | Low–Medium | High | Reviewed — `profiles_present` only (removed `no_profiles`) | **Updated — reviewed-by-me/cloud-esimconfig/** |
| 20 | PUT | `/cloud/gpo` | Low–Medium | High | Reviewed — single `gpo` (Port 3 HIGH) | **Updated — reviewed-by-me/cloud-gpo/** |
| 21 | PUT | `/cloud/hostName` | Low–Medium | High | Deferred — focus later (with GET) | **Deferred — focus later** |
| 22 | PUT | `/cloud/logs` | Low–Medium | High | Reviewed — single `logs` | **Updated — NEED LIVE TEST** |
| 23 | GET | `/cloud/logs/RcLog` | Low–Medium | High | Reviewed — `download` | **Updated — NEED LIVE TEST** |
| 24 | GET | `/cloud/logs/RgErrorLog` | Low–Medium | High | Reviewed — `download` | **Updated — NEED LIVE TEST** |
| 25 | GET | `/cloud/logs/RgWarningLog` | Low–Medium | High | Reviewed — `download` | **Updated — NEED LIVE TEST** |
| 26 | GET | `/cloud/logs/radioPacketLog` | Low–Medium | High | Reviewed — `download` | **Updated — NEED LIVE TEST** |
| 27 | GET | `/cloud/logs/syslog` | Low–Medium | High | Reviewed — `download` | **Updated — NEED LIVE TEST** |
| 28 | PUT | `/cloud/preSelection` | Low–Medium | High | Reviewed — enable `pre_selection` | **Updated — NEED LIVE TEST** |
| 29 | PUT | `/cloud/reboot` | Low | Medium | Reviewed — empty-string success, no body | **Updated — NEED LIVE TEST** |
| 30 | PUT | `/cloud/region` | Low–Medium | High | Reviewed — single `region` (USA) | **Updated — NEED LIVE TEST** |
| 31 | PUT | `/cloud/stack-led` | Low–Medium | High | Deferred — focus later (FXR60 only) | **Deferred — focus later** |
| 32 | PUT | `/cloud/timeZone` | Low–Medium | High | Reviewed — single `time_zone` (UTC) | **Updated — NEED LIVE TEST** |

---

## Tier 3 — Medium complexity (8)

Named variants for modes, cloud targets, auth, certs, OS, pass-through.

| # | Method | Endpoint | Tag | Action |
|---|--------|----------|-----|--------|
| 33 | PUT | `/cloud/apps/install` | userapp | Prefer SFTP+BASIC until cert check done | **NEED LIVE TEST — installedCertificateName/Type vs CA store** |
| 34 | PUT | `/cloud/apps/{appname}/pass-through` | userapp | One example `pass_through` ready | **NEED LIVE TEST — path appname + app response** |
| 35 | PUT | `/cloud/certificates` | Certificate | Draft packs exist; not finalized | **NEED LIVE TEST — PFX install** |
| 36 | PUT | `/cloud/cloudConfig` | System | Deferred — do later | **Deferred — do later** |
| 37 | GET | `/cloud/mode` | Control | Deferred — do later | **Deferred — do later** |
| 38 | PUT | `/cloud/mode` | Control | Deferred — do later | **Deferred — do later** |
| 39 | PUT | `/cloud/os` | Firmware | Draft packs exist; not finalize pinned CA | **NEED LIVE TEST — installed cert vs inline CA** |
| 40 | PUT | `/cloud/pass-through` | System | Add named variants (+ response) |

---

## Tier 4 — Already good (26)

Audit: keep as-is / already effective. No change unless polishing.

| # | Method | Endpoint |
|---|--------|----------|
| 41 | GET | `/cloud/apps` |
| 42 | PUT | `/cloud/apps/{appname}/autostart` |
| 43 | GET | `/cloud/ble-config` |
| 44 | PUT | `/cloud/ble-config` |
| 45 | GET | `/cloud/caCertificates` |
| 46 | GET | `/cloud/cableLossCompensation` |
| 47 | PUT | `/cloud/config` |
| 48 | PUT | `/cloud/eSimConfig` |
| 49 | GET | `/cloud/impinjGen2X` |
| 50 | PUT | `/cloud/impinjGen2X` |
| 51 | GET | `/cloud/logs` |
| 52 | DELETE | `/cloud/logs/radioPacketLog` |
| 53 | DELETE | `/cloud/logs/syslog` |
| 54 | GET | `/cloud/networkInterfaces` |
| 55 | PUT | `/cloud/ntpServer` |
| 56 | GET | `/cloud/readPoints` |
| 57 | GET | `/cloud/readerCapabilities` |
| 58 | GET | `/cloud/region` |
| 59 | PUT | `/cloud/start` |
| 60 | GET | `/cloud/status` |
| 61 | PUT | `/cloud/stop` |
| 62 | GET | `/cloud/supportedRegionList` |
| 63 | GET | `/cloud/supportedStandardList` |
| 64 | PUT | `/cloud/updatePassword` |
| 65 | GET | `/cloud/version` |
| 66 | GET | `/cloud/wifiNetworks` |

---

## Tier 5 — Optional polish (7)

Very low effort / low value (often empty-string success). Skip if busy.

| # | Method | Endpoint | Action |
|---|--------|----------|--------|
| 67 | PUT | `/cloud/apps/{appname}/start` | Optional `""` success example |
| 68 | PUT | `/cloud/apps/{appname}/stop` | Optional `""` success example |
| 69 | PUT | `/cloud/apps/{appname}/uninstall` | Optional `""` success example |
| 70 | PUT | `/cloud/caCertificates/{caname}` | Optional polish |
| 71 | PUT | `/cloud/certificates/{certname}` | Optional polish |
| 72 | PUT | `/cloud/revertbackOS` | Optional; empty `{}` intentional — don't invent fields |
| 73 | PUT | `/cloud/setdataToRG` | Optional; empty `{}` intentional — don't invent fields |

---

## Progress snapshot (from Excel + CONTEXT)

| Status | Endpoints |
|--------|-----------|
| Reviewed / Updated in Excel | `app-led` (GET + PUT), `gpi`, `gpo` (GET + PUT), `localRestLogin`, `ntpServer`, `preSelection`, `timeZone`, `DELETE caCertificates/{caname}`, `PUT cableLossCompensation`, `GET certificates`, `DELETE certificates/{certname}`, `GET eSimConfig`, `PUT logs` |
| Need live test | `PUT /cloud/app-led` success `""`; **`PUT /cloud/apps/install`** installed certs vs CA; **`PUT /cloud/apps/{appname}/pass-through`** path + response; **`PUT /cloud/certificates`** PFX install; **`PUT /cloud/os`** installed cert vs inline CA |
| Discuss with developer | `preSelection` GET string vs PUT boolean; `readerLocation` timestamp/no-fix; `timeZone` GET long-form vs PUT short-form; **`PUT /cloud/apps/install` — can HTTPS download use installed certs (`installedCertificateName`/`Type` from GET `/cloud/certificates`), which types (`server`/`client`/`app`), or must trust come from CA store / inline PEM?** |
| Deferred | `GET/PUT /cloud/hostName`, `GET /cloud/readerLocation`, `GET/PUT /cloud/stack-led` (FXR60 only), **`PUT /cloud/cloudConfig`**, **`GET/PUT /cloud/mode`** |
| Still pending Tier 1 | *(none — remaining items are deferred)* |

---

## Link to FXR60-90 package

- Approved REST examples may later feed `rest/operation_examples/` or the FXR90 canonical YAML.  
- Do **not** hand-edit generated `rest/FXR_60-90_rest_api.yaml` — use source packs + rebuild.  
- Stack LED = **FXR60 only**; App LED = both FXR60 and FXR90.
