# Finding 07 — `app-led` cannot be verified, and cannot be reset to `DEFAULT`

**Endpoint** `PUT /cloud/app-led`
**Type** Observability gap + missing reset path
**Status** Confirmed

All four enum colours (`red`, `amber`, `green`, `off`) are accepted with HTTP 200.

## Problem 1 — the state is not observable

`GET /cloud/app-led` returns only:

```json
{"status": "DEFAULT"}   |   {"status": "NON_DEFAULT"}
```

No colour, no flash flag, no remaining duration. The only thing confirmable over
the API is that *some* non-default state is active. **Which colour is actually
lit cannot be determined without physical access to the reader**, so none of the
four colour tests can be verified beyond "accepted".

## Problem 2 — there is no way back to `DEFAULT`

| Action | `status` |
|---|---|
| initial | `DEFAULT` |
| any PUT | `NON_DEFAULT` |
| `{"color":"off","flash":false,"seconds":0}` | `NON_DEFAULT` |

Once any PUT is made, the endpoint reports `NON_DEFAULT` for the rest of the
session. `"off"` turns the LED off but still counts as an application-set state,
and no documented route returns the reader to `DEFAULT`.

This is why the reader was left `NON_DEFAULT` at the end of testing — not an
oversight, but an endpoint limitation. Every other endpoint tested in this batch
was restored byte-identically.

## A quirk in `seconds`

| Value | Result |
|---|---|
| `60` | accepted |
| `0` | accepted — documented as "indefinite" |
| `-5` | rejected: `seconds (expected positive number)` |

So `0` is a special value rather than a duration, and it is not covered by the
"positive" wording in the error.

## Ask

Can `GET /cloud/app-led` return the active colour, flash state and remaining
duration? And is there any way to return to `DEFAULT` — `{"color":"off"}` does
not do it.

## Evidence

| Folder | Test |
|---|---|
| `evidence-1-off-does-not-restore-default/` | `rest/cloud-app-led-PUT/04-off-SUCCESS/` |
| `evidence-2-any-put-goes-non-default/` | `rest/cloud-app-led-PUT/01-amber-flash-60s-SUCCESS/` |
