# `/cloud/cableLossCompensation`

- **GET** - Retrieves the cableLossCompensation (`getCablelosscompensation`)
- **PUT** - Sets the cableLossCompensation (`setCablelosscompensation`)

## Reviewed PUT

| File | Example name | Summary |
|---|---|---|
| `PUT/cable_loss.json` | `cable_loss` | Port 1: 90 ft at 18 dB/100ft |
| `PUT/success.json` | `success` | Empty string on success |

## Method folders

```
cloud-cablelosscompensation/
  GET/     # GET response examples
  PUT/     # PUT request/response examples
```

| File | Method | Direction | Example name | Origin | Valid | Summary |
|---|---|---|---|---|---|---|
| `PUT/cable_loss.json` | PUT | request | `cable_loss` | reviewed | yes | Port 1: 90 ft at 18 dB/100ft |
| `PUT/success.json` | PUT | response | `success` | reviewed | yes | Empty string on success |
| `GET/inline.json` | GET | response 200 | `inline` | in-spec | yes |  |

## Trying these against a reader

```bash
READER=10.0.0.42
TOKEN=$(curl -sk -u admin:PASSWORD https://$READER/cloud/localRestLogin | jq -r .message)

curl -sk -X GET "https://$READER/cloud/cableLossCompensation" \
  -H "Authorization: Bearer $TOKEN"

curl -sk -X PUT "https://$READER/cloud/cableLossCompensation" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @PUT/cable_loss.json
```
