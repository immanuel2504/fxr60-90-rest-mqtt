# Test 01 result — plain MQTT on our own broker: PASSED

Config: `01-plain-1883-no-security.json` → broker `10.117.229.18:1883`, plain TCP,
`enableSecurity: false`, no security block.

## Evidence

**1. Command round-trip works**

`get_status` published to `fxr60-lab/mcmd`, full response received on `fxr60-lab/mrsp`.

**2. All four reader clients connected** (from `/var/log/mosquitto/mosquitto.log`)

```
Received PINGREQ from fxr60-lab-ctrl
Received PINGREQ from fxr60-lab-data
Received PINGREQ from fxr60-lab-mcmd
Received PINGREQ from fxr60-lab-mevents
Received PUBLISH from fxr60-lab-mevents (... 'fxr60-lab/mevents', 1972 bytes)
```

**3. Heartbeat events arriving** on `fxr60-lab/mevents`, roughly every 60s, ~1970 bytes.

The reader reports its own connection health inside each heartbeat:

```json
"interfaceConnectionStatus": {
  "control":         [{"interface":"CTRL_MQTT",     "connectionStatus":"connected", "connectionError":""}],
  "data":            [{"interface":"DATA_MQTT",     "connectionStatus":"connected", "connectionError":""}],
  "management":      [{"interface":"MGMT_CMD_MQTT", "connectionStatus":"connected", "connectionError":"",
                       "stats":{"commands_received":2,"responses_sent":2,"responses_failed":0}}]
}
```

`commands_received: 2 / responses_sent: 2 / responses_failed: 0` matches exactly the
two `get_status` commands sent — confirmation from both ends independently.

## Worth remembering

Heartbeat events carry per-interface `connectionStatus` and `connectionError`.
That is a far better diagnostic than the generic
`connection initialization failed with return code (255)` seen during the AWS work.
When a connection fails, subscribing to the management-events topic on a *reachable*
broker is the fastest way to learn why — assuming at least one channel still works.
