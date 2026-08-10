# Example summary titles — `/cloud/certificates`

## GET responses

### `GET/installed.json`

| Field | Value |
|---|---|
| **Example name** | `installed` |
| **Summary title** | `Server and client certificates` |

## NEED LIVE TEST

Confirm on a real reader that `GET /cloud/certificates` returns this shape:

- `name`, `type` (`server` / `client` / `app`)
- `serial`, `installTime`, `issuerName`, `subjectName`
- `validityStart`, `validityEnd`, `publickey`
