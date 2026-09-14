## Description

The `firmwareUpdateProgress` event is published on the management channel while an OS update is running.

The reader publishes progress events until the update completes or fails.

This event includes:

- The current update status.
- Image download progress.
- Overall update progress.
- Per-component update progress for OS, root file system, applications, radio firmware, and platform.

This event is useful when the backend must track the progress of an OS update after the update is started.

## Event Details

| Property | Value |
|---|---|
| MQTT event | `firmwareUpdateProgress` |
| Envelope `type` | `firmwareUpdateProgress` |
| Configuration path | Not configurable in `managementEventConfig` |
| Trigger | `set_os` |
| Delivery destination | `endpointConfig.management.event` |
| Communication type | Device to Cloud |
| Applies to | FXR60 / FXR90 |

## How Firmware Progress Works

This event does not have a `managementEventConfig` enable or disable flag.

Set the management-event destination on the common management-event configuration page. After the destination is configured, start the OS update by using `set_os`.

When the update starts, the reader automatically publishes `firmwareUpdateProgress` events on the management-event destination until the update completes or fails.

## Fields

| Field | Description |
|---|---|
| `status` | Current update status. Values include `started`, `failed`, `rebooting`, `downloading-<image>`, `erasing-<image>`, and `writing-<image>`. |
| `imageDownloadProgress` | Image download progress, from `0` to `100`. |
| `overallUpdateProgress` | Overall update progress, from `0` to `100`. |
| `updateProgressDetails` | Per-component update progress. This includes `os`, `rootFileSystem`, `applications`, `radioFirmware`, and `platform`. If the update fails, this field can contain a failure reason string. |

## Response Schema

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `firmwareUpdateProgress`. |
| `timestamp` | string | Event timestamp. |
| `component` | string | Component that published the event. |
| `eventNum` | number | Management event sequence number. |
| `data.status` | string | Current firmware update status. |
| `data.imageDownloadProgress` | number | Image download progress percentage. |
| `data.overallUpdateProgress` | number | Overall update progress percentage. |
| `data.updateProgressDetails` | object or string | Per-component update progress, or a failure reason string when the update fails. |
