# GET `/cloud/status` — schema difference

**Date:** 25 August 2026  
**operationId:** `getStatus`  
**MQTT:** `get_status`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path is the same**. Three response-shape differences: antennas map, Gen2X `feature` enum, `powerSource` enum.

---

## What is happening

| Field | Developer | RestDeveloperfile |
|---|---|---|
| `antennas` | named properties `"1"` … `"8"` | `additionalProperties` (only ports present on this reader) |
| `impinjGen2X.feature` | `fastId` \| `tagFocus` \| `tagProtect` \| `tagQuieting` | same plus `none` |
| `powerSource` | unconstrained string | `PWR_BRICK` \| `POE` \| `POE+` |

Ours documents FXR power sources and a `none` Gen2X idle value. Developer leaves `powerSource` open (example still uses `PWR_BRICK`).

---

## Trees

### Developer 200 (differing nodes)

```
antennas                        object              properties 1–8
impinjGen2X.feature             fastId | tagFocus | tagProtect | tagQuieting
powerSource                     string
```

### RestDeveloperfile 200

```
antennas                        object              additionalProperties connected|disconnected
impinjGen2X.feature             none | fastId | tagFocus | tagProtect | tagQuieting
powerSource                     PWR_BRICK | POE | POE+
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 3 | Changed | `antennas`, `impinjGen2X.feature`, `powerSource` |
| **3** | **Total** | |

---

## Docs work

**Keep docs** until the developer replies. Copy-paste: [DISCUSS-AND-FINALIZE.md](DISCUSS-AND-FINALIZE.md).
