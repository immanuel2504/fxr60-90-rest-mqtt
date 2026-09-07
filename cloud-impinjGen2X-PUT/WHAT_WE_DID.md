# TagProtect — exactly what we did, in order

A chronological record of every tag chosen, every operation run, and every
payload sent. Written so anyone can reproduce the run or audit the method.

Companion to [`TAG_PROTECT_REPORT.md`](TAG_PROTECT_REPORT.md), which carries the
findings. This file is the raw method.

| | |
|---|---|
| Reader | `10.233.48.36`, reader app 5.0.7 |
| Date | 2026-09-06 |
| Auth | `GET /cloud/localRestLogin` with `admin:Zebra@123`, bearer token |
| Antenna | 1 only (2, 3, 4 report `disconnected` on this reader) |
| Power | 30 dBm throughout |
| Password used | `A1B2C3D4` |

---

## 0. Setup — where tag data went

The reader's normal data endpoint is AWS IoT, which **cannot be read back**. Every
access operation returns its result in the *tag stream*, not in the HTTP
response, so tag data had to be routed somewhere readable first.

```
PUT /cloud/config
```
```json
{"READER-GATEWAY":{"endpointConfig":{"data":{"event":{"connections":[{
  "name":"DATA_MQTT_VIA_CONFIG","type":"mqtt",
  "options":{"enableSecurity":false,
             "endpoint":{"hostName":"10.117.229.18","port":1883,"protocol":"tcp"},
             "additional":{"cleanSession":true,"clientId":"fxr60-lab-data",
                           "keepAlive":60,"qos":0},
             "publishTopic":["fxr60-lab/tevents"],"subscribeTopic":[]}}]}}}}}
```

Confirmed: `DATA_MQTT_VIA_CONFIG: connected`. Observed with:

```bash
mosquitto_sub -h 10.117.229.18 -p 1883 -t 'fxr60-lab/tevents'
```

Baseline captured before any change, for restore at the end:

```bash
GET /cloud/mode          → CUSTOM, antennas [1], transmitPower [17]
GET /cloud/impinjGen2X   → (empty)
GET /cloud/status        → "impinjGen2X":{"feature":"none","isActive":false}
```

---

## 1. Which tags — and how they were chosen

### 1.1 First sweep: read every TID in the field

```
PUT /cloud/mode
```
```json
{"type":"CUSTOM","antennas":[1],"transmitPower":30,
 "query":{"sel":"ALL","session":"S1","tagPopulation":256,"target":"A"},
 "accesses":[{"type":"READ","config":{"membank":"TID","wordPointer":0,"wordCount":6}}],
 "tagMetaData":["ANTENNA","RSSI"]}
```
```
PUT /cloud/start {}    → 200
  ... 12 s ...
PUT /cloud/stop        → 200
```

24 tags returned. The relevant ones:

| EPC | RSSI | TID | MDID | TMN |
|---|---|---|---|---|
| `e2806894000040017790e471` | −38 | `e2806894200040017790e471` | `0x806` | `0x894` |
| `e2806894000040017790ac71` | −44 | `e2806894200040017790ac71` | `0x806` | `0x894` |
| `41544035a880c80000123bea` | −53 | `e2801130200030fd816a089d` | **`0x801`** | `0x130` |
| `333311112222333344445555` | −55 | `e28011c12000112dbc930317` | **`0x801`** | `0x1C1` |
| `bedd11112222333344445555` | −70 | `e28011c12000110dbc930317` | **`0x801`** | `0x1C1` |

### 1.2 TID decode used

```
byte 0                    E2       ISO/IEC 15963 class
bytes 1-2, upper 12 bits  MDID     mask designer ID   0x801 = Impinj
bytes 2-3, lower 12 bits  TMN      tag model number
```

### 1.3 The three tags actually tested, and why

| # | EPC | Chip | Why chosen |
|---|---|---|---|
| **T1** | `e2806894000040017790e471` | MDID `0x806` — **not Impinj** | Chosen **first, by signal strength alone** (−38 dBm, strongest in field). Mistake: picked before decoding the TID |
| **T2** | `41544035a880c80000123bea` | Monza R6, TMN `0x130` | Chosen after realising T1 wasn't Impinj. Genuinely Impinj — but R6 has no Protected Mode |
| **T3** | `333311112222333344445555` | Monza X-2K Dura, TMN `0x1C1` | Chosen after realising R6 was wrong. The only plausible candidate present |

**T3 is the one that matters.** T1 and T2 were dead ends — see
[§5](#5-mistakes-in-the-method).

`bedd11112222333344445555` (the second X-2K) was kept **unprotected as a
control**, so any change in T3's behaviour could be compared against an identical
chip that was left alone.

---

## 2. The operations, in order, on T3

All six steps below were run on `333311112222333344445555` (Monza X-2K).

### Step 1 — Read RESERVED before touching anything

```
PUT /cloud/mode
```
```json
{"type":"CUSTOM","antennas":[1],"transmitPower":30,
 "filter":{"value":"333311112222333344445555","match":"prefix","operation":"include"},
 "accesses":[{"type":"READ","config":{"membank":"RESERVED","wordPointer":0,"wordCount":4}}],
 "tagMetaData":["ANTENNA","RSSI"]}
```
```
PUT /cloud/start {}  →  200      ... 11 s ...      PUT /cloud/stop  →  200
```

**Result** — `accessResults` × 95:

```
["0000000000000000"]
   kill password   (words 0-1) = 00000000
   ACCESS password (words 2-3) = 00000000      ← unset, factory default
```

### Step 2 — Write the 32-bit access password

```
PUT /cloud/mode
```
```json
{"type":"CUSTOM","antennas":[1],"transmitPower":30,
 "filter":{"value":"333311112222333344445555","match":"prefix","operation":"include"},
 "accesses":[{"type":"WRITE",
              "config":{"membank":"RESERVED","wordPointer":2,"data":"A1B2C3D4"}}],
 "tagMetaData":["ANTENNA","RSSI"]}
```
```
PUT /cloud/start {}  →  200      ... 12 s ...      PUT /cloud/stop  →  200
```

**Result:**

```
x76  ["SUCCESS"]
x4   ["Error after 0 successful words written: CRC error in tag response"]
x2   ["Error after 0 successful words written: Tag did not respond"]
x2   ["Error after 1 successful words written: Tag did not respond"]
```

`wordPointer: 2` because the Gen2 RESERVED bank is words 0–1 kill, **words 2–3
access**. `A1B2C3D4` is 8 hex chars = 2 words = 32 bits.

The `filter` restricts the write to one tag. Without it all 24 tags in the field
would have been given this password.

### Step 3 — Verify the password is on the tag

Same payload as Step 1.

**Result** — `accessResults` × 122:

```
["a1b2c3d4a1b2c3d4"]
   kill password   = a1b2c3d4      ← ALSO changed, see §6
   ACCESS password = a1b2c3d4      ← CONFIRMED
```

### Step 4 — Configure TagProtect

```
PUT /cloud/impinjGen2X
```
```json
{"tagProtect":{"action":"enableTagProtection",
               "password":"A1B2C3D4",
               "tagID":"333311112222333344445555",
               "enableShortRange":false}}
```

**Response** — HTTP 200:

```json
{"message":"Success: Gen2X configured. Use applyImpinjGen2X flag in start command to apply features."}
```

State immediately after:

```
GET /cloud/impinjGen2X → {"tagProtect":{"action":"enableTagProtection",
                          "enableShortRange":false,"password":"A1B2C3D4",
                          "tagID":"333311112222333344445555"}}     stored
GET /cloud/status      → "impinjGen2X":{"feature":"none","isActive":false}
                                                                   NOT active
```

### Step 5 — Set a plain inventory mode, then apply

The mode still had the filter and access from Step 3, which would have masked
every other tag. Cleared first:

```
PUT /cloud/mode
```
```json
{"type":"CUSTOM","antennas":[1],"transmitPower":30,"tagMetaData":["ANTENNA","RSSI"]}
```

Then applied the Gen2X config:

```
PUT /cloud/start
```
```json
{"applyImpinjGen2X":true}
```

**Response** — HTTP 200:

```json
{"message":"Success: Radio started with Gen2X. Note: Gen2X will not auto-start on reboot (normal mode will resume)."}
```

State **during** the inventory:

```
GET /cloud/status → "impinjGen2X":{"feature":"tagProtect","isActive":true}   ACTIVE
                    "radioActivity":"active"
```

After 12 s, `PUT /cloud/stop` → 200.

### Step 6 — Observe whether T3 disappeared

**Result:**

```
unique tags: 18
T3      333311112222333344445555:  VISIBLE, reads=1
CONTROL bedd11112222333344445555:  VISIBLE, reads=1
```

The tag was still read. **This observation is the flawed one** — see
[§5.1](#51-the-central-mistake-a-test-that-cannot-fail).

---

## 3. Additional operations run

### 3.1 `disableTagVisibility` (reader-scoped branch)

```
PUT /cloud/impinjGen2X
```
```json
{"tagProtect":{"action":"disableTagVisibility","password":"A1B2C3D4"}}
```

Note: **no `tagID`** — the schema's second `oneOf` branch forbids it. Applied via
`start {"applyImpinjGen2X":true}`. HTTP 200; T3 still visible (22 tags).

### 3.2 Re-read RESERVED after protection was applied

Same payload as Step 1, run while protection was supposedly active.

```
["00000000a1b2c3d4"]
```

I reported this as proof the tag wasn't protected. **That reasoning was wrong** —
see [§5.2](#52-the-reserved-read-proved-nothing).

### 3.3 Log inspection

```
GET /cloud/logs/RcLog          → radio_control.log
GET /cloud/logs/RgErrorLog     → per-restart error files
```

`radio_control.log` at the moment of apply:

```
08:08:23.966 INFO requests.cpp Request: impinjgen2x {"tagProtect":{...}}
08:08:23.966 INFO requests.cpp Response: Success: Gen2X configured...
08:08:26.661 INFO impinjGen2X.cpp mergeImpinjGen2xWithMode:
               Total SELECT operations: 0
               Total ACCESS operations: 2          ← operations built
               accessBitMask: 0x0000000000000003   ← both enabled
08:08:26.708 INFO requests.cpp Request: start gen2x
08:08:26.709 INFO requests.cpp Response: Success: Radio started with Gen2X.
```

Compare `{"fastID":{"enabled":false}}` minutes earlier: `Total ACCESS
operations: 0`, `accessBitMask: 0x0`.

`RgErrorLog`: **no entry** for the protect attempt.

### 3.4 The same six steps on T1 and T2

T2 (Monza R6) — identical sequence, password confirmed `a1b2c3d4`, tag still
visible after protect + apply.

T1 (non-Impinj) — identical sequence, password confirmed, tag still visible.
Also tested `disableTagVisibility` against it.

---

## 4. Cleanup, in the order it must be done

### 4.1 Unprotect first

```
PUT /cloud/impinjGen2X
```
```json
{"tagProtect":{"action":"disableTagProtection",
               "password":"A1B2C3D4",
               "tagID":"333311112222333344445555"}}
```
```
PUT /cloud/start {"applyImpinjGen2X":true}   →  200
  ... 8 s ...
PUT /cloud/stop
```

Repeated for T2.

**Order matters.** Zeroing the password on a genuinely protected tag leaves no
way to supply the password needed to unprotect it.

### 4.2 Then zero the passwords

```
PUT /cloud/mode
```
```json
{"type":"CUSTOM","antennas":[1],"transmitPower":30,
 "filter":{"value":"333311112222333344445555","match":"prefix","operation":"include"},
 "accesses":[{"type":"WRITE",
              "config":{"membank":"RESERVED","wordPointer":0,"data":"0000000000000000"}}],
 "tagMetaData":["ANTENNA","RSSI"]}
```

`wordPointer: 0` with 16 hex chars = 4 words, clearing **both** passwords (needed
because the X-2K write had also set the kill password).

For T1, only the access password had changed, so `wordPointer: 2` with
`"00000000"`.

### 4.3 Verified

Read RESERVED words 0–3 on each:

```
333311112222333344445555  kill=00000000  access=00000000   RESTORED
41544035a880c80000123bea  kill=00000000  access=00000000   RESTORED
e2806894000040017790e471  kill=00000000  access=00000000   RESTORED
```

### 4.4 Reader restored

```
PUT /cloud/impinjGen2X  {"fastID":{"enabled":false}}     clear Gen2X
PUT /cloud/mode         <the baseline object from §0>    byte-identical ✅
PUT /cloud/config       <the AWS endpoint config>        DATA_AWS_CLOUD_EVENTS connected ✅
GET /cloud/status       "impinjGen2X":{"feature":"none","isActive":false} ✅
```

---

## 5. Mistakes in the method

Stated plainly, because they affect how much the result is worth.

### 5.1 The central mistake: a test that cannot fail

Protected Mode makes a tag invisible **unless the reader supplies the correct
password**. Our reader held the password.

| | Tag IS protected | Tag NOT protected |
|---|---|---|
| Reader knows password | reads it | reads it |

Both columns are identical. **We measured visibility from the one reader that
could never show a difference**, so "T3 still visible" was never evidence either
way.

**Fix:** inventory the protected tag from a *second* reader that does not know
the password. `10.117.229.9` is available for this and the test has not been run.

### 5.2 The RESERVED read proved nothing

I presented `["00000000a1b2c3d4"]` after protection as the clincher. Two errors:

1. Same flaw as §5.1 — our reader was authenticated.
2. **Protected Mode governs RF visibility, not memory locking.** Locking RESERVED
   is a separate Gen2 `Lock` command we never issued. A protected tag answering
   its own authenticated reader on an unlocked bank is expected.

### 5.3 Chip capability was assumed, not verified

I decoded TMN `0x1C1` → Monza X-2K and wrote a support table into the report
marking it ✅ supported. That came from product-family knowledge, **not** from
Impinj's Gen2X tag specification.

Zebra's MAUI Gen2X tutorial says explicitly:

> "Users should verify whether their tags support these operations by referring
> to Impinj Gen2X tag specifications: http://www.impinj.com/Gen2X"

We never checked it. If the X-2K Dura is not a Gen2X part, every observation is
explained and there is no firmware defect.

### 5.4 Tag chosen before the TID was decoded

T1 was picked on signal strength alone and turned out to be MDID `0x806` — not
Impinj. Two full write/verify/protect cycles were spent on T1 and T2 before
reaching a plausible candidate. Only cost is time, but it means two of the three
result rows were never meaningful.

**Fix:** decode TIDs first, then choose.

### 5.5 The conclusion overstated the evidence

Finding 3.3 originally read *"The tag never becomes RF-silent"* and presented the
result as a firmware defect. Given §5.1–5.3, the supportable claim is **"no
observable effect; cause not isolated, chip capability unverified."**

**Corrected.** `TAG_PROTECT_REPORT.md` §3.3 now carries that wording, the
unverified ✅/❌ chip-support marks have been removed from §1.2, the RESERVED-read
"proof" is marked as not evidence, and the lead question asks Zebra which chip
TagProtect was validated against rather than asserting it is broken.

---

## 6. Incidental observations

### 6.1 Writing RESERVED word 2 also set word 0 on the X-2K

| Tag | Chip | Wrote at `wordPointer:2` | Kill after | Access after |
|---|---|---|---|---|
| T3 | Monza X-2K | `A1B2C3D4` | **`a1b2c3d4`** changed | `a1b2c3d4` |
| T2 | Monza R6 | `A1B2C3D4` | `00000000` unchanged | `a1b2c3d4` |
| T1 | non-Impinj | `A1B2C3D4` | `00000000` unchanged | `a1b2c3d4` |

A single 2-word write at offset 2 set both passwords on the X-2K. Chip-specific;
worth knowing because setting a **kill** password by accident is worse than an
access password.

### 6.2 `set_mode` payload errors hit along the way

| Sent | Response |
|---|---|
| `"match":"equals"` | 422 — *"must be a must be prefix, suffix, or regex (equals entered)"* |
| `query` + `filter` with `prefix` | 422 — *"`query` and `filter` with `prefix` cannot be configured at the same time"* |
| `"wordCounter"` in a READ config | 422 — *"wordCount must be included in access-config object for read"* |

`match` has no `equals`; use the full EPC as a `prefix`. Drop `query` when
filtering by prefix. The spec's own `with_accesses` example uses `wordCounter`,
which the firmware rejects.

### 6.3 REST has no `AccessPassword` on WRITE

The MAUI SDK passes `AccessPassword` on the write operation to authenticate it:

```csharp
writeAccessParams.AccessPassword = 0x00000000;
```

The REST `accesses` WRITE config accepts only `membank`, `wordPointer`, `data`,
`blockSize` — no equivalent. Harmless on a virgin tag (zero password, no auth
needed), but it suggests REST may be unable to authenticate accesses to a tag
that *is* protected.

---

## 7. Reproducing this

```
1.  Route tag data somewhere readable            PUT /cloud/config     §0
2.  Capture baseline mode + Gen2X state          GET /cloud/mode       §0
3.  Read all TIDs, decode MDID/TMN               PUT /cloud/mode       §1.1
4.  Verify the chip against Impinj's Gen2X spec  (document lookup)     §5.3
5.  Read RESERVED w0-3 on the chosen tag         PUT /cloud/mode       §2.1
6.  Write the password at wordPointer 2          PUT /cloud/mode       §2.2
7.  Read RESERVED back and confirm               PUT /cloud/mode       §2.3
8.  Configure TagProtect                         PUT /cloud/impinjGen2X §2.4
9.  Clear the filter, apply with the start flag  PUT /cloud/start      §2.5
10. Inventory FROM A SECOND READER               (not yet done)        §5.1
11. Unprotect, then zero the password            §4.1 then §4.2
12. Restore mode, Gen2X and data endpoint        §4.4
```

Step 4 and step 10 are the two we skipped. Either could change the conclusion.

Every payload above is stored verbatim in the numbered folders beside this file;
the raw MQTT tag streams are in [`evidence/`](evidence/).
