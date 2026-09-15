# `/cloud/mode`

- **GET** - Retrieves the operating mode (`getMode`)
- **PUT** - Updates the reader's operating mode (`setMode`)

GET request examples are `verbose_false` and `verbose_true`. GET responses include those same names plus mode samples (`SIMPLE`, `INVENTORY`, `PORTAL`, `CONVEYOR`). `verbose_false` shows a CUSTOM configured-values response.

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
| `GET/CONVEYOR.json` | `CONVEYOR` | Response: CONVEYOR mode |

## PUT examples (12)

| File | Example name | Summary |
|---|---|---|
| `PUT/simple_baseline.json` | `simple_baseline` | SIMPLE mode baseline |
| `PUT/inventory_report_interval.json` | `inventory_report_interval` | INVENTORY mode with report interval |
| `PUT/portal_gpi_trigger.json` | `portal_gpi_trigger` | PORTAL mode with GPI start trigger |
| `PUT/conveyor_baseline.json` | `conveyor_baseline` | CONVEYOR mode baseline |
| `PUT/filter_by_prefix.json` | `filter_by_prefix` | Filter tags by prefix |
| `PUT/custom_comprehensive.json` | `custom_comprehensive` | CUSTOM mode with query, selects, and tag metadata |
| `PUT/access_operations.json` | `access_operations` | Run access operations |
| `PUT/write_access_password.json` | `write_access_password` | Assign an access password (WRITE to RESERVED bank) |
| `PUT/report_filter.json` | `report_filter` | Report filter |
| `PUT/radio_stop_duration.json` | `radio_stop_duration` | Radio stop duration |

## Notes

- No `rssiFilter` on PUT examples (optional schema field)
- No legacy `component` / `linkProfile` / `payload`
- Do not combine `accesses` with `reportFilter`
- `radioStartConditions` / `radioStopConditions` are not for PORTAL
- SIMPLE mode baseline does not include `tagMetaData`
- Prefix `filter` should not be combined with `query` / `selects`
- Tag metadata location is `READERLOCATION`
- Access word length is `wordCount` (not `wordCounter`)
- `transmitPower` is 0–30 dBm
