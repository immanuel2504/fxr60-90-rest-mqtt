# `/cloud/logs/radioPacketLog`

- **GET** - Retrieve radio packet log
- **DELETE** - Purge radio packet log (no example pack yet)

## Reviewed GET

| File | Example name | Summary |
|---|---|---|
| `GET/download.json` | `download` | Radio packet log archive |

## NEED LIVE TEST

Enable packet logging with `PUT /cloud/logs`, then confirm GET returns `binary` + `filename`.
