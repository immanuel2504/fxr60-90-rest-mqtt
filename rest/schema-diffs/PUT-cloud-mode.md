# PUT `/cloud/mode` — schema difference

**Date:** 25 August 2026  
**operationId:** `setMode`  
**MQTT:** `set_mode`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path and operatingMode object are the same**. Nested **port** enums are FXR docs polish, not a new field.

---

## What is happening

No new request keys. Ours constrains GPI / antenna-stop **port** to `1`–`4`. Developer leaves those as unconstrained integers.

Same nested fields as [GET `/cloud/mode`](GET-cloud-mode.md).

`tagMetaData`: our docs include **`READER_LOCATION`**; developer spec does not. Same questions as GET `/cloud/mode` — see [DISCUSS-AND-FINALIZE.md](DISCUSS-AND-FINALIZE.md).

---

## Difference table

| JSON field | Developer | RestDeveloperfile |
|---|---|---|
| `antennaStopCondition` port | integer | enum `1` \| `2` \| `3` \| `4` |
| `radioStartConditions.gpis[].port` | integer | enum `1` \| `2` \| `3` \| `4` |
| `radioStopConditions.gpis[].port` | integer | enum `1` \| `2` \| `3` \| `4` |

---

## Tree (differing nodes)

```
operatingMode
├── antennaStopCondition….port     integer   vs   1|2|3|4
├── radioStartConditions.gpis.port integer   vs   1|2|3|4
└── radioStopConditions.gpis.port  integer   vs   1|2|3|4
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 4 | Changed | nested `port` (+ tagMetaData walk) |
| **4** | **Total** | (walk counted 5) |

---

## Docs work

**Keep docs.** Ports 1–4 and `READER_LOCATION` stay until the developer replies. Same questions as GET `/cloud/mode` — copy-paste in [DISCUSS-AND-FINALIZE.md](DISCUSS-AND-FINALIZE.md).
