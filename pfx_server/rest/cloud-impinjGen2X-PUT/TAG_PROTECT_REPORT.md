# FXR60 Impinj TagProtect — Procedure and Test Report

The complete working procedure for Impinj TagProtect (Protected Mode) on the
FXR60, including the access-password prerequisite the current documentation
mentions but does not explain, and the two-step apply flow that is documented on
the wrong page.

**Written to be lifted into the Impinj Gen2X documentation.** Section 1 is the
procedure; sections 2 onward are the test evidence behind it.

> For the chronological record — which tags were chosen and why, every payload in
> order, and an honest account of the method's flaws — see
> [`WHAT_WE_DID.md`](WHAT_WE_DID.md).

## Scope

| | |
|---|---|
| Endpoints | `PUT /cloud/impinjGen2X`, `PUT /cloud/mode`, `PUT /cloud/start` |
| Reader | `10.233.48.36`, reader app 5.0.7 |
| Date | 2026-09-06 |
| Feature | `tagProtect` only — all four documented actions |
| Chips tested | Monza X-2K Dura, Monza R6, one non-Impinj |
| Outcome | Every API call works; **no observable protection effect — cause not isolated** |

---

## 1. The procedure

### 1.1 Prerequisites

| What | Why |
|---|---|
| An **Impinj** tag whose silicon supports Protected Mode | TagProtect is Impinj-proprietary. Verify the chip — see [§1.2](#12-identify-the-chip-first) |
| A **32-bit access password** already written to the tag | TagProtect authenticates with it. Setting it is [step A](#step-a--write-the-access-password) |
| Tag data reaching an endpoint **you can read** | Access results arrive in the tag stream, not in the HTTP response |
| The tag within reliable read range | Every step executes during an inventory |

The documentation states *"The target tag must have a valid 32-bit Access
Password configured before using Protected Mode operations"* but does not say how
to configure one. **Step A is the missing piece.**

### 1.2 Identify the chip first

TagProtect is not universal across Impinj silicon. Read the TID and decode it
before anything else:

```json
{"type":"CUSTOM","antennas":[1],"transmitPower":30,
 "accesses":[{"type":"READ","config":{"membank":"TID","wordPointer":0,"wordCount":6}}],
 "tagMetaData":["ANTENNA","RSSI"]}
```

Then `PUT /cloud/start {}`, wait, `PUT /cloud/stop`, and read `accessResults`.

Decoding a TID such as `e28011c12000112dbc930317`:

| Bytes | Field | Value | Meaning |
|---|---|---|---|
| 0 | class | `E2` | ISO/IEC 15963 |
| 1–2 (upper 12 bits) | **MDID** | `0x801` | **Impinj** |
| 2–3 (lower 12 bits) | **TMN** | `0x1C1` | Monza X-2K |

| MDID | Vendor |
|---|---|
| **`0x801`** | **Impinj** — TagProtect possible |
| `0x806`, `0x803`, … | other vendors — TagProtect will never work |

| TMN | Chip |
|---|---|
| `0x1C1` | Monza X-2K Dura |
| `0x0C1` | Monza X-8K |
| `0x100` | Monza 4QT |
| `0x130` | Monza R6 |
| `0x160` / `0x170` | Monza R6-P / R6-A |

> ⚠️ **Then check the part against Impinj's Gen2X tag specification**
> (`http://www.impinj.com/Gen2X`). Decoding the TID tells you *which chip* you
> have; it does **not** tell you whether that chip implements Protected Mode.
> Zebra's own MAUI Gen2X tutorial makes this a prerequisite:
>
> > "Users should verify whether their tags support these operations by referring
> > to Impinj Gen2X tag specifications"
>
> An earlier version of this table marked specific TMNs as ✅/❌ supported. Those
> marks came from product-family knowledge, **not** from the Gen2X spec, and have
> been removed. Verifying the part is [Test A](#the-two-tests-that-would-settle-this)
> and it is still outstanding.

This step matters regardless: of the 17 "Impinj-looking" tags in our field (EPCs
starting `E280`), the strongest turned out to be MDID `0x806` — **not Impinj at
all**. An `E280` EPC prefix tells you nothing; only the TID identifies the
vendor.

### Step A — Write the access password

The Gen2 RESERVED bank layout is fixed by the EPC Gen2 spec:

| Words | Contents |
|---|---|
| 0–1 | Kill password (32 bits) |
| **2–3** | **Access password (32 bits)** |

So write 8 hex characters (2 words = 32 bits) at `wordPointer: 2`:

```json
{"type":"CUSTOM","antennas":[1],"transmitPower":30,
 "filter":{"value":"333311112222333344445555","match":"prefix","operation":"include"},
 "accesses":[{"type":"WRITE",
              "config":{"membank":"RESERVED","wordPointer":2,"data":"A1B2C3D4"}}],
 "tagMetaData":["ANTENNA","RSSI"]}
```

```
PUT /cloud/mode    ← the payload above
PUT /cloud/start   {}
   ... wait ~12 s ...
PUT /cloud/stop
```

> ⚠️ **The `filter` is not optional in practice.** Without it the WRITE applies to
> **every tag in the field** — 24 tags were present during this testing, and all
> of them would have had their access password set. Use the full EPC as a
> `prefix` match to target exactly one tag.

Expected `accessResults` in the tag stream:

```
x76  ["SUCCESS"]
x4   ["Error after 0 successful words written: CRC error in tag response"]
x2   ["Error after 0 successful words written: Tag did not respond"]
```

Retries are normal RF behaviour. The `SUCCESS` count is what matters.

### Step B — Verify the password landed

**Do not skip this.** Every later `tagProtect` call returns HTTP 200 whether the
password is right or wrong, so this read is the only checkpoint you get.

```json
{"type":"CUSTOM","antennas":[1],"transmitPower":30,
 "filter":{"value":"333311112222333344445555","match":"prefix","operation":"include"},
 "accesses":[{"type":"READ","config":{"membank":"RESERVED","wordPointer":0,"wordCount":4}}],
 "tagMetaData":["ANTENNA","RSSI"]}
```

| | `accessResults` | Kill | **Access** |
|---|---|---|---|
| before | `0000000000000000` | `00000000` | `00000000` |
| after | `a1b2c3d4a1b2c3d4` | `a1b2c3d4` | **`a1b2c3d4`** ✅ |

### Step C — Configure TagProtect

```json
PUT /cloud/impinjGen2X
{"tagProtect": {"action": "enableTagProtection",
                "password": "A1B2C3D4",
                "tagID": "333311112222333344445555",
                "enableShortRange": false}}
```

```json
→ 200 {"message":"Success: Gen2X configured. Use applyImpinjGen2X flag in start command to apply features."}
```

**This only saves the configuration.** Confirmed immediately after the 200:

```
GET /cloud/impinjGen2X  → the tagProtect object, stored ✅
GET /cloud/status       → "impinjGen2X":{"feature":"none","isActive":false}  ← NOT active
```

### Step D — Apply it with the start flag

```json
PUT /cloud/start
{"applyImpinjGen2X": true}
```

```json
→ 200 {"message":"Success: Radio started with Gen2X. Note: Gen2X will not auto-start on reboot (normal mode will resume)."}
```

Now the feature is live:

```
GET /cloud/status → "impinjGen2X":{"feature":"tagProtect","isActive":true}  ✅
```

> ⚠️ **`applyImpinjGen2X: true` must be sent on every start.** The feature is
> per-inventory-session. After `PUT /cloud/stop` it reverts to
> `{"feature":"none","isActive":false}`, and a later plain `start {}` does **not**
> re-apply it even though the config is still saved.

### Step E — Reverse it, in this order

```json
PUT /cloud/impinjGen2X
{"tagProtect": {"action": "disableTagProtection",
                "password": "A1B2C3D4",
                "tagID": "333311112222333344445555"}}

PUT /cloud/start {"applyImpinjGen2X": true}
```

> ⚠️ **Unprotect before clearing the password.** If you zero the access password
> on a genuinely protected tag, you can no longer supply the password needed to
> unprotect it — the tag stays RF-silent to any reader that does not know the old
> value. Order: **unprotect → apply → then** write `00000000` back to RESERVED
> words 2–3.

### 1.3 The four actions and their shapes

The schema is a `oneOf` with two branches, and **`tagID` placement is the
difference**:

| Action | Scope | `tagID` |
|---|---|---|
| `enableTagProtection` | one tag | **required** |
| `disableTagProtection` | one tag | **required** |
| `enableTagVisibility` | the reader | **must be omitted** |
| `disableTagVisibility` | the reader | **must be omitted** |

The visibility actions control whether **this reader** can see protected tags —
they do not protect or unprotect anything. Easy to conflate; worth stating
explicitly in the docs.

`password` is pattern-checked `^[0-9A-Fa-f]{8}$` — exactly 8 hex characters.

---

## 2. Test results

| # | Step | Result |
|---|---|---|
| 01 | Write access password via `set_mode` WRITE | ✅ **76 × SUCCESS** |
| 02 | Verify password by reading RESERVED | ✅ **`a1b2c3d4` confirmed** |
| 03 | `enableTagProtection` | ✅ 200, stored (not yet applied) |
| 04 | Apply via `applyImpinjGen2X: true` | ✅ 200, **`feature: tagProtect, isActive: true`** |
| 05 | `disableTagVisibility` | ✅ 200, stored and applied |
| 06 | `disableTagProtection` | ✅ 200, stored and applied |

Every API call in the chain works. All four documented actions return 200, both
`oneOf` branches validate correctly, and the feature demonstrably activates.

**But no protection effect was observable** — the tag stayed readable.

That result is *inconclusive rather than negative*: visibility was measured only
from the reader that held the password, which reads the tag whether or not it is
protected. See [§3.3](#33--no-observable-effect--but-the-test-could-not-have-detected-success)
and [`WHAT_WE_DID.md` §5](WHAT_WE_DID.md).

---

## 3. Findings

### 3.1 🐛 The two-step apply flow is documented on the wrong page

`PUT /cloud/impinjGen2X` returns:

```
"Success: Gen2X configured. Use applyImpinjGen2X flag in start command to apply features."
```

The `applyImpinjGen2X` flag is documented under **`PUT /cloud/start`**. The
`impinjGen2X` endpoint description lists the supported TagProtect actions and the
full request schema, but **never mentions that a start call is required**.

Anyone reading only the `impinjGen2X` page will configure TagProtect, see
`GET /cloud/impinjGen2X` return their config, see `GET /cloud/status` report
`feature: none`, and reasonably conclude the feature is broken.

**Ask:** state the two-step flow in the `impinjGen2X` description, with a pointer
to the flag.

### 3.2 🐛 The prerequisite is stated but not explained

The docs say the tag must have a valid 32-bit access password "configured" —
without saying that:

- it lives in **RESERVED bank words 2–3**
- you set it with a `WRITE` access operation through **`PUT /cloud/mode`**
- the write **executes during an inventory**, not on the PUT
- **without a `filter` you write it to every tag in the field**

That last point is a footgun. This report's [Step A](#step-a--write-the-access-password)
is the procedure that was missing.

### 3.3 ⚠️ No observable effect — but the test could not have detected success

> **Correction.** An earlier version of this section was headed *"The tag never
> becomes RF-silent"* and reported this as a firmware defect. **That conclusion
> overstated the evidence.** Two flaws in the method, both explained in
> [`WHAT_WE_DID.md` §5](WHAT_WE_DID.md):
>
> 1. **Visibility was measured from the reader that held the password.** Protected
>    Mode hides a tag *unless the reader supplies the correct password*. Our
>    reader supplied it. So a protected tag and an unprotected tag look
>    identical from this reader — the observation has no discriminating power.
> 2. **Chip capability was assumed, not verified.** Monza X-2K was marked
>    "supported" from product-family knowledge, not from Impinj's Gen2X tag
>    specification, which Zebra's own MAUI tutorial says to check.
>
> The supportable claim is therefore: **no observable effect, cause not
> isolated.** Whether TagProtect works on 5.0.7 is still open. The two tests that
> would settle it are listed at the end of this section.

This is the headline negative result. TagProtect is described as rendering a tag
"invisible to an RFID reader… RF silent… does not respond to Gen2 commands unless
the reader first provides the correct 32-bit password."

Observed on every attempt:

| Chip | TMN | Password verified | After protect + apply | Meaningful? |
|---|---|---|---|---|
| Monza X-2K Dura | `0x1C1` | ✅ `a1b2c3d4` | **still visible**, reads=1 | the only candidate |
| Monza R6 | `0x130` | ✅ `a1b2c3d4` | still visible | ✗ Gen2X capability unverified |
| non-Impinj | MDID `0x806` | ✅ `a1b2c3d4` | still visible | ✗ not Impinj — cannot work |

Only the **X-2K** row carries any weight. The non-Impinj tag could never have
worked, and the R6's capability was never verified against Impinj's Gen2X spec —
so two of the three rows are dead ends rather than evidence, and both were tested
before the TID was decoded (see [`WHAT_WE_DID.md` §5.4](WHAT_WE_DID.md)).

On the X-2K the password was confirmed on the tag by read-back, and the
reader reported `feature: tagProtect, isActive: true` during the inventory.

The tag's RESERVED bank also stayed readable after protection was applied:

```
RESERVED read after protect: ["00000000a1b2c3d4"]
```

> **This is not evidence of failure**, contrary to what an earlier version of this
> report claimed. Two reasons: our reader was authenticated (it held the
> password), and **Protected Mode governs RF visibility, not memory locking** —
> locking RESERVED is a separate Gen2 `Lock` command that was never issued. A
> protected tag answering its own authenticated reader on an unlocked bank is
> expected behaviour.

#### What was genuinely ruled out

| Hypothesis | How it was excluded |
|---|---|
| Password not on the tag | Read back and confirmed `a1b2c3d4` on all three tags before protecting |
| Wrong memory bank/offset | Gen2 spec RESERVED words 2–3; corroborated by Zebra's MAUI tutorial (`MemoryBankReserved`, `Offset = 2`, `WriteDataLength = 2`) |
| Config not applied | `status` showed `feature: tagProtect, isActive: true` during the inventory |
| Command never reached the radio | `radio_control.log` shows two access operations built and armed — below |
| Needs a second inventory | Ran further inventories; tag still visible |
| Tag out of range | Read at −55 dBm throughout, reads in every window |
| Non-Impinj silicon | Repeated on a TID-decoded Impinj part (MDID `0x801`) |

#### What was NOT ruled out

| Hypothesis | Why it is still open |
|---|---|
| **The chip is not Gen2X-capable** | Monza X-2K was marked supported from product-family knowledge, **not** from Impinj's Gen2X tag spec. Never checked |
| **Protection worked and we could not see it** | Visibility was measured only from the reader holding the password, which reads the tag either way |
| Per-tag operation failed on the tag | TagProtect returns no `accessResults` and logs no outcome, so this is invisible |
| An undocumented step is missing | e.g. a `Lock` or QT sequence the MAUI SDK performs internally |

Either of the first two would fully explain every observation with no firmware
defect involved.

#### The reader *does* build the protect operations

From `radio_control.log` at the moment of apply — this is why the failure looks
like silicon or protocol rather than a dropped command:

```
08:08:23.966 INFO requests.cpp Request: impinjgen2x {"tagProtect":{"action":
             "enableTagProtection","enableShortRange":false,
             "password":"A1B2C3D4","tagID":"41544035a880c80000123bea"}}
08:08:23.966 INFO requests.cpp Response: Success: Gen2X configured...
08:08:26.661 INFO impinjGen2X.cpp mergeImpinjGen2xWithMode:
               ===== FINAL MERGE RESULT =====
               Total SELECT operations: 0
               Total ACCESS operations: 2          ← two Gen2 accesses built
               accessBitMask: 0x0000000000000003   ← both enabled
08:08:26.708 INFO requests.cpp Request: start gen2x
08:08:26.709 INFO requests.cpp Response: Success: Radio started with Gen2X.
```

Contrast the same log lines for `{"fastID":{"enabled":false}}` minutes earlier:
`Total ACCESS operations: 0`, `accessBitMask: 0x0`. So TagProtect **is**
translated into two access operations and armed on the radio.

**No error is logged anywhere.** `RgErrorLog` contains only unrelated earlier
`set_mode` failures — nothing about the protect attempt. The reader reports
success at every layer and the tag stays readable.

#### What was not established

Whether the per-tag Gen2 access operations **succeeded or failed on the tag**.
Unlike `set_mode` accesses, TagProtect's operations produce no `accessResults` in
the tag stream and nothing in the logs, so their outcome is invisible.

Three possibilities remain open and cannot be distinguished from what was
measured:

1. **Protection worked.** The tag is protected, and our reader reads it because it
   holds the password — exactly as designed. Nothing is wrong.
2. The operations are issued but the tag rejects them (password handling, command
   encoding, or a lock/QT sequence the chip needs first).
3. The operations succeed but the reader keeps singulating the tag anyway —
   protection set but not honoured.

#### The two tests that would settle this

Neither has been run. Either could close the question without a firmware defect.

**Test A — verify the chip is Gen2X-capable.** A document lookup, not a reader
test. Check the Monza X-2K Dura part against Impinj's Gen2X tag specification
(`http://www.impinj.com/Gen2X`), as Zebra's MAUI Gen2X tutorial instructs. If the
part is not Gen2X, every observation is explained. **Do this first — it is free.**

**Test B — read the protected tag from a second reader.** Protect the tag on
`10.233.48.36`, then inventory it from `10.117.229.9`, which does not know the
password:

| Second reader sees | Verdict |
|---|---|
| **Nothing** | Protection **worked**. Possibility 1. No defect — and this report's original conclusion was wrong |
| **The tag** | Protection genuinely failed. Possibility 2 or 3, worth escalating |

This is the decisive test. `10.117.229.9` is available but was not used.

### 3.4 The Gen2X feature is per-session, not persistent

| Point | `status.impinjGen2X` |
|---|---|
| after `PUT /cloud/impinjGen2X` | `{"feature":"none","isActive":false}` |
| after `start {"applyImpinjGen2X":true}` | `{"feature":"tagProtect","isActive":true}` |
| after `PUT /cloud/stop` | `{"feature":"none","isActive":false}` |
| after a later plain `start {}` | `{"feature":"none","isActive":false}` |

The saved config survives (`GET /cloud/impinjGen2X` still returns it), but the
**activation does not**. The reader's own note says *"Gen2X will not auto-start on
reboot"* — the reality is stronger: it does not carry across inventory sessions
either.

### 3.5 Three `set_mode` gotchas found while writing the password

All three block the prerequisite step and none is obvious from the docs:

| Payload | Response |
|---|---|
| `filter.match: "equals"` | 422 — *"must be a must be prefix, suffix, or regex (equals entered)"* |
| `query` + `filter` with `prefix` | 422 — *"`query` and `filter` with `prefix` cannot be configured at the same time"* |
| `wordCounter` in a READ config | 422 — *"wordCount must be included in access-config object for read"* |

- `match` accepts only `prefix`, `suffix`, `regex` — **no `equals`**. Use the full
  EPC as a `prefix` for single-tag targeting.
- Drop `query` when filtering by prefix. (A documented constraint — confirmed.)
- The spec's own `with_accesses` example uses **`wordCounter`**; the firmware
  requires **`wordCount`**. Already reported in
  [`../cloud-mode-PUT/MODE_TEST_REPORT.md`](../cloud-mode-PUT/MODE_TEST_REPORT.md).

The first message is also malformed — *"must be a must be"* plus stray escaping.

### 3.6 Writing RESERVED word 2 changed word 0 on the Monza X-2K

| Chip | Wrote at `wordPointer: 2` | Kill password after | Access password after |
|---|---|---|---|
| Monza X-2K | `A1B2C3D4` | **`a1b2c3d4`** ← also changed | `a1b2c3d4` |
| Monza R6 | `A1B2C3D4` | `00000000` unchanged | `a1b2c3d4` |
| non-Impinj | `A1B2C3D4` | `00000000` unchanged | `a1b2c3d4` |

On the X-2K both passwords ended up set, from a single 2-word write at offset 2.
Chip-specific behaviour — possibly a BlockWrite alignment or memory-mapping
difference. Worth knowing before writing RESERVED on unknown stock, since
inadvertently setting a **kill** password is worse than setting an access
password.

Not investigated further; recorded as observed.

---

## 4. Questions for Zebra

1. **Which chip was TagProtect validated against on 5.0.7 (highest priority)?**
   The full documented flow was followed with a read-back-verified password on a
   Monza X-2K; the reader reported `feature: tagProtect, isActive: true` and
   `radio_control.log` shows two access operations armed — but no protection
   effect was observable. Our test cannot distinguish "protection worked and our
   authenticated reader reads it anyway" from "protection failed", so we are
   asking rather than reporting a defect. A known-working chip + payload
   combination would let us verify our procedure.

2. **Which Impinj chips are supported?** Please list them. Monza R6 is common and
   does not implement Protected Mode, so "use an Impinj tag" is not sufficient
   guidance.

3. **Are the protect operations' results observable?** `set_mode` accesses return
   `accessResults` per tag; TagProtect returns nothing in the tag stream and logs
   no outcome. Without that, a failure is indistinguishable from a success.

4. **Should a failed protect operation surface an error?** Currently HTTP 200 at
   configure, HTTP 200 at apply, `isActive: true` in status, nothing in
   `RgErrorLog` — and no effect.

5. **Please document the prerequisite properly.** Where the access password lives
   (RESERVED words 2–3), that it is set with a `WRITE` access via
   `PUT /cloud/mode`, that it executes during an inventory, and that a `filter`
   is required to avoid writing to every tag in the field.

6. **Please document the two-step flow on the `impinjGen2X` page**, not only under
   `/cloud/start`.

7. **Is per-session activation intended?** `applyImpinjGen2X: true` must be
   repeated on every start. If so, say it — the current note mentions only reboot.

8. **`tagID` placement.** Required for the protection actions, forbidden for the
   visibility actions. Worth an explicit callout.

9. **Monza X-2K RESERVED write.** Writing 2 words at `wordPointer: 2` also
   changed words 0–1 (the kill password). Expected?

10. **`filter.match` has no `equals`.** Single-tag targeting via a full-EPC
    `prefix` works but reads as a workaround. And the error message is malformed:
    *"must be a must be prefix, suffix, or regex"*.

11. **No `AccessPassword` on REST WRITE operations.** The MAUI SDK passes
    `writeAccessParams.AccessPassword` to authenticate a write; the REST
    `accesses` WRITE config accepts only `membank`, `wordPointer`, `data`,
    `blockSize`. Harmless on a virgin tag (zero password), but can REST
    authenticate an access to a tag that IS protected?

12. **Please point to the Gen2X-capable part list.** Zebra's MAUI Gen2X tutorial
    says to verify tags against Impinj's Gen2X specification. A list of parts
    Zebra has validated TagProtect against would be more actionable.

---

## 5. Reader and tag state after testing

| | Pre-test | Post-test | |
|---|---|---|---|
| Mode | `CUSTOM`, antenna 1, 17 dBm | **byte-identical** | ✅ |
| `impinjGen2X` | `{"feature":"none","isActive":false}` | same | ✅ |
| Data endpoint | `DATA_AWS_CLOUD_EVENTS` connected | same | ✅ |
| Tag `3333…5555` access pwd | `00000000` | `00000000` | ✅ |
| Tag `4154…3bea` access pwd | `00000000` | `00000000` | ✅ |
| Tag `e280…e471` access pwd | `00000000` | `00000000` | ✅ |

All three tags were unprotected first, then had both passwords written back to
zero, verified by reading RESERVED words 0–3 on each. No tag was left protected
or password-locked.

---

## 6. Folder contents

```
01-write-access-password-via-set_mode/    the prerequisite - PUT /cloud/mode WRITE
02-verify-access-password/                read RESERVED back to confirm
03-enableTagProtection/                   PUT /cloud/impinjGen2X
04-apply-via-start-flag/                  PUT /cloud/start {"applyImpinjGen2X":true}
05-disableTagVisibility/                  the reader-scoped oneOf branch
06-disableTagProtection/                  reversal and cleanup order
evidence/                                 every raw MQTT tag capture
```

Each numbered folder holds `request body/request.json`, `response body/` with the
verbatim response, `http_status.txt`, and a `verification.txt` giving the full
method, observed results and gotchas.

`evidence/` holds the raw newline-delimited tag streams — `x2k_*` (Monza X-2K),
`imp_*` (Monza R6), `res_*`/`write*` (non-Impinj), `tid.ndjson` (the TID sweep
used for chip identification) and `z_*.ndjson` (per-tag password verification
after cleanup).

---

## 7. Related

| File | Contents |
|---|---|
| [`../cloud-mode-PUT/MODE_TEST_REPORT.md`](../cloud-mode-PUT/MODE_TEST_REPORT.md) | `PUT /cloud/mode` — all five modes, `accesses`, `wordCount` |
| [`../SETTINGS_ENDPOINTS_TEST_REPORT.md`](../SETTINGS_ENDPOINTS_TEST_REPORT.md) | The six settings endpoints |
| [`../../findings/`](../../findings/) | Every finding as its own folder with evidence |
