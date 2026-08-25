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

1. **`xml`** — raw RFID reader configuration string. Developer: at least one of `xml`, `GPIO-LED`, or `READER-GATEWAY` must be sent. Ours has no `xml`.
2. **LED action enums** (same change repeated on every GPIO-LED event):

| Field | Developer | RestDeveloperfile |
|---|---|---|
| `led` | `1` \| `2` \| `3` | `3` only (FXR60 / FXR90) |
| `postActionColor` | `GREEN` \| `RED` \| `AMBER` | same plus `OFF` |

READER-GATEWAY fields match.

---

## Trees (differing nodes)

### Developer request

```
PUT /cloud/config
├── xml                         string              [developer only]
├── GPIO-LED                    GPIOLEDConfig
│   └── <event>[] / LED action
│       ├── led                 1 | 2 | 3
│       └── postActionColor     GREEN | RED | AMBER
└── READER-GATEWAY              object
```

### RestDeveloperfile request

```
PUT /cloud/config
├── GPIO-LED                    GPIOLEDConfig
│   └── <event>[] / LED action
│       ├── led                 3
│       └── postActionColor     GREEN | RED | AMBER | OFF
└── READER-GATEWAY              object
```

The spreadsheet listed `led` / `postActionColor` once per event (CLOUD_CONNECT, TAG_READ, …). That is one schema (`ledAction.v1`) reused, not 18 independent firmware fields.

---

## Examples

### Developer — XML only

```json
{
  "xml": "<RFID …>"
}
```

### LED action (developer vs ours)

```json
{ "type": "LED", "led": 1, "color": "GREEN", "postActionColor": "AMBER" }
```

```json
{ "type": "LED", "led": 3, "color": "GREEN", "postActionColor": "OFF" }
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 1 | Added in developer | `xml` |
| 18 | Changed | `led` + `postActionColor` on 9 events (same two enums) |
| **19** | **Total** | |

---

## Docs work still to do (not applied yet)

Nothing has been merged. Add `xml` if FXR firmware accepts it. LED `3` + `OFF` are FXR-facing constraints; keep them if that is the product, or widen to 1–3 if docs must match the platform GPIO-LED schema.
