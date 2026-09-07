# Finding 05 — `region` silently ignores fields it cannot apply

**Endpoint** `PUT /cloud/region`
**Type** Silent no-op
**Status** Confirmed for both optional fields

`GET /cloud/supportedStandardList?region=United States/Canada` reports for
`US_FCC_15`:

```
isLBTConfigurable     "false"
isChannelSelectable   "false"
isHoppingConfigurable "false"
```

Both optional fields were sent anyway:

| Sent | Response | Effect |
|---|---|---|
| `isLBT: true` | **200** | none — `lbtEnabled` still `false` |
| `channeldata: [915750,915250,903250]` | **200** | none — still all 50 channels |

## The problem is the silence, not the behaviour

Refusing to apply them is arguably correct, since the standard genuinely does not
support either. But a caller enabling Listen-Before-Talk receives HTTP 200 and
reasonably concludes LBT is now on.

## A trap when verifying this

Checking the channel **count** is what reveals it. The three channels sent are
already the first three of the standard's own list, so a spot-check of
`channelData[:3]` looks like the narrowing worked:

```
sent:  [915750, 915250, 903250]
after: first3=['915750','915250','903250']   ← looks applied
       len=50                                ← was not applied
```

Only `len() == 50` shows the list was untouched.

## Two typing issues on the same field

| | Input | Output |
|---|---|---|
| Name | `channeldata` | `channelData` |
| Element type | `integer` (per schema) | **string** — `["915750",…]` |

So the field cannot be round-tripped without transforming both its name and its
element type. `isLBTConfigurable` is likewise the string `"false"`, not a boolean.

## Ask

Reject these with something like `isLBT not configurable for standard
US_FCC_15`, rather than accepting and discarding them. And align the input/output
name and element type for `channeldata`/`channelData`.

## Note — region changes themselves work

This finding is only about the two optional fields. Switching standards works and
is fully verifiable; see [[06-region-spec-example-fails-on-us-canada-reader]] for
the tested standard switches.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-isLBT-ignored/` | `rest/cloud-region-PUT/08-isLBT-silently-ignored/` |
| `evidence-2-channeldata-ignored/` | `rest/cloud-region-PUT/09-channeldata-silently-ignored/` |
