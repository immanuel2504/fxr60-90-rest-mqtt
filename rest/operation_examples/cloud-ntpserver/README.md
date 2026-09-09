# `/cloud/ntpServer`

- **GET** — Current NTP server (`get_ntpServer`)
- **PUT** — Set NTP server (`set_ntpServer`)

## GET examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `GET/pool_ntp_org.json` | response 200 | `pool_ntp_org` | `server` pool.ntp.org |

## PUT examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `PUT/time1_time2.json` | request | `time1_time2` | `server` and `server2` |
| `PUT/server1.json` | request | `server1` | Legacy `server1` |
| `PUT/time_google.json` | request | `time_google` | `server` only |
| `PUT/success.json` | response 200 | `success` | Empty string on success |
