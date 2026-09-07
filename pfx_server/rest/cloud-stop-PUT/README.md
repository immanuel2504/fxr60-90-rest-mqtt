# `PUT /cloud/stop` tests

The four `stop` examples from `openAPISpec 11.yaml` (IoT Connector REST API
v3.0.0), each with its request body, verbatim response and verification notes.

**The report covering these tests is in the sibling folder**, because it covers
`start` and `stop` together — they are only meaningful as a pair, and every stop
test was verified by starting something first:

> [`../cloud-start-PUT/START_STOP_TEST_REPORT.md`](../cloud-start-PUT/START_STOP_TEST_REPORT.md)

| Folder | Example | Result |
|---|---|---|
| `01-stop_RFID_default-empty-body-SUCCESS/` | `stop_RFID_default` `{}` | ✅ `radio: active → inactive` |
| `02-stop_RFID_explicit-SUCCESS/` | `stop_RFID_explicit` | ✅ `radio: active → inactive` |
| `03-stop_BLE_only-SUCCESS/` | `stop_BLE_only` | ✅ `ble: running → stopped` |
| `04-stop_BLE_and_RFID-SUCCESS/` | `stop_BLE_and_RFID` | ✅ both stopped |

All four work. One behaviour worth knowing: **`stop` is not idempotent** —
stopping something that is not running returns
`422 {"code":1,"message":"No scan is currently active"}` rather than a no-op.
See test 03.
