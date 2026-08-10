## 1. Description

> **Product applicability: FXR60 only — not applicable to the FXR90.** The stack LED (stack light) is an FXR60 feature; the FXR90 has no stack light. This endpoint and its schema are documented here because the stack-light definition is shared across the Zebra fixed-reader family. On an FXR90, use `PUT /cloud/app-led` for the application LED instead.

The `PUT /cloud/stack-led` REST endpoint updates the stack LED state on the reader.

Supported colors: `red`, `amber`, `green`, `blue`, `off`.

Supported brightness: `low`, `med`, `high` (defaults to `low`).

> Note on `blue`: `blue` is valid **here**, on the stack light. It is **not** a valid application LED colour — see `PUT /cloud/app-led`, whose colours are `red`, `amber`, `green`, `off`.

## 2. Endpoint Details

| Property | Value |
|---|---|
| REST Endpoint | `PUT /cloud/stack-led` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | **FXR60** — the FXR90 has no stack light |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |

## 3. Request Body

| Field | Type | Description |
|---|---|---|
| `color` | string | LED color: `red`, `amber`, `green`, `blue`, or `off` |
| `brightness` | string | `low`, `med`, or `high` |
| `flash` | boolean | Whether the LED should blink |
| `seconds` | integer | Duration in seconds; use `0` for indefinite |

## 4. When to Use This Endpoint

Use `PUT /cloud/stack-led` to:

- Set a visual indicator on the reader stack LED
- Temporarily override the default LED state with a timed color/flash pattern
