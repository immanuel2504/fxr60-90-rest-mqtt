# `/cloud/logs`

- **GET** — Current log configuration (`get_logs`)
- **PUT** — Set log configuration (`set_logs`)

## GET examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `GET/info_packet_off.json` | response 200 | `info_packet_off` | radio_control INFO, reader_gateway INFO, radioPacketLog off |

## PUT examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `PUT/logs.json` | request | `logs` | reader_gateway DEBUG and radioPacketLog on |
| `PUT/radioPacketLog_on.json` | request | `radioPacketLog_on` | Enable radioPacketLog |
| `PUT/success.json` | response 200 | `success` | Empty string on success |
