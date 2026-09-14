# `/cloud/preSelection`

- **GET** - Current preSelection state (`enabled` / `disabled` string)
- **PUT** - Enable or disable preSelection (`true` / `false` boolean)

GET and PUT use different types for the same setting. That is the published schema.

| File | Example name | Summary |
|---|---|---|
| `GET/preselection_disabled.json` | `preselection_disabled` | Preselection disabled |
| `PUT/enable_preselection.json` | `enable_preselection` | Enable preselection |
| `PUT/success.json` | `success` | Empty string on success |
