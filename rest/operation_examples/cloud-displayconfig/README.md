# `/cloud/displayConfig`

- **GET** — Current display configuration (`get_displayConfig`). FXR60 only.
- **PUT** — Update display configuration (`set_displayConfig`).

## GET examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `GET/enabled.json` | response 200 | `enabled` | Display enabled at 1920x1080 |

## PUT examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `PUT/landscape_japanese.json` | request | `landscape_japanese` | Landscape, Japanese, 1920x1080 |
| `PUT/portrait_german.json` | request | `portrait_german` | Portrait, German, 1280x720 |
| `PUT/flipped_orientation.json` | request | `flipped_orientation` | Enable and flip orientation |
| `PUT/success.json` | response 200 | `success` | Empty object on success |
