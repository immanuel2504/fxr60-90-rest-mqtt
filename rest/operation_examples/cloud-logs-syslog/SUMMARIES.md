# Example summary titles — `/cloud/logs/syslog`

## GET responses

### `GET/download.json`

| Field | Value |
|---|---|
| **Example name** | `download` |
| **Summary title** | `Syslog archive` |

## DELETE response

### `DELETE/success.json`

| Field | Value |
|---|---|
| **Example name** | `success` |
| **Summary title** | `Empty string on success` |
| **HTTP status** | `200` |

## NEED LIVE TEST

Confirm on a real reader that the GET response includes non-empty `binary` (Base64) and a `filename`.

Confirm the DELETE (purge) response body. The spec declares `200 OK` with no content, so the
empty-string example above follows the convention used by the other DELETE packs rather than a
verified reader response.
