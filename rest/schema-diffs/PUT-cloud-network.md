# PUT `/cloud/network` — schema difference

**Date:** 25 August 2026  
**operationId:** `updateNetwork`  
**MQTT:** `set_network`

Compared:

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec (source of truth for firmware) |
| `rest/RestDeveloperfile.yaml` | Current docs source |

The **path is the same**. Ethernet 802.1X **JSON key casing**, where **enable** flags live, and Wi-Fi inner-auth spelling disagree.

---

## What is happening

Three client-visible disagreements:

1. **802.1X object key** on `eth0.security`: developer `802_1xEAP` vs ours `802_1XEAP`.
2. **Enable flags**: developer puts Wi-Fi enable on `mlan0.accesspoint.enable`. Ours puts `mlan0.enable`, plus extra `eth0.security.enable` and `mlan0.accesspoint.security.enable`.
3. **Inner authentication spelling**: developer `MSCHAPv2` vs ours `MSCHAPV2` (and ours also allows `""` for outer TLS).

Sending the RestDeveloperfile key `802_1XEAP` will not match the developer schema.

---

## Difference table

| JSON field | Status | Developer | RestDeveloperfile |
|---|---|---|---|
| `eth0.security.802_1xEAP` | Renamed | object | — (ours uses `802_1XEAP`) |
| `eth0.security.802_1XEAP` | Ours only | — | object |
| `eth0.security.enable` | Ours only | — | boolean (802.1X on/off, separate from port enable) |
| `eth0.enable` | Same idea | boolean (port on/off) | boolean (port on/off) |
| `mlan0.accesspoint.enable` | Developer only | boolean (Wi-Fi station on/off) | — |
| `mlan0.enable` | Ours only | — | boolean (Wi-Fi station on/off) |
| `mlan0.accesspoint.security.enable` | Ours only | — | boolean |
| `…WPA2Enterprise.innerAuthentication` | Changed | `TLS` \| `MSCHAPv2` | `TLS` \| `MSCHAPV2` \| `""` |
| `…WPA3Enterprise.innerAuthentication` | Changed | `TLS` \| `MSCHAPv2` | `TLS` \| `MSCHAPV2` \| `""` |

---

## Trees (differing nodes)

### Developer

```
eth0
├── enable                      boolean             ethernet port on/off
└── security
    └── 802_1xEAP               object              [lowercase x]
        ├── authentication      TLS | TTLS | PEAP
        └── innerAuthentication TLS | MSCHAPv2

mlan0
└── accesspoint
    ├── enable                  boolean             Wi-Fi station on/off  [developer location]
    └── security
        ├── WPA2Enterprise.innerAuthentication   TLS | MSCHAPv2
        └── WPA3Enterprise.innerAuthentication   TLS | MSCHAPv2
```

### RestDeveloperfile

```
eth0
├── enable                      boolean             ethernet port on/off
└── security
    ├── enable                  boolean             802.1X on/off  [ours only]
    └── 802_1XEAP               object              [uppercase X]
        └── innerAuthentication TLS | MSCHAPV2 | ""

mlan0
├── enable                      boolean             Wi-Fi station on/off  [ours location]
└── accesspoint
    └── security
        ├── enable              boolean             [ours only]
        └── WPA2/WPA3Enterprise.innerAuthentication  TLS | MSCHAPV2 | ""
```

---

## Examples

### Developer — ethernet 802.1X

```json
{
  "eth0": {
    "enable": true,
    "security": {
      "802_1xEAP": {
        "authentication": "PEAP",
        "innerAuthentication": "MSCHAPv2",
        "username": "john.doe",
        "password": "secret"
      }
    }
  }
}
```

### RestDeveloperfile — same intent

```json
{
  "eth0": {
    "enable": true,
    "security": {
      "enable": true,
      "802_1XEAP": {
        "authentication": "PEAP",
        "innerAuthentication": "MSCHAPV2",
        "username": "john.doe",
        "password": "secret"
      }
    }
  }
}
```

---

## Spreadsheet row

| Count | Kind | Fields |
|---:|---|---|
| 1 | Added in developer | `mlan0.accesspoint.enable` |
| 3 | Only in RestDeveloperfile | `eth0.security.enable`, `mlan0.enable`, `mlan0.accesspoint.security.enable` |
| 2 | Changed | WPA2/WPA3 `innerAuthentication` |
| 1 | Renamed | `802_1XEAP` → `802_1xEAP` |
| **7** | **Total** | |

---

## Docs work still to do (not applied yet)

Nothing has been merged into `RestDeveloperfile.yaml`. Align with the developer column when firmware is the source of truth, then update `rest/operation_descriptions/`, `rest/operation_examples/`, MQTT `openapi_md.json`, and rebuild.
