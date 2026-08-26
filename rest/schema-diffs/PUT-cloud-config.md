# PUT `/cloud/config` — schema difference

**Date:** 25 August 2026  
**operationId:** `setConfigMqtt`  
**MQTT:** `set_config`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path is the same**. Developer adds request field `xml`. GPIO-LED **LED number** and **postActionColor** enums differ in `ledAction.v1` (shared by every event: TAG_READ, RADIO_START, GPI_*, CLOUD_*).

---

## What is happening

1. **`xml`** — **9a Final.** Optional Cloud Connect RFID XML string. At least one of `xml`, `GPIO-LED`, or `READER-GATEWAY`.
2. **LED action enums** (same change repeated on every GPIO-LED event):

| Field | Developer | RestDeveloperfile |
|---|---|---|
| `led` | `1` \| `2` \| `3` | **Same (9b Final).** Device: 1, 2, and 3 all work. |
| `postActionColor` | `GREEN` \| `RED` \| `AMBER` | **Same (9c Final).** Device rejects `OFF`. |

READER-GATEWAY fields match.

---

## Trees (differing nodes)

### Developer request

```
PUT /cloud/config
├── xml                         string
├── GPIO-LED                    GPIOLEDConfig
│   └── <event>[] / LED action
│       ├── led                 1 | 2 | 3
│       └── postActionColor     GREEN | RED | AMBER
└── READER-GATEWAY              object
```

### RestDeveloperfile request

```
PUT /cloud/config
├── xml                         string              Cloud Connect RFID profile (9a Final)
├── GPIO-LED                    GPIOLEDConfig
│   └── <event>[] / LED action
│       ├── led                 1 | 2 | 3           (9b Final)
│       └── postActionColor     GREEN | RED | AMBER   (9c Final; OFF rejected)
└── READER-GATEWAY              object
```

The spreadsheet listed `led` / `postActionColor` once per event (CLOUD_CONNECT, TAG_READ, …). That is one schema (`ledAction.v1`) reused, not 18 independent firmware fields.

---

## Examples

### XML only (9a)

```json
{
  "xml": "<RFID><!-- Cloud Connect operational profile --></RFID>"
}
```

### LED action — 9b Final (`1` \| `2` \| `3`); 9c Final (`OFF` rejected)

```json
{ "type": "LED", "led": 1, "color": "GREEN", "postActionColor": "AMBER" }
```

```json
{ "type": "LED", "led": 3, "color": "GREEN", "postActionColor": "GREEN" }
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 1 | Added in developer | `xml` |
| 18 | Changed | `led` + `postActionColor` on 9 events (same two enums) |
| **19** | **Total** | |

---

## Status

**9a Final.** Optional PUT / MQTT `xml` is in the docs.  
**9b Final.** `led` 1, 2, or 3. Device: all three work.  
**9c Final.** Dropped `OFF`. Device rejects it. Ask why.
