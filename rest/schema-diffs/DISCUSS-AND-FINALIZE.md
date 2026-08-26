# Schema diffs — discuss and finalize

**Started:** 26 August 2026  
**Working note for decisions.** Per-endpoint comparison files stay in this folder (trees, examples, field maps). Do not merge `RestDeveloperfile.yaml` until a row here is **Final**. Do not edit `rest/openAPISpec 10.yaml`.

---

## Send to the developer

Excel to share: [REST-schema-questions-for-developer_2026-08-26.xlsx](REST-schema-questions-for-developer_2026-08-26.xlsx) — 14 questions. Developer replies in column **I**.

### GET `/cloud/mode` (and PUT `/cloud/mode` for ports + `READER_LOCATION`)

> On GET `/cloud/mode`, `{ "verbose": true }` works on the reader.  
> Your spec does not list a request body.  
> Can you add `verbose` to GET `/cloud/mode`?  
>  
> The reader has four GPI ports (1, 2, 3, and 4).  
> GET `/cloud/gpi` already shows all four.  
> On GET `/cloud/mode` and PUT `/cloud/mode`, when we start or stop inventory using a GPI, the spec only allows port 1 or 2.  
> Why only two? Can we use port 3 and 4 on GET `/cloud/mode` and PUT `/cloud/mode` as well?  
>  
> Your spec does not list `READER_LOCATION`.  
> Does GET `/cloud/mode` and PUT `/cloud/mode` support `READER_LOCATION` in `tagMetaData`?

### PUT `/cloud/network` (and GET `/cloud/network` response spelling)

> On PUT `/cloud/network`, `802_1XEAP` (uppercase X) works on the reader.  
> Your spec lists `802_1xEAP` (lowercase x).  
> Can you change the spec to `802_1XEAP`?  
> GET `/cloud/network` has the same spelling on `securityType`.  
>  
> On PUT `/cloud/network`, `innerAuthentication` value `MSCHAPV2` works on the reader.  
> `MSCHAPv2` does not.  
> Your spec lists `MSCHAPv2`.  
> Can you change the spec to `MSCHAPV2`?  
>  
> On PUT `/cloud/network`, Wi-Fi on/off works with `mlan0.enable`.  
> 802.1X on/off works with `eth0.security.enable`.  
> Wi-Fi security on/off works with `mlan0.accesspoint.security.enable`.  
> Your spec puts Wi-Fi on/off at `mlan0.accesspoint.enable` and does not list the two security `enable` fields.  
> Can you match the reader?

### GET `/cloud/config`

> On GET `/cloud/config`, when GPIO-LED is not configured, `{}` works on the reader.  
> `"NOT_CONFIGURED"` is not what the reader returns.  
> Your spec lists `"NOT_CONFIGURED"`.  
> Can you change the spec to an empty object?

### PUT `/cloud/config` (`postActionColor`)

> On PUT `/cloud/config`, `postActionColor` value `OFF` is rejected.  
> Your spec only lists `GREEN`, `RED`, and `AMBER`.  
> Why is `OFF` not allowed? Can the LED be turned off after the action?

### GET `/cloud/stack-led`

> On PUT `/cloud/stack-led`, your spec lists allowed values:  
> color: `red`, `amber`, `green`, `blue`, `off`  
> brightness: `low`, `med`, `high`  
>  
> On GET `/cloud/stack-led`, your spec leaves `status`, `color`, and `brightness` as free strings.  
> Can GET use the same lists as PUT?  
> For `status`, is the value only `DEFAULT` or `NON_DEFAULT`?

---

### GET `/cloud/status`

> On GET `/cloud/status`, your spec always lists antenna ports `"1"` through `"8"`.  
> FXR60 does not have eight antennas.  
> Does the reader return only the ports that exist, or always 1–8?  
>  
> For `impinjGen2X.feature`, your spec lists `fastId`, `tagFocus`, `tagProtect`, and `tagQuieting`.  
> What value is returned when Gen2X is not in use? Is it `none`?  
>  
> For `powerSource`, your spec is an open string.  
> On FXR, we see `PWR_BRICK`, `POE`, and `POE+`. `DC` is not used.  
> Can you list those three values in the spec?

---

### PUT `/cloud/certificates` and PUT `/cloud/os`

> On PUT `/cloud/certificates` and PUT `/cloud/os`, BASIC username and password work with `authenticationOptions`.  
> `options` does not work on the reader.  
> Your spec lists `options`.  
> Can you change the spec to `authenticationOptions`?

### PUT `/cloud/impinjGen2X`

> On PUT `/cloud/impinjGen2X`, the request body matches (fastID, tagProtect, tagFocus, tagQuieting).  
> The 200 success body does not.  
> Your spec says success is an empty string `""`.  
> We document `{ "message": "Success: Gen2X configured. Use applyImpinjGen2X flag in start command to apply features." }`.  
> What does the reader actually return on 200? An empty string, or that JSON message?

---

## 1. GET `/cloud/mode`

Detail: [GET-cloud-mode.md](GET-cloud-mode.md) · PUT: [PUT-cloud-mode.md](PUT-cloud-mode.md)  
MQTT: `get_mode`

### 1a. `{ "verbose": true }`

| | |
|---|---|
| Developer YAML | No request body |
| Our docs | Optional `{ "verbose": true }` — full config including defaults. Omit or `false` — configured values only |
| Device (26 Aug 2026) | **Works** |

**Keep docs.** Do not delete `verbose`. Ask developer to add it to their spec.

- [x] Device tested
- [x] Final for our docs
- [ ] Developer reply

### 1b. GPI ports 1–4 vs spec max 2

On GET/PUT `/cloud/mode`, when inventory starts or stops on a GPI:

| Place | Ports |
|---|---|
| GET `/cloud/gpi` | 1, 2, 3, 4 |
| `readerCapabilities` example | `numGPIs: 4` |
| Developer mode GPI | only 1 or 2 |
| Our docs | 1–4 |

Until they answer: **keep 1–4**.

- [ ] Developer reply
- [ ] Final

### 1c. `READER_LOCATION` in `tagMetaData`

Our docs include `READER_LOCATION`. Developer spec does not.

Until they answer: **keep `READER_LOCATION`**.

- [ ] Developer reply
- [ ] Final

PUT `/cloud/mode` is the same 1b and 1c questions. **Keep docs** (ports 1–4 and `READER_LOCATION`) until the developer replies.

---

## 14. PUT `/cloud/mode` — waiting on developer

Same as 1b and 1c. No extra PUT-only fields.

- [ ] Developer reply
- [ ] Final

---

## 2. PUT `/cloud/apps/install`

Detail: [PUT-cloud-apps-install.md](PUT-cloud-apps-install.md) · three download APIs: [HTTPS-download-control.md](HTTPS-download-control.md)  
MQTT: `set_installUserapp`

Certificates (`PUT /cloud/certificates`) and OS (`PUT /cloud/os`) still use `authenticationOptions` until those are retested. Install (HTTPS, 26 Aug 2026) uses `options`.

### 2a. BASIC credentials key — `options` — **Final**

| | |
|---|---|
| Our docs | `options` |
| Developer YAML | `options` |
| Device (26 Aug 2026, HTTPS install) | **`options` works** |

**Align to developer.** PUT `/cloud/apps/install` BASIC credentials are `options.username` / `options.password`. Certificates and OS stay `authenticationOptions` until tested.

- [x] Device tested (HTTPS)
- [x] **Final** — rename install to `options`

### 2b. Retry, timeouts, headers — **Final**

Developer is right. Docs now match their retry / timeouts / headers. Credentials are `options` (2a).

| | Docs now |
|---|---|
| Retry | `{ "type": "randomWait", "policy": { "retries", "wait": { "min", "max" } } }` |
| Timeouts | `{ "connection", "read" }` — HTTPS only |
| Headers | `headers.Authorization` |
| When retry is sent | HTTPS → background install. FTPS/SFTP → do not send retry |

- [x] **Final** — Align to developer (retry / timeouts / headers). Credentials are `options`.

---

## 3. PUT `/cloud/certificates`

Detail: [PUT-cloud-certificates.md](PUT-cloud-certificates.md)  
MQTT: `set_updateCertificate`

Same download pattern as install. Required fields stay `url`, `type`, `name`.

### 3a. BASIC credentials key — `authenticationOptions` vs `options` — **Final**

| | |
|---|---|
| Our docs | `authenticationOptions` |
| Developer YAML | `options` |
| Device | **`authenticationOptions` works. `options` does not.** |

**Keep docs.** Do not rename to `options`. Install (2a) now uses `options`; certificates stay `authenticationOptions` until retested.

- [x] **Final for our docs** — keep `authenticationOptions`
- [ ] Developer reply — they should use `authenticationOptions` in the spec, not `options`

### 3b. Retry, timeouts, headers — **Final**

Developer is right. Docs now match their retry / timeouts / headers. Credentials stay `authenticationOptions` (3a).

| | Docs now |
|---|---|
| Retry | `{ "type": "randomWait", "policy": { "retries", "wait": { "min", "max" } } }` |
| Timeouts | `{ "connection", "read" }` — HTTPS only |
| Headers | `headers.Authorization` |
| When retry is sent | HTTPS → background. FTPS/SFTP → do not send retry |

- [x] **Final** — Align to developer (retry / timeouts / headers). Keep `authenticationOptions`.

---

## 4. PUT `/cloud/os`

Detail: [PUT-cloud-os.md](PUT-cloud-os.md)  
MQTT: `set_os`

Required fields stay `url`, `authenticationType`. OS is **not** like install or certificates: the update is **always background**. `retry` does not switch sync/async.

### 4a. BASIC credentials — `authenticationOptions` vs `options` — **Final**

| | |
|---|---|
| Our docs | `authenticationOptions` |
| Developer YAML | `options` |
| Device | **`authenticationOptions` works. `options` does not.** |

**Keep docs.** Talk to the developer — same note as install and certificates.

- [x] **Final for our docs** — keep `authenticationOptions`
- [ ] Developer reply

### 4b. Retry and timeouts — **Final**

Developer is right. Docs now include HTTPS `retry` / `timeouts`. OS is always asynchronous. Credentials stay `authenticationOptions` (4a).

| | Docs now |
|---|---|
| Retry | `{ "type": "randomWait", "policy": { "retries", "wait": { "min", "max" } } }` — HTTPS only |
| Timeouts | `{ "connection", "read" }` — HTTPS only |
| When retry is sent | Does **not** change sync/async. OS is always background. SCP/FTPS/SFTP: do not send retry |

- [x] **Final** — Align to developer (retry / timeouts / always async). Keep `authenticationOptions`.

---

## 5. DELETE `/cloud/certificates/{certname}` — **Final**

MQTT: `del_certificate`

Our docs had `type` as a **query** parameter (`?type=client`). Developer spec and **device (26 Aug 2026)** use `type` in the **JSON body**.

```http
DELETE /cloud/certificates/{certname}
{ "type": "client" }
```

- [x] Device tested
- [x] **Final** — Align to developer. `type` in request body (`client` or `app`). Not in the URL.

---

## 6. PUT `/cloud/network`

Detail: [PUT-cloud-network.md](PUT-cloud-network.md)  
MQTT: `set_network`

Three JSON disagreements. GET `/cloud/network` has the same 802.1X spelling (item 7).

### 6a. Ethernet 802.1X key spelling — **Final**

| | |
|---|---|
| Our docs | `802_1XEAP` (uppercase X) |
| Developer spec | `802_1xEAP` (lowercase x) |
| Device (26 Aug 2026) | **`802_1XEAP` works.** |

**Keep docs.** Do not rename to `802_1xEAP`. Ask the developer to use `802_1XEAP` in the spec.

- [x] Device tested
- [x] **Final for our docs** — keep `802_1XEAP`
- [ ] Developer reply

### 6b. Where `enable` lives — **Final**

| | Our docs | Developer spec | Device (26 Aug 2026) |
|---|---|---|---|
| Ethernet port on/off | `eth0.enable` | `eth0.enable` | same |
| 802.1X on/off | `eth0.security.enable` | not listed | **our field works** |
| Wi-Fi on/off | `mlan0.enable` | `mlan0.accesspoint.enable` | **`mlan0.enable` works** |
| Wi-Fi security on/off | `mlan0.accesspoint.security.enable` | not listed | **our field works** |

**Keep docs.** Do not move Wi-Fi enable to `mlan0.accesspoint.enable`. Do not drop the security `enable` flags. Ask the developer to match the reader.

- [x] Device tested
- [x] **Final for our docs**
- [ ] Developer reply

### 6c. Inner authentication spelling — **Final**

| | |
|---|---|
| Our docs | `MSCHAPV2` |
| Developer spec | `MSCHAPv2` |
| Device (26 Aug 2026) | **`MSCHAPV2` works. `MSCHAPv2` does not.** |

**Keep docs.** Do not change to `MSCHAPv2`. Ask the developer to use `MSCHAPV2` in the spec.

- [x] Device tested
- [x] **Final for our docs** — keep `MSCHAPV2`
- [ ] Developer reply

---

## 7. GET `/cloud/network`

Detail: [GET-cloud-network.md](GET-cloud-network.md)  
MQTT: `get_network`

### 7a. Optional GET body `{ "interface": "eth0" }` — **Final**

| | |
|---|---|
| Our docs | Optional `{ "interface": "eth0" }` — that interface only. Omit or `{}` — all interfaces |
| Developer spec | Same |
| Device | Developer is right |

**Align to developer.** Keep `802_1XEAP` on the response (7b). `wan0` stays FXR90 only.

- [x] **Final** — add optional GET / MQTT `interface` filter

### 7b. Response `securityType` spelling — **Final**

Same as 6a. Our docs: `802_1XEAP`. Their spec: `802_1xEAP`. Device already confirmed `802_1XEAP` on PUT.

**Keep docs.** Do not rename to `802_1xEAP`.

- [x] **Final for our docs** — keep `802_1XEAP`

---

## 8. GET `/cloud/config`

Detail: [GET-cloud-config.md](GET-cloud-config.md)  
MQTT: `get_config`

### 8a. Extra field `xml` — **Final**

| | |
|---|---|
| Our docs | `xml` string — Cloud Connect RFID profile, when present |
| Developer spec | Same |
| Device | Align to developer |

**Align to developer.** Add optional `xml` on GET / MQTT `get_config`. GPIO-LED unset stays `{}` (8b).

- [x] **Final** — add `xml`

### 8b. GPIO-LED when nothing is configured — **Final**

| | Unset value |
|---|---|
| Developer | `"GPIO-LED": "NOT_CONFIGURED"` |
| Our docs | `"GPIO-LED": {}` |
| Device (26 Aug 2026) | **Works** (`{}`) |

**Keep docs.** Do not change unset GPIO-LED to `"NOT_CONFIGURED"`. Ask developer to match `{}`.

- [x] Device tested
- [x] **Final for our docs** — keep `{}`
- [ ] Developer reply

---

## 9. PUT `/cloud/config`

Detail: [PUT-cloud-config.md](PUT-cloud-config.md)  
MQTT: `set_config`

### 9a. Request field `xml` — **Final**

| | |
|---|---|
| Our docs | Optional `xml` — Cloud Connect RFID profile. Send at least one of `xml`, `GPIO-LED`, or `READER-GATEWAY` |
| Developer spec | Same |
| Device | Align to developer |

**Align to developer.** LED number is 1, 2, or 3 (9b). `postActionColor` `OFF` dropped (9c).

- [x] **Final** — add `xml` on PUT / MQTT `set_config`

### 9b. LED number — **Final**

| | Allowed `led` |
|---|---|
| Developer | `1`, `2`, or `3` |
| Our docs | same |
| Device (26 Aug 2026) | **All three work** |

**Align to developer.** GPIO-LED LED actions may use light 1, 2, or 3.

- [x] Device tested
- [x] **Final** — `led` 1 \| 2 \| 3

### 9c. `postActionColor` — **Final**

| | Allowed |
|---|---|
| Developer | `GREEN`, `RED`, `AMBER` |
| Our docs | same (dropped `OFF`) |
| Device (26 Aug 2026) | **`OFF` rejected** |

**Align to developer.** Drop `OFF`. Ask why the reader rejects it.

- [x] Device tested
- [x] **Final for our docs** — no `OFF`
- [ ] Developer reply (why `OFF` is rejected)

---

## 10. PUT `/cloud/apps/{appname}/start` — **Final**

Detail: [PUT-cloud-apps-appname-start.md](PUT-cloud-apps-appname-start.md)  
MQTT: `set_startUserapp`

| | REST body |
|---|---|
| Our docs | None — app name is only in the URL |
| Developer YAML | Optional `{ "appname" }` (for MQTT in the same file) |
| Device (26 Aug 2026) | **No request body needed.** Path only works. |

**Keep docs.** Do not add a REST body. MQTT still sends `appname` in the payload.

- [x] Device tested
- [x] **Final for our docs** — path only

## 11. PUT `/cloud/apps/{appname}/stop` — **Final**

Same as start. Path only. No REST body.

- [x] **Final for our docs** — path only (same as 10)

## 12. PUT `/cloud/apps/{appname}/uninstall` — **Final**

Same as start. Path only. No REST body.

- [x] **Final for our docs** — path only (same as 10)

---

## 13. PUT `/cloud/apps/{appname}/pass-through` — **Final**

Detail: [PUT-cloud-apps-appname-pass-through.md](PUT-cloud-apps-appname-pass-through.md)  
MQTT: `set_reqToUserapp`

| | |
|---|---|
| Our docs | `userapp` required; `command` optional |
| Developer YAML | Same |
| Device | Not tested |

**Align to developer.** REST body requires `userapp`. `{appname}` stays in the path. `command` is optional.

- [x] **Final** — Align to developer

---

## 15. PUT `/cloud/start` — **Final**

Detail: [PUT-cloud-start.md](PUT-cloud-start.md)  
MQTT: `start`

| | Targeted `scanType` object |
|---|---|
| Our docs | Any data-endpoint name (`additionalProperties`) |
| Developer YAML | Same |
| Device | Align to developer |

**Align to developer.** Do not name `dataEndpoint1` / `dataEndpoint2` as schema properties. Example names match the developer file (`start_Global_*`, `start_Targeted`).

- [x] **Final** — Align to developer

## 16. PUT `/cloud/stop` — **Final**

Same as start. MQTT: `stop`

- [x] **Final** — Align to developer

---

## 17. GET `/cloud/stack-led` — **Final**

Detail: [GET-cloud-stack-led.md](GET-cloud-stack-led.md)  
MQTT: `get_stackled`

Developer (26 Aug 2026): `status` is `DEFAULT` or `NON_DEFAULT`. Keep GET enums (`status`, `color`, `brightness`).

- [x] Developer reply — `status` is `DEFAULT` \| `NON_DEFAULT`
- [x] **Final** — Keep docs

---

## 18. GET `/cloud/status` — waiting on developer

Detail: [GET-cloud-status.md](GET-cloud-status.md)  
MQTT: `get_status`

Antenna map, Gen2X `none`, and `powerSource` enum. **Keep docs** until they reply.

- [ ] Developer reply
- [ ] Final

---

## 19. GET `/cloud/version` — **Final**

Detail: [GET-cloud-version.md](GET-cloud-version.md)  
MQTT: `get_version`

| | |
|---|---|
| Our docs | `model`: `FXR90`, `FX7500`, `FX9600`, `ATR7000`, `FXR60`. Upgrade objects are plain objects. |
| Developer YAML | Same |

**Align to developer.**

- [x] **Final** — Align to developer

---

## 20. GET `/cloud/cableLossCompensation` — **Final**

Detail: [GET-cloud-cableLossCompensation.md](GET-cloud-cableLossCompensation.md)  
MQTT: `get_cableLossCompensation`

**Align to developer.** Per-port map uses `patternProperties: '^[1-8]$'` and `additionalProperties: false`.

- [x] **Final** — Align to developer

## 21. PUT `/cloud/cableLossCompensation` — **Final**

Same Each-branch wrapper as GET. MQTT: `set_cableLossCompensation`

- [x] **Final** — Align to developer

---

## 22. PUT `/cloud/impinjGen2X` — waiting on developer

Detail: [PUT-cloud-impinjGen2X.md](PUT-cloud-impinjGen2X.md)  
MQTT: `set_impinjGen2X`

Request schema matches. **200 body does not:** developer `""` vs our `{ "message": "…" }`. Keep our message until they confirm what the reader returns.

- [ ] Developer reply
- [ ] Final

---

## 23. GET `/cloud/readerCapabilities` — **Final**

Detail: [GET-cloud-readerCapabilities.md](GET-cloud-readerCapabilities.md)  
MQTT: `get_readerCapabilities`

| | `supportedPowerSource` |
|---|---|
| Our docs | `DC` \| `POE` \| `POE+` \| `POWERBRICK` \| `BATTERY` |
| Developer YAML (GET path) | Same |

**Align to developer.** Add `DC`. GET `/cloud/status` `powerSource` is unchanged (still waiting: `PWR_BRICK` / `POE` / `POE+`, no `DC`).

- [x] **Final** — Align to developer

