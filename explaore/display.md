# Display (FXR60)

Display is the **screen on an FXR60** (HDMI monitor). These APIs are **not on FXR90**.

This file collects the display walkthrough: what the endpoints are, every field, and every scenario we used.

---

## Endpoints (3 operations, 2 paths)

| # | Method | Path | MQTT | What it does |
|---|---|---|---|---|
| 1 | `GET` | `/cloud/displayConfig` | `get_displayConfig` | Read the 7 screen settings |
| 2 | `PUT` | `/cloud/displayConfig` | `set_displayConfig` | Change settings. Success body is `{}` |
| 3 | `GET` | `/cloud/inputOutputDevices` | `get_inputOutputDevices` | What is plugged in (keyboard, mouse, touch, monitor) |

Auth: Bearer token (`Authorization: Bearer <token>`).

| Call | Result looks like |
|---|---|
| PUT `/cloud/displayConfig` | `{}` — accepted, does **not** echo settings |
| GET `/cloud/displayConfig` | The 7 config fields |
| GET `/cloud/inputOutputDevices` | Hardware status + `monitor.details` |

`displayConfig` = what you **configured**.  
`inputOutputDevices` = what is **attached**.

---

## Scenario A — Warehouse door: turn the screen on after plugging HDMI

An FXR60 is at a door. A monitor is plugged in so operators can see a local page without a laptop.

### 1. Confirm the monitor is plugged in

```http
GET /cloud/inputOutputDevices
```

Check:

- `monitor.status` = `connected`
- Copy a size from `monitor.details[].supportedResolutions` (e.g. `1920x1080`)

If `disconnected`, PUT will not show a picture. Plug HDMI in first.

### 2. Turn the screen on and choose what it shows

```http
PUT /cloud/displayConfig
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "enable": true,
  "enableOnscreenKeyboard": true,
  "startUrl": "https://localhost/",
  "resolution": "1920x1080",
  "orientation": "landscape",
  "screenTimeoutSec": 300,
  "keyboardLayout": "Japanese"
}
```

Success:

```json
{}
```

| Setting | What the operator sees |
|---|---|
| `enable: true` | Monitor is on |
| `startUrl` | The page on the screen |
| `resolution` | Full HD — must be in `supportedResolutions` |
| `orientation: landscape` | Wide picture |
| `screenTimeoutSec: 300` | After 5 minutes idle, the screen blanks |
| `enableOnscreenKeyboard: true` | Type on the glass if there is no USB keyboard |
| `keyboardLayout: Japanese` | USB keyboard keys match Japanese layout |

### 3. Confirm

```http
GET /cloud/displayConfig
```

You should get the same seven fields. Look at the monitor — it should show the new URL/size/rotation.

### 4. Typical follow-ups

**Always on (no blanking):**

```json
{ "screenTimeoutSec": 0 }
```

**Monitor hung in portrait:**

```json
{ "orientation": "portrait" }
```

**Turn the display off:**

```json
{ "enable": false }
```

All PUT fields are optional. Send only what you want to change. If you omit `resolution`, the reader uses its preferred mode. If you omit `screenTimeoutSec`, the default is **300**.

**Order:** plug HDMI → GET input/output → PUT displayConfig → GET displayConfig.

---

## The 7 `displayConfig` fields

GET and PUT use the **same** field names (`enable`, not `isEnabled`).

| Field | Type | Allowed values | Meaning |
|---|---|---|---|
| `enable` | boolean | `true` / `false` | Display on or off |
| `enableOnscreenKeyboard` | boolean | `true` / `false` | Software touch keyboard on the screen |
| `startUrl` | string, **no enum** | Any URL string | Page opened when the display is on |
| `resolution` | string | `WidthxHeight`, e.g. `1920x1080` | Pick from `supportedResolutions` |
| `orientation` | string **enum (4)** | See below | Rotation of the page |
| `screenTimeoutSec` | integer | `0`–`3600` | Idle seconds then blank. `0` = always on |
| `keyboardLayout` | string **enum (9)** | See below | Physical USB keyboard map |

Documented GET/PUT example:

```json
{
  "enable": true,
  "enableOnscreenKeyboard": true,
  "startUrl": "https://localhost/",
  "resolution": "1920x1080",
  "orientation": "landscape",
  "screenTimeoutSec": 300,
  "keyboardLayout": "Japanese"
}
```

---

## Scenario B — `startUrl`: any string, not an enum

The spec does **not** list allowed URLs. `startUrl` is only:

- type: **string**
- description: URL opened when the display is enabled
- example: `"https://localhost/"`

No `enum`, no `format: uri`, no pattern.

That is correct. An enum is for a closed list (`orientation`, `keyboardLayout`). A URL is open-ended.

| Value | Typical result |
|---|---|
| `https://localhost/` | Local reader UI on the monitor (documented case) |
| `https://warehouse.example.com/kiosk` | Works if the **reader** can reach that host |
| `http://10.233.46.10/status` | Same — reader must reach that IP |
| `"hello"` or a broken URL | PUT may succeed; the screen will not load a useful page |

`https://localhost/` means the reader opening a page **on itself**, not your laptop.

Schema: any string is valid. Practice: use a URL the FXR60 can actually open.

---

## Scenario C — `orientation` (4 values)

Only these four strings:

| Value | What you see |
|---|---|
| `landscape` | Wide screen, page upright (usual) |
| `portrait` | Monitor stood tall; page rotated 90° |
| `landscape-flipped` | Wide, page upside down (180°) |
| `portrait-flipped` | Tall, flipped the other way |

```json
{ "orientation": "landscape" }
```

Anything else (`"horizontal"`, `"90"`) is not in the spec.

Use the value that matches how the physical screen is mounted.

---

## Scenario D — `keyboardLayout` (9 values)

This is the **physical USB keyboard** language — not `startUrl`, not `orientation`, not the on-screen keyboard.

Only these 9:

1. `English-US`
2. `English-UK`
3. `German`
4. `Spanish`
5. `Italian`
6. `French`
7. `Brazilian`
8. `Swedish`
9. `Japanese`

### Story

An FXR60 is in Japan. An operator plugs in a **Japanese USB keyboard**. If the reader still thinks the keyboard is `English-US`, printed keys will not match what appears.

1. Plug in the USB keyboard.
2. `GET /cloud/inputOutputDevices` → `keyboard.status` should be `connected`.
3. PUT only the layout:

```http
PUT /cloud/displayConfig
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "keyboardLayout": "Japanese"
}
```

4. Operator types on the monitor. Keys match the keycaps.
5. GET displayConfig → `keyboardLayout` is `Japanese`. GET inputOutputDevices → `keyboard.keyboardLayout` should match when the keyboard is attached.

| Keyboard on the desk | You send | Result |
|---|---|---|
| Japanese | `Japanese` | Keys match |
| Japanese | `English-US` | Wrong characters |
| US | `English-US` | Keys match |

Wrong enum = keys look broken even though the hardware is fine.

---

## PUT vs GET (what each provides)

**PUT** applies the setting. It does **not** return `keyboardLayout` or the other fields.

```json
{}
```

**GET** `/cloud/displayConfig` is how you see what was set (all seven fields). After a PUT that sent only `{ "keyboardLayout": "Japanese" }`, GET still returns all seven; the others stay as they were.

---

## Scenario E — Change settings after plugging (checklist)

1. Plug the monitor into the FXR60.
2. `GET /cloud/inputOutputDevices` — `monitor.status` connected; note a `supportedResolutions` value.
3. `PUT /cloud/displayConfig` with only the fields you want, for example:

```json
{
  "enable": true,
  "startUrl": "https://localhost/"
}
```

or size and rotation:

```json
{
  "resolution": "1920x1080",
  "orientation": "landscape"
}
```

4. `GET /cloud/displayConfig` to confirm.

| You want | Send |
|---|---|
| Screen on / off | `"enable": true` or `false` |
| Different page | `"startUrl": "https://..."` |
| Different size | `"resolution": "1920x1080"` |
| Rotate | `"orientation": "portrait"` (or landscape / flipped) |
| Never blank | `"screenTimeoutSec": 0` |
| Blank after N seconds | `"screenTimeoutSec": 300` (max 3600) |
| Touch keyboard | `"enableOnscreenKeyboard": true` |
| USB keyboard language | `"keyboardLayout": "English-US"` |

---

## `GET /cloud/inputOutputDevices` — hardware

Four top-level parts:

| Part | What it provides |
|---|---|
| `keyboard` | USB keyboard present? Which layout? |
| `mouse` | USB mouse present? |
| `touch` | Touch screen present? |
| `monitor` | HDMI/monitor present? Plus `details` |

`status` on keyboard / mouse / touch / monitor is only `connected` or `disconnected`.

### `monitor.details[]`

| Field | Example | Meaning |
|---|---|---|
| `manufacturer` | `HPN` | Who made the screen |
| `model` | `HP Z24n G2` | Model name |
| `currentResolution` | `1920x1080` | Size in use now |
| `supportedResolutions` | `1920x1080`, `1600x900`, `1280x1024` | Sizes you may PUT as `resolution` |
| `orientation` | `landscape` | How the picture is rotated now |
| `screenActive` | `true` | `true` = awake, `false` = blanked by timeout |

Use `supportedResolutions` before PUT `resolution`. Use `screenActive` to see if the panel is asleep.

---

## Scenario F — Keyboard present vs not present

**Present:**

```json
{
  "keyboard": {
    "status": "connected",
    "keyboardLayout": "Japanese"
  }
}
```

**Not present** (documented example still may include `keyboardLayout`):

```json
{
  "keyboard": {
    "status": "disconnected",
    "keyboardLayout": "Japanese"
  }
}
```

Present or not = **`status` only**. Do not use `keyboardLayout` to decide if a keyboard is plugged in. That field can still show the stored layout when disconnected.

---

## Scenario G — Mouse present vs not present

Mouse has **only** `status`. No layout field.

**Present:**

```json
{
  "mouse": {
    "status": "connected"
  }
}
```

**Not present** (documented example):

```json
{
  "mouse": {
    "status": "disconnected"
  }
}
```

Keyboard and mouse are independent. The monitor can stay `connected` either way.

---

## Scenario H — Keyboard and mouse both not present

Both statuses are `disconnected`. This is the documented full example:

```json
{
  "keyboard": {
    "keyboardLayout": "Japanese",
    "status": "disconnected"
  },
  "monitor": {
    "details": [
      {
        "currentResolution": "1920x1080",
        "manufacturer": "HPN",
        "model": "HP Z24n G2",
        "orientation": "landscape",
        "screenActive": true,
        "supportedResolutions": [
          "1920x1080",
          "1600x900",
          "1280x1024"
        ]
      }
    ],
    "status": "connected"
  },
  "mouse": {
    "status": "disconnected"
  },
  "touch": {
    "status": "disconnected"
  }
}
```

The screen can still be on. Operators type with **`enableOnscreenKeyboard: true`** if they need a keyboard on glass.

---

## Scenario I — When is touch present?

`touch` is `connected` when the FXR60 detects a **touch screen** (touch HDMI monitor or USB HID touch).

**Present:**

```json
{
  "touch": {
    "status": "connected"
  }
}
```

**Not present** (plain HDMI monitor — documented example):

```json
{
  "touch": {
    "status": "disconnected"
  }
}
```

Do not mix these:

| | What it is |
|---|---|
| `touch.status` | **Hardware** — is a touch screen detected? |
| `enableOnscreenKeyboard` | **Software** — show a virtual keyboard on the display |

A non-touch monitor (`touch` disconnected) can still use the on-screen keyboard. A touch monitor (`touch` connected) can leave the on-screen keyboard off if they only tap buttons.

---

## FXR60 vs FXR90

| | FXR60 | FXR90 |
|---|---|---|
| Display APIs | Yes | **No** |

---

## Related example files in this repo

| File | What it is |
|---|---|
| `rest/operation_examples/cloud-displayconfig/PUT/display_config.json` | Full PUT body |
| `rest/operation_examples/cloud-displayconfig/PUT/success.json` | `{}` |
| `rest/operation_examples/cloud-displayconfig/GET/enabled.json` | Full GET body |
| `rest/operation_examples/cloud-inputoutputdevices/GET/devices.json` | Monitor connected; keyboard, mouse, touch disconnected |
