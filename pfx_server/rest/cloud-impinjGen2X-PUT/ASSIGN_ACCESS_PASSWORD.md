# How to Assign an Access Password Before Using Protected Mode

Protected Mode requires the target tag to already have a valid 32-bit access
password. Assign one by writing 8 hexadecimal characters to the Gen2 `RESERVED`
bank at `wordPointer: 2`.

| Words | Contents |
|---|---|
| 0–1 | Kill password |
| **2–3** | **Access password** ← write here |

---

## 1. Assign the password

### REST — `PUT /cloud/mode`

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

### MQTT — `set_mode`

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

Then run an inventory — the write executes when the tag is singulated, not when
the command returns:

| Action | REST | MQTT |
|---|---|---|
| Start | `PUT /cloud/start` with `{}` | `{"command": "start", "payload": {}}` |
| Stop | `PUT /cloud/stop` | `{"command": "stop", "payload": {}}` |

Result in the tag data stream:

```json
{"data": {"idHex": "e28011b0a5050076c4d7530a", "accessResults": ["SUCCESS"]}}
```

> Include the `filter`. Without it the password is written to **every tag in the
> field**.

---

## 2. Use it with Protected Mode

### REST — `PUT /cloud/impinjGen2X`

```json
{
  "tagProtect": {
    "action": "enableTagProtection",
    "password": "A1B2C3D4",
    "tagID": "e28011b0a5050076c4d7530a"
  }
}
```

### MQTT — `set_impinjGen2X`

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

Apply it on the next start:

| REST | MQTT |
|---|---|
| `PUT /cloud/start` with `{"applyImpinjGen2X": true}` | `{"command": "start", "payload": {"applyImpinjGen2X": true}}` |

---

## Password rules

- Exactly **8 hex characters** (`0`–`9`, `A`–`F`) — 32 bits
- Case-insensitive: `a1b2c3d4` = `A1B2C3D4`
- **Do not use `00000000`** — that means "no password" on a Gen2 tag, so it
  cannot protect anything. The API accepts it without warning.

---

## Commands used

| Purpose | REST | MQTT |
|---|---|---|
| Write the password | `PUT /cloud/mode` | `set_mode` |
| Start inventory | `PUT /cloud/start` | `start` |
| Stop inventory | `PUT /cloud/stop` | `stop` |
| Configure Protected Mode | `PUT /cloud/impinjGen2X` | `set_impinjGen2X` |

---

*Verified on FXR60 5.0.7 and FXR90 5.0.4 with Impinj Monza 4i tags.*
