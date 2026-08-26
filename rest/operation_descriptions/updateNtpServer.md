## 1. Description

The `PUT /cloud/ntpServer` REST endpoint sets one or more NTP servers used by the reader for time synchronization.

This endpoint allows you to configure:

- The primary NTP server through `server` (current convention) or `server1` (legacy convention)
- An optional secondary NTP server through `server2`

Use this endpoint to:

- Point the reader to your organization's NTP server for accurate timekeeping
- Configure fallback NTP servers for resilience when the primary is unreachable
- Correct clock drift that is affecting event timestamps and log correlation
- Standardize NTP configuration across a fleet of readers

## 2. Endpoint Details

| Property | Value |
|---|---|
| MQTT Command | `set_ntpServer` |
| Pattern Name | NTP Server Configuration |
| REST Endpoint | `PUT /cloud/ntpServer` |
| Communication Type | Client to Device (HTTP request/response) |
| Applies To | FXR60 / FXR90 |
| Authentication | Bearer token (`Authorization: Bearer <token>`) |
| Content-Type | `application/json` |
| Required Request Fields | `server` (or `server1` for the legacy convention) |

## 3. Before You Begin

Confirm that the NTP server is reachable from the reader's network before sending this request. An unreachable NTP server will leave the reader clock unsynchronized.

| What You Need | Details |
|---|---|
| Primary NTP server | Hostname or IP address of the primary NTP server. Provide it as `server` (current convention) or `server1` (legacy convention). The reader must be able to reach this address on UDP port 123. |
| Secondary NTP server | Optional - provide `server2` as a backup time source. |
| Network access | NTP uses UDP port 123. Ensure this port is open between the reader and the NTP server on all network paths. |
