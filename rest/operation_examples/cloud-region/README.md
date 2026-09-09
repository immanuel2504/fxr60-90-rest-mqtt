# `/cloud/region`

- **GET** — Active RF region (`get_region`)
- **PUT** — Set country and standard (`set_region`)

## GET examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `GET/region.json` | response 200 | `region` | United States/Canada, US_FCC_15 |

## PUT examples

| File | Direction | Example name | Summary |
|---|---|---|---|
| `PUT/us_fcc_15.json` | request | `us_fcc_15` | United States/Canada, US_FCC_15 |
| `PUT/us_fcc_a.json` | request | `us_fcc_a` | United States/Canada, US_FCC_A |
| `PUT/us_fcc_c.json` | request | `us_fcc_c` | United States/Canada, US_FCC_C |
| `PUT/success.json` | response 200 | `success` | Empty string on success |
