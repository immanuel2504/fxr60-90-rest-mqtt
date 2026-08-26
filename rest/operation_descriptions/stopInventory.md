## 1. Description

The `PUT /cloud/stop` REST endpoint stops RFID inventory, BLE scanning, or both.

By default, if the request body is empty or `scanType` is not provided, the reader stops RFID inventory only.

`scanType` can be an **array** (global stop on every data endpoint) or an **object** (targeted stop per data endpoint).

Use this endpoint to:

- Stop an active RFID inventory cycle
- Stop BLE scanning without stopping RFID
- Stop both BLE and RFID before changing configuration
- Return the reader to an idle state before changing mode or BLE settings

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `stop` |
| Pattern Name | Scan Control - Stop |
| REST Endpoint | `PUT /cloud/stop` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Supported Operations | Stop RFID inventory, BLE scan, or both |
| Firmware Requirement | BLE requires reader build **4.0.11** or later. On earlier builds the `scanType` field is not available. |

## 3. Stop Behavior

`scanType` is either:

- An **array** — **global stop**. The same scan types are stopped on **every** data endpoint.
- An **object** — **targeted stop**. Keys are data endpoint names; values are the scan types to stop on that endpoint.

**Global stop** (array). Example — BLE on all endpoints:

```json
{ "scanType": ["ble"] }
```

| Request body | Result |
|---|---|
| `{}` | Stops RFID inventory only. This is the default behavior. |
| `{ "scanType": ["rfid"] }` | Stops RFID inventory on every data endpoint. BLE scanning continues if active. |
| `{ "scanType": ["ble"] }` | Stops BLE scanning on every data endpoint. RFID inventory continues if active. |
| `{ "scanType": ["ble", "rfid"] }` | Stops both on every data endpoint. |

**Targeted stop** (object with data-endpoint fields):

```json
{ "scanType": { "dataEndpoint1": ["ble", "rfid"], "dataEndpoint2": ["rfid"] } }
```

> Firmware requirement: BLE scanning — and with it the `scanType` field — is available from reader build **4.0.11** onward. On builds older than 4.0.11, `scanType` is not supported: send an empty body `{}`, which stops RFID inventory. Check the installed build with `GET /cloud/version` (`readerApplication`).

## 4. Before You Begin

Stopping a scan type that is already idle may still succeed or may return failure depending on the reader state. If you need to know the current state first, check `GET /cloud/status`.

| What You Need | Details |
|---|---|
| Current activity | Optional. Check `GET /cloud/status` if you need to confirm RFID or BLE activity before stopping. |
| Target scan type | Choose `rfid`, `ble`, or both in `scanType`. Omit `scanType` only when you want the default RFID stop behavior. |
