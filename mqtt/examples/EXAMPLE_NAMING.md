# MQTT / OpenAPI example naming

Use **scenario-based** names. The example name tells the reader what the example demonstrates, not where it came from or how it was generated.

## Fields

| Field | Purpose | Shown in |
|---|---|---|
| **Example name** | Stable OpenAPI example key | Spec / internal ID |
| **Summary title** | Human-readable label | Viewer dropdown |

Define both in `mqtt/examples/<command>/SUMMARIES.md` (and the matching REST pack).

## REST ↔ MQTT parity

Shared command examples must **match across REST and MQTT**:

1. Every REST scenario that applies to an MQTT command must exist in the MQTT pack.
2. Every shared MQTT scenario must exist in the REST pack.
3. Use the **same example name** and the **same scenario filename stem** on both sides.
4. Payloads stay equivalent: REST body ↔ MQTT `payload` (MQTT wraps `command` / `command_id`).
5. MQTT-only envelopes (management events, tag/BLE data events) are excluded from this rule.

Track mappings in `mqtt/examples/REST_MQTT_EXAMPLE_MAP.md`.

## Rules

1. Name the **scenario** (behavior, mode, or outcome), not the source file path or generation method.
2. Use `snake_case` ASCII for example names. Prefer matching the JSON filename stem.
3. Prefer action or outcome words (`filter_by_prefix`, `custom_query`, `tag_selection`). Avoid weak prefixes such as `with_` or protocol tags such as `gen2_`.
4. Keep **one example per distinct payload** — no duplicates that only differ by name.
5. Summary titles are short, readable phrases that describe the scenario.
6. Common response outcomes may use shared names such as `success` or `empty` when that is the scenario.

## Examples

| Good | Why |
|---|---|
| `verbose_false` / `Configured values only` | Describes the request behavior |
| `enable_fastID` / `Enable FastID` | Describes the action |
| `SIMPLE` / `SIMPLE mode` | Describes the mode payload |
| `MQTT — set_config` | Describes the configuration path |

| Avoid | Why |
|---|---|
| `default_configured_only` next to `verbose_false` | Same scenario, two names |
| `verbose_full` next to `verbose_true` | Duplicate payload |
| `example1`, `live_capture`, `from_lab` | Source/generation, not scenario |
| REST-only or MQTT-only copies of the same scenario | Breaks REST ↔ MQTT parity |
