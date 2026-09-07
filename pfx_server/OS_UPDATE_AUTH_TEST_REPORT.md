# FXR60 OS Update Download Authentication Test Report

## Scope

Tested `PUT /cloud/os` on the FXR60 reader at `10.233.48.36`.

Firmware source:

```text
https://10.117.229.18/FXR_5.0.5-6.tar.bz2
```

The approved firmware update completed successfully with Reader Application
version `5.0.5-6` installed.

## Results

| Download security method | Result | Server observation |
| --- | --- | --- |
| Basic authentication | Success | Reader downloaded firmware with Basic auth, flashed, rebooted, and reported `5.0.5-6` |
| Bearer token header | Failed | Reader sent Basic authentication instead of the supplied Bearer header; Bearer-only server returned HTTP 401 |
| Mutual TLS plus Basic | Failed | Reader did not present its installed client certificate; mTLS handshake failed |

## Working Basic Authentication Request

```json
{
  "url": "https://10.117.229.18/FXR_5.0.5-6.tar.bz2",
  "authenticationType": "BASIC",
  "authenticationOptions": {
    "username": "altautoadmin",
    "password": "@1T@uT0dud3"
  },
  "verifyPeer": false,
  "verifyHost": false,
  "retry": {
    "type": "randomWait",
    "policy": {
      "retries": 3,
      "wait": {
        "min": 10,
        "max": 30
      }
    }
  },
  "timeouts": {
    "connection": 5,
    "read": 20
  }
}
```

Result: `HTTP 200` acknowledgment. The reader downloaded, flashed, rebooted,
and reported:

```text
readerApplication: 5.0.5-6
```

## Bearer Token Header Request

The file server was configured as Bearer-only.

```json
{
  "url": "https://10.117.229.18/FXR_5.0.5-6.tar.bz2",
  "authenticationType": "NONE",
  "headers": {
    "Authorization": "Bearer @1T@uT0dud3"
  },
  "verifyPeer": false,
  "verifyHost": false,
  "retry": {
    "type": "randomWait",
    "policy": {
      "retries": 3,
      "wait": {
        "min": 10,
        "max": 30
      }
    }
  },
  "timeouts": {
    "connection": 5,
    "read": 20
  }
}
```

The REST endpoint returned the immediate asynchronous acknowledgment:

```text
HTTP 200
```

However, the reader requested the firmware with Basic authentication instead
of Bearer authentication. The Bearer-only server rejected it:

```text
GET /FXR_5.0.5-6.tar.bz2 (auth=Basic)
HTTP 401
```

The reader remained online and did not start flashing.

## Mutual TLS Plus Basic Request

The source server was configured with `--auth basic --mtls`. The request
selected the installed client certificate named `scenario-basic`.

```json
{
  "url": "https://10.117.229.18/FXR_5.0.5-6.tar.bz2",
  "authenticationType": "BASIC",
  "authenticationOptions": {
    "username": "altautoadmin",
    "password": "@1T@uT0dud3"
  },
  "verifyPeer": true,
  "verifyHost": true,
  "CACertificateFileContent": "<local CA PEM>",
  "installedCertificateType": "client",
  "installedCertificateName": "scenario-basic",
  "retry": {
    "type": "randomWait",
    "policy": {
      "retries": 3,
      "wait": {
        "min": 10,
        "max": 30
      }
    }
  },
  "timeouts": {
    "connection": 5,
    "read": 20
  }
}
```

The REST endpoint returned `HTTP 200` as an asynchronous acknowledgment, but
the mTLS server logged:

```text
TLS handshake failed from 10.233.48.36:
PEER_DID_NOT_RETURN_A_CERTIFICATE
```

The reader did not send the selected installed client certificate, so firmware
download and flashing did not start.

## Conclusion

For `PUT /cloud/os` on this reader, Basic download authentication is verified
to work. Bearer header authentication and mTLS client-certificate selection did
not work in these tests.