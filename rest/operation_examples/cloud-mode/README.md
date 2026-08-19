# `/cloud/mode`

- **GET** - Retrieves the operating mode (`getMode`) — review later
- **PUT** - Updates the reader's operating mode (`setMode`)

PUT examples sourced from `FXR-Series/examples/mode_testing/PUT_cloud_mode` (lab lean set).

## PUT examples (11)

| File | Example name | Summary |
|---|---|---|
| `PUT/simple_basic.json` | `simple_basic` | SIMPLE mode baseline |
| `PUT/inventory_with_interval.json` | `inventory_with_interval` | INVENTORY mode with report interval |
| `PUT/portal_gpi_trigger.json` | `portal_gpi_trigger` | PORTAL mode with GPI start trigger |
| `PUT/conveyor_basic.json` | `conveyor_basic` | CONVEYOR mode baseline |
| `PUT/with_filter_prefix.json` | `with_filter_prefix` | CUSTOM mode with prefix EPC filter |
| `PUT/with_query.json` | `with_query` | CUSTOM mode with Gen2 query |
| `PUT/with_selects.json` | `with_selects` | CUSTOM mode with Gen2 selects |
| `PUT/with_accesses.json` | `with_accesses` | CUSTOM mode with READ TID access |
| `PUT/with_report_filter.json` | `with_report_filter` | CUSTOM mode with report filter |
| `PUT/with_tag_metadata.json` | `with_tag_metadata` | CUSTOM mode with tag metadata fields |
| `PUT/with_radio_stop.json` | `with_radio_stop` | CUSTOM mode with radio stop conditions |

## Notes

- No `rssiFilter` (FX9600 only)
- No legacy `component` / `linkProfile` / `payload`
- Do not combine `accesses` with `reportFilter`
- `radioStartConditions` / `radioStopConditions` are not for PORTAL
- SIMPLE mode baseline does not include `radioStartConditions` / `radioStopConditions`
- Prefix `filter` should not be combined with `query` / `selects`

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X PUT "https://$READER/cloud/mode" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/simple_basic.json
```
