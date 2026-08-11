# `set_mode`

REST: `PUT /cloud/mode` → `cloud-mode/`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/simple_basic.json` | request | `simple_basic` | `cloud-mode/PUT/simple_basic.json` | SIMPLE mode baseline |
| `request/inventory_with_interval.json` | request | `inventory_with_interval` | `cloud-mode/PUT/inventory_with_interval.json` | INVENTORY mode with report interval |
| `request/portal_gpi_trigger.json` | request | `portal_gpi_trigger` | `cloud-mode/PUT/portal_gpi_trigger.json` | PORTAL mode with GPI start trigger |
| `request/conveyor_basic.json` | request | `conveyor_basic` | `cloud-mode/PUT/conveyor_basic.json` | CONVEYOR mode baseline |
| `request/with_filter_prefix.json` | request | `with_filter_prefix` | `cloud-mode/PUT/with_filter_prefix.json` | CUSTOM mode with prefix EPC filter |
| `request/with_query.json` | request | `with_query` | `cloud-mode/PUT/with_query.json` | CUSTOM mode with Gen2 query |
| `request/with_selects.json` | request | `with_selects` | `cloud-mode/PUT/with_selects.json` | CUSTOM mode with Gen2 selects |
| `request/with_accesses.json` | request | `with_accesses` | `cloud-mode/PUT/with_accesses.json` | CUSTOM mode with READ TID access |
| `request/with_report_filter.json` | request | `with_report_filter` | `cloud-mode/PUT/with_report_filter.json` | CUSTOM mode with report filter |
| `request/with_tag_metadata.json` | request | `with_tag_metadata` | `cloud-mode/PUT/with_tag_metadata.json` | CUSTOM mode with tag metadata fields |
| `request/with_radio_stop.json` | request | `with_radio_stop` | `cloud-mode/PUT/with_radio_stop.json` | CUSTOM mode with radio stop conditions |
| `response/success.json` | response | `success` | `—` | Command succeeded |
