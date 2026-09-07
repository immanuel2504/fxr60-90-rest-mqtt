# FXR60 User-App Download Authentication Test Report

## Scope

Tested `PUT /cloud/apps/install` on an FXR60 running Reader Application
version `5.0.5`.

Package URL base:

```text
https://10.117.229.18/
```

Test package: `sampleAntenna_1.0.4.deb`, a valid Zebra Data Application with
`APP_TYPE: DA` metadata.

## Results

| Download security method | Result | Server observation |
| --- | --- | --- |
| Basic authentication | Success | Reader downloaded the package with Basic authentication and installed it |
| None authentication | Success | Reader downloaded the package without credentials and installed it |
| Bearer token header | Success | Reader downloaded the package with Bearer authentication and installed it |
| Mutual TLS plus Basic | Success | Reader presented its client certificate, used Basic authentication, and installed the package |

The app was removed between tests so each security method installed the same
package from a clean app state.

## Basic Authentication Request

```json
{
  "url": "https://10.117.229.18/",
  "filename": "sampleAntenna_1.0.4.deb",
  "authenticationType": "BASIC",
  "options": {
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

## None Authentication Request

The source server was configured with `--auth none`.

```json
{
  "url": "https://10.117.229.18/",
  "filename": "sampleAntenna_1.0.4.deb",
  "authenticationType": "NONE",
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

Reader result: `HTTP 200`. Server log recorded `auth=<none>` and `HTTP 200`.

## Bearer Header Request

The source server was configured with `--auth bearer`.

```json
{
  "url": "https://10.117.229.18/",
  "filename": "sampleAntenna_1.0.4.deb",
  "authenticationType": "NONE",
  "verifyPeer": false,
  "verifyHost": false,
  "headers": {
    "Authorization": "Bearer @1T@uT0dud3"
  },
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

Reader result: `HTTP 200`. Server log recorded `auth=Bearer` and `HTTP 200`.

## Mutual TLS Plus Basic Request

The source server was configured with `--auth basic --mtls`. The reader used
the already installed client certificate named `scenario-basic`.

```json
{
  "url": "https://10.117.229.18/",
  "filename": "sampleAntenna_1.0.4.deb",
  "authenticationType": "BASIC",
  "options": {
    "username": "altautoadmin",
    "password": "@1T@uT0dud3"
  },
  "verifyPeer": true,
  "verifyHost": true,
  "CACertificateFileContent": "<local-CA-PEM>",
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

Reader result: `HTTP 200`. Server log recorded:

```text
GET /sampleAntenna_1.0.4.deb (auth=Basic peer_cn=reader)
HTTP 200
```

## Conclusion

All four tested download-security methods work for `PUT /cloud/apps/install` on
this reader. This differs from `PUT /cloud/certificates`, where only Basic
download authentication completed successfully.