## Description

By default the reader publishes one `heartbeat` event every 60 seconds. Set `interval` to change that cadence, or set it to `0` to disable heartbeats.

This page covers interval only. The published event is still `type` `heartbeat`. Field lists for each `data` section are on the Radio Control, Reader Gateway, System, and User Apps pages. The Heartbeat page shows interval and fields together.

`interval` and `fields` are siblings in the same `heartbeat` object. You can send both in one `set_config` payload.

| Property | Value |
|---|---|
| MQTT Event | `heartbeat` |
| Pattern Name | Heartbeat Interval |
| Envelope `type` | `heartbeat` |
| Config path | `heartbeat.interval` |
| Applies To | FXR60 / FXR90 |

## Fields

| Configuration name | Published field | Description | Default |
|---|---|---|---|
| `interval` | — | How often the reader publishes a heartbeat, in seconds. `0` disables heartbeats. | `60` |
| `fields.userDefined` | Copied onto the heartbeat | Optional static key-value pairs, such as site or location, attached to every heartbeat. | Omitted |
