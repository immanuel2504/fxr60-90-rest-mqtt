# Example summary titles — `/cloud/mode`

GET responses replaced 2026-08-12 with a live verbose/non-verbose pair captured from a reader in
INVENTORY mode. The previous four (`inline`, `SIMPLE`, `INVENTORY`, `PORTAL`) were removed: they
returned `antennaStopCondition` and `query` as arrays, which the live captures contradict, and
`inline` combined `reportFilter` with `modeSpecificSettings.interval`.

PUT refreshed from `FXR-Series/examples/mode_testing/PUT_cloud_mode`.

### `GET/verbose_false.json`

| Field | Value |
|---|---|
| **Example name** | `verbose_false` |
| **Summary title** | `Response: verbose false — configured values only` |

### `GET/verbose_true.json`

| Field | Value |
|---|---|
| **Example name** | `verbose_true` |
| **Summary title** | `Response: verbose true — full configuration including defaults` |

### `GET/default_configured_only.json`

| Field | Value |
|---|---|
| **Example name** | `default_configured_only` |
| **Summary title** | `Request: configured values only (default)` |

### `GET/verbose_full.json`

| Field | Value |
|---|---|
| **Example name** | `verbose_full` |
| **Summary title** | `Request: entire configuration including defaults` |

### `PUT/simple_basic.json`

| Field | Value |
|---|---|
| **Example name** | `simple_basic` |
| **Summary title** | `SIMPLE mode baseline` |

### `PUT/inventory_with_interval.json`

| Field | Value |
|---|---|
| **Example name** | `inventory_with_interval` |
| **Summary title** | `INVENTORY mode with report interval` |

### `PUT/portal_gpi_trigger.json`

| Field | Value |
|---|---|
| **Example name** | `portal_gpi_trigger` |
| **Summary title** | `PORTAL mode with GPI start trigger` |

### `PUT/conveyor_basic.json`

| Field | Value |
|---|---|
| **Example name** | `conveyor_basic` |
| **Summary title** | `CONVEYOR mode baseline` |

### `PUT/with_filter_prefix.json`

| Field | Value |
|---|---|
| **Example name** | `with_filter_prefix` |
| **Summary title** | `CUSTOM mode with prefix EPC filter` |

### `PUT/with_query.json`

| Field | Value |
|---|---|
| **Example name** | `with_query` |
| **Summary title** | `CUSTOM mode with Gen2 query` |

### `PUT/with_selects.json`

| Field | Value |
|---|---|
| **Example name** | `with_selects` |
| **Summary title** | `CUSTOM mode with Gen2 selects` |

### `PUT/with_accesses.json`

| Field | Value |
|---|---|
| **Example name** | `with_accesses` |
| **Summary title** | `CUSTOM mode with READ TID access` |

### `PUT/with_report_filter.json`

| Field | Value |
|---|---|
| **Example name** | `with_report_filter` |
| **Summary title** | `CUSTOM mode with report filter` |

### `PUT/with_tag_metadata.json`

| Field | Value |
|---|---|
| **Example name** | `with_tag_metadata` |
| **Summary title** | `CUSTOM mode with tag metadata fields` |

### `PUT/with_radio_stop.json`

| Field | Value |
|---|---|
| **Example name** | `with_radio_stop` |
| **Summary title** | `CUSTOM mode with radio stop conditions` |
