# `set_appled`

REST: `PUT /cloud/app-led` → `cloud-app-led/`

Stable `command_id`: `req-set-appled`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/app_led.json` | request | `app_led` | `cloud-app-led/PUT/app_led.json` | Amber blink for 60 seconds |
| `request/continuous_alarm.json` | request | `continuous_alarm` | `cloud-app-led/PUT/continuous_alarm.json` | Red, flashing, indefinite (seconds: 0) |
| `response/success.json` | response | `success` | `—` | Command succeeded |
