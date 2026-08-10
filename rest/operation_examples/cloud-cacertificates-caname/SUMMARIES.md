# Example summary titles — `/cloud/caCertificates/{caname}`

## DELETE response

### `DELETE/success.json`

| Field | Value |
|---|---|
| **Example name** | `success` |
| **Summary title** | `Empty string on success` |
| **HTTP status** | `200` |

Path parameter example: `caname` = `AmazonRootCA1`

## NEED LIVE TEST

Confirm on a real reader:

1. **DELETE** — name comes from path `{caname}` only (no request body).
2. **PUT** — REST uses path `{caname}` + body `{ "content": "..." }`; body `name` is MQTT-style and should be ignored (or rejected) on local REST.
