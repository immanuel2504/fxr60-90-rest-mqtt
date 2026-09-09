# `/cloud/preSelection`

- **GET** - Current preSelection state (`enabled` / `disabled` string)
- **PUT** - Enable or disable preSelection (`true` / `false` boolean)

GET and PUT use different types for the same setting. That is the published schema.

| File | Example name | Summary |
|---|---|---|
| `GET/disabled.json` | `disabled` | Current preSelection state (`disabled`) |
| `PUT/enable.json` | `enable` | Enable preSelection (`true`) |
| `PUT/success.json` | `success` | Empty string on success |
