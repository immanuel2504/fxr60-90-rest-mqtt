# `set_displayConfig`

REST: `PUT /cloud/displayConfig` → `cloud-displayconfig/`

FXR60 only.

Stable `command_id`: `req-set-displayConfig`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/landscape_japanese.json` | request | `landscape_japanese` | `cloud-displayconfig/PUT/landscape_japanese.json` | Landscape, Japanese, 1920x1080 |
| `request/portrait_german.json` | request | `portrait_german` | `cloud-displayconfig/PUT/portrait_german.json` | Portrait, German, 1280x720 |
| `request/flipped_orientation.json` | request | `flipped_orientation` | `cloud-displayconfig/PUT/flipped_orientation.json` | Enable and flip orientation |
| `response/success.json` | response | `success` | `cloud-displayconfig/PUT/success.json` | Command succeeded |
