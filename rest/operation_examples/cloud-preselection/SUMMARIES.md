# Example summary titles — `/cloud/preSelection`

## GET responses

### `GET/pre_selection.json`

| Field | Value |
|---|---|
| **Example name** | `pre_selection` |
| **Summary title** | `Current preSelection state` |

---

## PUT request

### `PUT/pre_selection.json`

| Field | Value |
|---|---|
| **Example name** | `pre_selection` |
| **Summary title** | `Enable preSelection` |

---

## PUT response

### `PUT/success.json`

| Field | Value |
|---|---|
| **Example name** | `success` |
| **Summary title** | `Empty string on success` |
| **HTTP status** | `200` |

## NEED LIVE TEST / discuss with developer

GET returns string `"enabled"` / `"disabled"`; PUT sends boolean `true` / `false`. Confirm contract on a reader.
