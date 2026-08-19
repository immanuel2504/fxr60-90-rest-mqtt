# FXR60-90 — session context (what happened)

Last updated: 2026-08-08 (also includes FXR-Series example-review thread)

## Goal

Ship **self-contained** final OpenAPI packages for **FXR60 / FXR90**:

- REST → `rest/FXR_60-90_rest_api.yaml`
- MQTT → `mqtt/FXR_60-90_mqtt_api.json` (+ local docs viewer)

A copy of this whole folder also lives on the Desktop: `C:\Users\Admin\Desktop\FXR60-90`.

---

## Current layout

```text
FXR60-90/
  README.md
  CONTEXT.md                 # this file
  rest/
    RestDeveloperfile.yaml   # source schemas (copied into package)
    operation_descriptions/
    operation_examples/
    scripts/
      FXR_60-90_api_rest_api.py
      build_fxr90_rest_api.py  # helpers (copied into package)
    FXR_60-90_rest_api.yaml    # generated final
  mqtt/
    openapi_md.json            # applied OpenAPI (synced with final)
    examples/                  # 72 command packs
    tag_config.json            # REST-aligned tag names
    scripts/FXR_60-90_mqtt_api.py  # self-contained build
    FXR_60-90_mqtt_api.json    # generated final
    docs/                      # viewer UI (from repo docs/)
      index.html
      swagger.html
      openapi_md.json
      css/ js/ assets/
```

---

## Rebuild

```bash
.venv\Scripts\python.exe FXR60-90/rest/scripts/FXR_60-90_api_rest_api.py
.venv\Scripts\python.exe FXR60-90/mqtt/scripts/FXR_60-90_mqtt_api.py
```

- REST needs Python + **PyYAML**
- MQTT needs Python **stdlib only**
- No other repo-root files required to rebuild (dependencies were copied in)

---

## Timeline of decisions / work

### 1. REST final package
- Built from developer OpenAPI + markdown descriptions + folder examples
- Examples live under `rest/operation_examples/<path>/<METHOD>/*.json` (not embedded YAML)
- Avoid “Grok” / audit wording in customer-facing text
- Still missing examples for 4 DELETE ops (syslog, radioPacketLog, cert, CA cert) — build exits `1` when those are absent

### 2. MQTT examples
- Packs from `mqtt-examples` → `mqtt/examples/<command>/{request,response}/*.json`
- Initially wired through repo `scripts/generate_openapi_tags_md.py`

### 3. MQTT schemas in package → then removed
- Tried copying `schemas/` into `mqtt/schemas` (needed `references/` for `$ref`)
- User asked to build from compiled OpenAPI instead of separate schema tree
- Flow became: **`openapi_md.json` + `examples/`** → final JSON
- Package-local `mqtt/schemas/` removed from the lean layout

### 4. Docs viewer inside MQTT
- Copied repo `docs/` UI into `mqtt/docs/`
- Titles branded **FXR60 / FXR90**
- `swagger.html` → `../FXR_60-90_mqtt_api.json`
- `Command Schemas.json` removed; viewer loads without it
- Kept `tag_config.json` for display-name overrides

### 5. Stack LED added to MQTT
- Missing from MQTT sources / `Command Schemas.json` (only **app LED** there)
- REST has `/cloud/stack-led` (**FXR60 only**)
- Added MQTT ops: `get_stackled`, `set_stackled` + example packs
- Noted in descriptions: FXR60 only; FXR90 should use `get_appled` / `set_appled`
- Final MQTT: **85** endpoints, **72** example packs

### 6. Keep OpenAPI files in sync
- `mqtt/openapi_md.json`, `mqtt/FXR_60-90_mqtt_api.json`, and `mqtt/docs/openapi_md.json` are kept identical after each build

### 7. Tags match REST
- MQTT tags renamed to REST style: `Control`, `App-led`, `Stack-led`, `Date&Time`, `Ble`, etc.
- MQTT-only event tags: `Management-events`, `Tag-data-events`
- REST-only tag not mirrored: `Login`

### 8. Self-contained package
- REST: copied `RestDeveloperfile.yaml` + `build_fxr90_rest_api.py` into `rest/`
- MQTT: inlined example-overlay helpers into `FXR_60-90_mqtt_api.py` (no import from repo `scripts/`)
- Desktop copy: `C:\Users\Admin\Desktop\FXR60-90`

---

## Important product rules

| Topic | Rule |
|-------|------|
| Stack LED | FXR60 only; not on FXR90 |
| App LED | Both; MQTT `get_appled` / `set_appled` |
| Examples | Prefer folder packs; merge don’t blindly replace |
| Generated files | Do not hand-edit `FXR_60-90_rest_api.yaml` or `FXR_60-90_mqtt_api.json` |

---

## Known gaps

1. REST: 4 DELETE operations still have no example packs → rebuild returns exit code `1`
2. MQTT OpenAPI validator may still complain about `set_config` schema complexity (historical; file still written)
3. Leftover sibling folders under repo `FXR60-90/` (e.g. older `mqtt_examples/`, `operation_examples/`) may exist outside the lean `rest/` + `mqtt/` packages — prefer the packages above

---

## Quick verify

MQTT final should include:

- `/get_appled`, `/set_appled`
- `/get_stackled`, `/set_stackled` with examples
- Tags `App-led`, `Stack-led` (REST naming)

---

## Related work: FXR-Series REST example review (sibling folder)

**Repo / folder:** `C:\Users\Admin\Desktop\FXR-Series`  
**Detail copy also at:** `FXR-Series/reviewed-by-me/CONTEXT.md`

This is **separate from** the self-contained `FXR60-90` package above. It is a hand-review of examples for the FXR90 REST OpenAPI before merging into the canonical YAML.

### Goal

Improve Swagger / docs **examples** for FXR90 REST.  
You review each endpoint in Excel; agent does **not** auto-merge into the official OpenAPI until you ask.

### Key files in FXR-Series

| File / folder | Role |
|---|---|
| `FXR90-rest-api.yaml` | **Canonical** OpenAPI (source of truth) |
| `FXR90-rest-api.with-examples.yaml` | Review copy with PROPOSED examples injected |
| `grok-examples/`, `opus-examples/` | Draft example packs |
| `docs-examples-audit/FXR90-Examples-Effort-Effectiveness.xlsx` | Tier / Effort / Effectiveness work order |
| `reviewed-by-me/` | Your **approved** examples after review |

### What happened earlier (audit phase)

1. Inventory ~52 paths / ~73 `/cloud/*` operations.
2. Excel audits (Grok, Opus, Effort-Effectiveness).
3. Built `grok-examples` / `opus-examples` (GET/PUT folders, PROPOSED JSON).
4. Built `FXR90-rest-api.with-examples.yaml` for preview only.
5. Cascading dropdowns in UI — **rejected**; leave Swagger as-is.
6. Work order: Tier 0 schema fixes → **Tier 1 simple GETs first** → Tier 2–3 later.

### Your rule

- Do **not** silently edit `FXR90-rest-api.yaml`.
- Explain → propose JSON → you approve → save under `reviewed-by-me/` → mark Excel **Reviewed by me**.

### Tier 1 (simple / do first) — missing GET response examples

1. `GET /cloud/localRestLogin`
2. `GET /cloud/hostName`
3. `GET /cloud/timeZone`
4. `GET /cloud/ntpServer`
5. `GET /cloud/preSelection`
6. `GET /cloud/gpi`
7. `GET /cloud/gpo`
8. `GET /cloud/app-led`
9. `GET /cloud/stack-led`
10. `GET /cloud/readerLocation`

### Deep dive completed with you: `/cloud/app-led`

**What it is**

- Application LED on the reader (status light for operators).
- “App” = **your** integration software calling REST (not one fixed product app).
- GET → `DEFAULT` (reader controls LED) or `NON_DEFAULT` (app override active).
- PUT → set `color` / `flash` / `seconds` (e.g. amber blink while busy).

**Confusion resolved**

| What you saw | Meaning |
|---|---|
| Word `DEFAULT` in YAML | Schema enum / description — allowed values |
| `{"status":"DEFAULT"}` in Swagger | Often **auto-generated** from schema |
| Excel “MISSING” | No explicit `examples:` block under GET 200 |
| PUT amber example | **Already in** canonical YAML |

Rule: schema / Swagger auto-fill ≠ official named OpenAPI example.

**Your decisions**

- Approve GET: `DEFAULT` + `NON_DEFAULT`.
- Keep PUT amber blink; optional green/off later.
- Summary titles must show the **result** (no “Grok Nice-to-Have”).
- Filenames: **snake_case**, all lowercase.
- Excel: new column **Reviewed by me** → marked **Updated** for app-led.

**Approved layout**

```text
FXR-Series/reviewed-by-me/cloud-app-led/
  GET/default_reader_controls_led.json     → {"status":"DEFAULT"}
  GET/non_default_app_controls_led.json    → {"status":"NON_DEFAULT"}
  PUT/set_led.json                         → amber, flash, 60s
  SUMMARIES.md
  README.md
```

**Summary titles**

- `Response: status = DEFAULT (reader controls LED)`
- `Response: status = NON_DEFAULT (app controls LED)`
- `Request: amber blink for 60 seconds (busy signal)`

### Next endpoint: `/cloud/gpi`

- GPI = General Purpose **Input** pins 1–4 (sensors/triggers).
- **GET only** (no PUT).
- Canonical: schema only; proposed samples: all LOW, pin 3 HIGH.
- Folder created: `reviewed-by-me/cloud-gpi/` (`all_pins_low.json`, `pin_3_high.json`) + Excel Updated.
- Confirm with you if that folder is final or still draft.

### Process going forward (per endpoint)

1. Explain endpoint (simple English + scenario).
2. Show canonical “how it is” vs proposed JSON.
3. You review summaries / filenames.
4. Save under `reviewed-by-me/<endpoint>/GET|PUT/`.
5. `SUMMARIES.md` + `README.md` (why customer uses it).
6. Excel **Reviewed by me** = Updated.
7. Merge into canonical YAML **only when you ask**.

### Tier 1 — DONE (2026-08-11)

`gpo`, `hostName`, `localRestLogin`, `ntpServer`, `preSelection`, `readerLocation`, `stack-led`, `timeZone` — all reviewed and closed.

Still open: Tier 0 schema fixes and Tier 2+.

### Live feedback batch (2026-08-10)

Applied reader/QA feedback across packs + Excel + REST/MQTT rebuild:

- **Good / Updated:** localRestLogin, start, preSelection, impinjGen2X, version (live FXR60 body), status (one), readerCapabilities, cableLoss GET/PUT, reboot, hostName GET + one PUT, app-led, gpo/gpi, region GET/PUT (Canada one each), supported lists, timeZone GET UTC + PUT UTC/Kolkata, certificates GET (live list), certificates PUT (old `updateCertificate` only), cert refresh, wifiNetworks (live scan), networkInterfaces (fxr60 + fxr90), readPoints, pass-through (removed bad request; Success response), **cloudConfig PUT** (11 examples), **config PUT** (11 examples — see below), updatePassword (`set_password` / `set_password_rfidadm`), apps start/stop/uninstall (no REST body), ble path → **`/cloud/bleConfig`**
- **Deferred:** **GET `/cloud/config`** (work later), **GET `/cloud/mode`** (later)
- **Updated:** **PUT `/cloud/mode`** — 11 examples from `mode_testing/PUT_cloud_mode`

### PUT `/cloud/mode` (2026-08-11) — 11 examples

From lab lean set (no rssiFilter / legacy):

1. `simple_basic` / `inventory_with_interval` / `portal_gpi_trigger` / `conveyor_basic`
2. `with_filter_prefix` / `with_query` / `with_selects` / `with_accesses`
3. `with_report_filter` / `with_tag_metadata` / `with_radio_stop`

### PUT `/cloud/config` (2026-08-11) — 11 examples

REST `cloud-config/PUT/` + MQTT `set_config/request/`:

1. `data_mqtt` — MQTT + GPIO-LED + global batching/retention + managementEventConfig  
2. `data_aws` / `data_azure` / `data_http_post` / `data_tcpip_server` / `data_websocket`  
3. `clear_data`  
4. `gpio_led_tag_radio` / `gpio_led_cloud` / `gpio_led_gpi` / `gpio_led_conditions`
- **Discuss:** stack-led (QA), ntpServer (Mayur/Dhavnesh), caCertificates (Mayur), DELETE certificates type param (QA)
- **NEED LIVE TEST:** `PUT /cloud/os` + `PUT /cloud/apps/install` (installed cert HTTPS bodies)
- **Need to work:** setdataToRG
- **Product:** eSimConfig = FXR90 only; `wan0` not on FXR60 (Krishna)

### Link to this package (FXR60-90)

- App LED / stack LED product rules above still apply (stack LED = FXR60 only).
- When FXR-Series reviews are done, approved REST examples may feed `rest/operation_examples/` or the FXR90 canonical YAML — **do not hand-edit** generated `rest/FXR_60-90_rest_api.yaml`; prefer source packs + rebuild.
