# Finding 13 — `GPIO-LED` replaces wholesale — it does not merge

**Endpoint** `PUT /cloud/config` (`GPIO-LED`)
**Type** Undocumented update semantics
**Status** Confirmed

Sending a `GPIO-LED` object **replaces the entire stored object**. Any event not
named in the request is discarded, silently and with HTTP 200.

So a request configuring only `RADIO_START` removes any previously configured
`CLOUD_CONNECT`, `TAG_READ`, GPI events and defaults.

## Why this is easy to get wrong

Nothing in the response indicates anything was dropped. The caller sees success
and has no reason to re-read the config. And it is the **opposite** of
`PUT /cloud/displayConfig`, which merges — see
[[08-displayconfig-merges-partial-updates]].

| Endpoint | Partial update |
|---|---|
| `PUT /cloud/config` → `GPIO-LED` | **replaces** — omitted events discarded |
| `PUT /cloud/displayConfig` | **merges** — omitted fields preserved |

## Practical consequence

Always send the **complete** `GPIO-LED` object, including every event you want to
keep. Read the current object with `GET /cloud/config` first and modify it, rather
than sending a fragment.

## A related positive result

`GPIO-LED` is independent of the data plane: test 17 clears the data endpoint and
keeps `GPIO-LED`, and the GPIO actions still fire with no data endpoint
configured at all. The two objects are stored and evaluated separately — it is
only *within* `GPIO-LED` that replacement applies.

## Ask

Document the replace semantics, and state them per endpoint across the API.

## Evidence

`request body/` + `response body/` — `rest/cloud-config-PUT/17-combined-clear-data-keep-gpio-SUCCESS/`
