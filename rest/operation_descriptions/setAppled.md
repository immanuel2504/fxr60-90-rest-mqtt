## 1. Description

The `PUT /cloud/app-led` REST endpoint sets the color, flash behavior, and duration of the application LED on the reader.

This endpoint allows you to configure:

- The LED color through `color`
- Whether the LED flashes through `flash`
- How long the LED state persists through `seconds`

Use this endpoint to:

- Signal application state to operators on the floor using the reader LED
- Flash the application LED to draw attention to a reader requiring action
- Set a timed LED state that automatically resets after a defined duration
- Override the default LED behavior from application logic

## 2. Endpoint Details

| Property | Value |
|---|---|
| Pattern Name | Application LED Control |
| REST Endpoint | `PUT /cloud/app-led` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Supported Colors | `red`, `amber`, `green`, `off` |

## 3. Before You Begin

Decide on the LED color, flash behavior, and duration before sending this request.

| What You Need | Details |
|---|---|
| LED color | One of `red`, `amber`, `green`, or `off` to turn the LED off. |
| Flash behavior | Whether the LED should blink (`true`) or remain solid (`false`). |
| Duration | How long in seconds the LED state should persist. Set to `0` for indefinite (until the next `PUT /cloud/app-led` request). |
