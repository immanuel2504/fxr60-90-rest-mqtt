# Example summary titles — `/cloud/logs`

## PUT request

### `PUT/logs.json`

| Field | Value |
|---|---|
| **Example name** | `logs` |
| **Summary title** | `DEBUG radio_control and cloud_agent` |

---

## PUT response

### `PUT/success.json`

| Field | Value |
|---|---|
| **Example name** | `success` |
| **Summary title** | `Empty string on success` |
| **HTTP status** | `200` |

## NEED LIVE TEST

Confirm on a real reader:

1. Request body shape (`components` + `radioPacketLog`) is accepted.
2. Success response is empty string `""`.
3. GET `/cloud/logs` afterward reflects the new levels.
