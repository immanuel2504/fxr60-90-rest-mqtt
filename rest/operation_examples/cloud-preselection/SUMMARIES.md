# Example summary titles — `/cloud/preSelection`

## GET responses

### `GET/preselection_disabled.json`

| Field | Value |
|---|---|
| **Example name** | `preselection_disabled` |
| **Summary title** | `Preselection disabled` |

---

## PUT request

### `PUT/enable_preselection.json`

| Field | Value |
|---|---|
| **Example name** | `enable_preselection` |
| **Summary title** | `Enable preselection` |

---

## PUT response

### `PUT/success.json`

| Field | Value |
|---|---|
| **Example name** | `success` |
| **Summary title** | `Empty string on success` |
| **HTTP status** | `200` |

GET returns string `"enabled"` / `"disabled"`; PUT sends boolean `true` / `false`. That split is the published schema.
