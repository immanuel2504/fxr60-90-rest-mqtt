# Example summary titles — `/cloud/preSelection`

## GET responses

### `GET/disabled.json`

| Field | Value |
|---|---|
| **Example name** | `disabled` |
| **Summary title** | `preSelection disabled` |

---

## PUT request

### `PUT/enable.json`

| Field | Value |
|---|---|
| **Example name** | `enable` |
| **Summary title** | `Enable preSelection` |

---

## PUT response

### `PUT/success.json`

| Field | Value |
|---|---|
| **Example name** | `success` |
| **Summary title** | `Empty string on success` |
| **HTTP status** | `200` |

GET returns string `"enabled"` / `"disabled"`; PUT sends boolean `true` / `false`. That split is the published schema.
