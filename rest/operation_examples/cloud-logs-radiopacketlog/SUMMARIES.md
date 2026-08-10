# Example summary titles — `/cloud/logs/radioPacketLog`

## GET responses

### `GET/download.json`

| Field | Value |
|---|---|
| **Example name** | `download` |
| **Summary title** | `Radio packet log archive` |

## NEED LIVE TEST

Confirm on a real reader:

1. Enable `radioPacketLog` via `PUT /cloud/logs` first.
2. Response includes non-empty `binary` (Base64) and a `filename`.
