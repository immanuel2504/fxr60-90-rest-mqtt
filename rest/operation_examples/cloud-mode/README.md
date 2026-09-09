# `/cloud/mode`

- **GET** - Retrieves the operating mode (`getMode`)
- **PUT** - Updates the reader's operating mode (`setMode`)

GET request examples are `verbose_false` and `verbose_true`. GET responses include those same names plus one sample per mode (`SIMPLE`, `INVENTORY`, `PORTAL`, `CONVEYOR`, `CUSTOM`). `verbose_true` / `INVENTORY` share the verbose capture; `verbose_false` / `CUSTOM` share the configured-only capture.

PUT examples sourced from `FXR-Series/examples/mode_testing/PUT_cloud_mode` (lab lean set), corrected to match `operatingMode.v1` and live firmware.

## GET examples

| File | Example name | Summary |
|---|---|---|
| `GET/verbose_false_request.json` | `verbose_false` | Request: verbose false — configured values only |
| `GET/verbose_true_request.json` | `verbose_true` | Request: verbose true — full configuration including defaults |
| `GET/verbose_false.json` | `verbose_false` | Response: verbose false — CUSTOM configured values only |
| `GET/verbose_true.json` | `verbose_true` | Response: verbose true — INVENTORY full configuration |
| `GET/SIMPLE.json` | `SIMPLE` | Response: SIMPLE mode |
| `GET/INVENTORY.json` | `INVENTORY` | Response: INVENTORY mode (verbose true) |
| `GET/PORTAL.json` | `PORTAL` | Response: PORTAL mode |
| `GET/CONVEYOR.json` | `CONVEYOR` | Response: CONVEYOR mode after live PUT |
| `GET/CUSTOM.json` | `CUSTOM` | Response: CUSTOM mode (verbose false) |

## PUT examples (11)

| File | Example name | Summary |
|---|---|---|
| `PUT/SIMPLE.json` | `SIMPLE` | SIMPLE mode baseline |
| `PUT/INVENTORY.json` | `INVENTORY` | INVENTORY mode with report interval |
| `PUT/PORTAL.json` | `PORTAL` | PORTAL mode with GPI start trigger |
| `PUT/CONVEYOR.json` | `CONVEYOR` | CONVEYOR mode baseline |
| `PUT/CUSTOM_filter.json` | `CUSTOM_filter` | CUSTOM filter |
| `PUT/CUSTOM_query.json` | `CUSTOM_query` | CUSTOM query |
| `PUT/CUSTOM_selects.json` | `CUSTOM_selects` | CUSTOM selects |
| `PUT/CUSTOM_accesses.json` | `CUSTOM_accesses` | CUSTOM accesses |
| `PUT/CUSTOM_report_filter.json` | `CUSTOM_report_filter` | CUSTOM report filter |
| `PUT/CUSTOM_metadata.json` | `CUSTOM_metadata` | CUSTOM metadata |
| `PUT/CUSTOM_radio_stop.json` | `CUSTOM_radio_stop` | CUSTOM radio stop |

## Notes

- No `rssiFilter` on PUT examples (optional schema field; not used in the lab set)
- No legacy `component` / `linkProfile` / `payload`
- Do not combine `accesses` with `reportFilter`
- `radioStartConditions` / `radioStopConditions` are not for PORTAL
- SIMPLE mode baseline does not include `tagMetaData`
- Prefix `filter` should not be combined with `query` / `selects`
- Tag metadata location is `READERLOCATION` (not `READER_LOCATION`)
- Access word length is `wordCount` (not `wordCounter`)
- `transmitPower` is 0–30 dBm
