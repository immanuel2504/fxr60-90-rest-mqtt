# Example summary titles — `/cloud/apps/{appname}/pass-through`

## PUT request

### `PUT/pass_through.json`

| Field | Value |
|---|---|
| **Example name** | `pass_through` |
| **Summary title** | `Send status to mylogger` |

Path parameter: `appname` = `mylogger`

## NEED LIVE TEST

**Excel status:** NEED LIVE TEST — path appname + app response shape

1. Confirm REST body is `command` only (no `userapp` — name is in the path).
2. Confirm real app response shape (app-defined JSON).
3. App must be installed and running (`GET /cloud/apps`).
