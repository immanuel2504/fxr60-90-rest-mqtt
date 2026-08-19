# Example summary titles — `/cloud/logs/radioPacketLog`

## GET responses

### `GET/download.json`

| Field | Value |
|---|---|
| **Example name** | `download` |
| **Summary title** | `Radio packet log archive` |

## DELETE response

### `DELETE/success.json`

| Field | Value |
|---|---|
| **Example name** | `success` |
| **Summary title** | `Empty string on success` |
| **HTTP status** | `200` |

## NEED LIVE TEST

Confirm on a real reader:

1. Enable `radioPacketLog` via `PUT /cloud/logs` first.
2. GET response includes non-empty `binary` (Base64) and a `filename`.
3. DELETE (purge) response body. The spec declares `200 OK` with no content, so the empty-string
   example above follows the convention used by the other DELETE packs rather than a verified
   reader response.
