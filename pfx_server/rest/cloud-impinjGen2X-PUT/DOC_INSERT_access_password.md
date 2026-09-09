# Documentation insert — assigning the TagProtect access password

Drop-in text for the REST and MQTT documentation of `PUT /cloud/impinjGen2X` /
`set_impinjGen2X`.

**Why it is needed.** Every TagProtect action authenticates against a 32-bit
access password that must already be stored on the tag. Neither document states
this prerequisite, and neither explains where the password lives or how to set
one.

The closest existing text is in the `disableTagProtection` row of
`## 5. Choosing TagProtect Actions`:

> `password` must match the tag's existing access password exactly.

That implies the tag has a password but never says how it got one. In testing,
`enableTagProtection` with a password that does not match the tag returns
`200 OK` and silently leaves the tag unprotected — so a reader who misses this
has no error to work from.

Three changes are proposed:

| # | Where | Change |
|---|---|---|
| A | `## 3. Before You Begin`, TagProtect password row | Replace one table row |
| B | `## 5. Choosing TagProtect Actions`, `enableTagProtection` row | Add the prerequisite to *Key Constraints* |
| C | `## 5. Choosing TagProtect Actions`, at the end | Add a new subsection |

Everything else in both documents stays as it is.

---

## Change A — one row in `## 3. Before You Begin`

**Current row:**

| What You Need | Details |
|---|---|
| TagProtect password | An 8-character hex string (32-bit) is required for all TagProtect actions. |

**Replace with:**

| What You Need | Details |
|---|---|
| TagProtect password | An 8-character hex string (32-bit) is required for all TagProtect actions. **The target tag must already have a valid 32-bit access password configured before any Protected Mode operation.** The tag's access password occupies words 2–3 of the `RESERVED` memory bank. Read it, or assign one, using a `set_mode` access operation before configuring TagProtect — see [Assigning the Access Password](#assigning-the-access-password). Many tags ship with a password already set; read it first and use that value. |

---

## Change B — `enableTagProtection` row in `## 5. Choosing TagProtect Actions`

**Current row:**

| Action | What It Does | Required Fields | Key Constraints |
|---|---|---|---|
| `enableTagProtection` | Permanently protects a tag; the tag becomes invisible to standard reads until unprotected. | `password`, `tagID` | `password` must be exactly 8 hex characters. Optional `enableShortRange` reduces read range during protection. |

**Replace the Key Constraints cell with:**

> `password` must be exactly 8 hex characters **and must match the access
> password already stored on the target tag** — see
> [Assigning the Access Password](#assigning-the-access-password). A password
> that does not match the tag returns `200 OK` and leaves the tag unprotected.
> Optional `enableShortRange` reduces read range during protection.

---

## Change C — new subsection at the end of `## 5. Choosing TagProtect Actions`

Insert the following after the existing `> Important:` note at the end of that
section.

---

### Assigning the Access Password

Every TagProtect action authenticates against the tag's 32-bit access password,
which must already be stored on the tag. The access password occupies words 2–3
of the Gen2 `RESERVED` memory bank:

| Words | Contents |
|---|---|
| 0–1 | Kill password |
| **2–3** | **Access password** |

Reading and writing this bank is done with a `set_mode` access operation, not
through `impinjGen2X`. Because access operations execute when the tag is
singulated, each read or write must be followed by an inventory.

#### Step 1 — Read the current password

Many tags are supplied with an access password already programmed. Read words 0–3
before assigning a new one.

**REST** — `PUT /cloud/mode`

```json
{
  "type": "CUSTOM",
  "antennas": [1],
  "transmitPower": 30,
  "filter": {
    "value": "e28011b0a5050076c4d7530a",
    "match": "prefix",
    "operation": "include"
  },
  "accesses": [
    {
      "type": "READ",
      "config": {
        "membank": "RESERVED",
        "wordPointer": 0,
        "wordCount": 4
      }
    }
  ]
}
```

**MQTT** — `set_mode`

```json
{
  "command": "set_mode",
  "payload": {
    "type": "CUSTOM",
    "antennas": [1],
    "transmitPower": 30,
    "filter": {
      "value": "e28011b0a5050076c4d7530a",
      "match": "prefix",
      "operation": "include"
    },
    "accesses": [
      {
        "type": "READ",
        "config": {
          "membank": "RESERVED",
          "wordPointer": 0,
          "wordCount": 4
        }
      }
    ]
  }
}
```

Run an inventory to execute the read:

| Action | REST | MQTT |
|---|---|---|
| Start | `PUT /cloud/start` with `{}` | `{"command": "start", "payload": {}}` |
| Stop | `PUT /cloud/stop` | `{"command": "stop", "payload": {}}` |

The result arrives in `accessResults` in the tag data stream as 16 hexadecimal
characters covering words 0–3:

```json
{"data": {"idHex": "e28011b0a5050076c4d7530a",
          "accessResults": ["1234876512348765"]}}
```

| Characters | Field |
|---|---|
| 1–8 | Kill password (words 0–1) |
| **9–16** | **Access password (words 2–3)** |

| Value read | Action |
|---|---|
| `0000000000000000` | No password set — assign one in step 2 |
| Any other value | A password is already set — use the last 8 characters and skip step 2 |

#### Step 2 — Assign a password

Write 8 hexadecimal characters (2 words = 32 bits) to `wordPointer: 2`.

**REST** — `PUT /cloud/mode`

```json
{
  "type": "CUSTOM",
  "antennas": [1],
  "transmitPower": 30,
  "filter": {
    "value": "e28011b0a5050076c4d7530a",
    "match": "prefix",
    "operation": "include"
  },
  "accesses": [
    {
      "type": "WRITE",
      "config": {
        "membank": "RESERVED",
        "wordPointer": 2,
        "data": "A1B2C3D4"
      }
    }
  ]
}
```

**MQTT** — `set_mode`

```json
{
  "command": "set_mode",
  "payload": {
    "type": "CUSTOM",
    "antennas": [1],
    "transmitPower": 30,
    "filter": {
      "value": "e28011b0a5050076c4d7530a",
      "match": "prefix",
      "operation": "include"
    },
    "accesses": [
      {
        "type": "WRITE",
        "config": {
          "membank": "RESERVED",
          "wordPointer": 2,
          "data": "A1B2C3D4"
        }
      }
    ]
  }
}
```

Run an inventory as in step 1. Each singulation produces a result:

```json
{"data": {"idHex": "e28011b0a5050076c4d7530a", "accessResults": ["SUCCESS"]}}
```

Intermittent `CRC error in tag response` or `Tag did not respond` entries are
normal RF behaviour when the tag is at the edge of range; at least one `SUCCESS`
confirms the write.

> **Include a `filter`.** Without one, the write is applied to every tag in the
> field. Use the target EPC with `"match": "prefix"` to address a single tag.

> **Do not use `00000000`.** A zero access password means "no password set" on a
> Gen2 tag, so the tag cannot be protected. The request is accepted without
> error.

#### Step 3 — Verify

Repeat the step 1 read. The last 8 characters of `accessResults` must match the
password that was written:

```json
{"data": {"idHex": "e28011b0a5050076c4d7530a",
          "accessResults": ["00000000a1b2c3d4"]}}
```

Verification is required because TagProtect requests are accepted whether or not
the supplied password matches the tag. A password mismatch returns `200 OK` and
leaves the tag unprotected.

#### Step 4 — Configure TagProtect

Use the same password in the TagProtect request.

**REST** — `PUT /cloud/impinjGen2X`

```json
{
  "tagProtect": {
    "action": "enableTagProtection",
    "password": "A1B2C3D4",
    "tagID": "e28011b0a5050076c4d7530a"
  }
}
```

**MQTT** — `set_impinjGen2X`

```json
{
  "command": "set_impinjGen2X",
  "payload": {
    "tagProtect": {
      "action": "enableTagProtection",
      "password": "A1B2C3D4",
      "tagID": "e28011b0a5050076c4d7530a"
    }
  }
}
```

Apply it on the next inventory start:

| REST | MQTT |
|---|---|
| `PUT /cloud/start` with `{"applyImpinjGen2X": true}` | `{"command": "start", "payload": {"applyImpinjGen2X": true}}` |

#### Password requirements

| Requirement | Notes |
|---|---|
| Length | Exactly 8 hexadecimal characters (32-bit) |
| Characters | `0`–`9` and `A`–`F` only |
| Case | Not significant — `a1b2c3d4` and `A1B2C3D4` are equivalent |
| Reserved value | `00000000` must not be used; it denotes "no password" on a Gen2 tag |

#### Changing or clearing a password

Writing to words 2–3 again replaces the previous value; there is no separate
change operation.

> Unprotect the tag with `disableTagProtection` before changing or clearing its
> access password. If the password is changed while the tag is protected, the
> value required to unprotect it can no longer be supplied and the tag remains
> unreadable.

---

## Verification

Every payload above was executed against live readers:

| | |
|---|---|
| Readers | FXR60 reader application 5.0.7; FXR90 reader application 5.0.4 |
| Tags | Impinj Monza 4i (MDID `0x801`, TMN `0x1B0`) |
| Protect confirmed | Target tag visible 5/5 inventories before protection, 0/5 after, with a control tag visible 5/5 throughout |
| Restored | `disableTagProtection` returned the tag to 5/5 visibility |

Supporting detail, including the measurement and raw captures:
[`tagprotect-CONFIRMED-monza4i/TAGPROTECT_CONFIRMED.md`](tagprotect-CONFIRMED-monza4i/TAGPROTECT_CONFIRMED.md)
