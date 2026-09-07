# FXR60 Certificate Download Authentication Test Report

> **Superseded by a retest.** These results are from reader application **5.0.5**
> on a different reader (`10.117.229.9`). The same tests were repeated on **5.0.7**
> — see `CERTIFICATE_AUTH_TEST_REPORT_507.md` in this folder. All findings below
> still hold on 5.0.7; nothing was fixed.

## Scope

Tested `PUT /cloud/certificates` on an FXR60 with Reader Application version
`5.0.5`.

The test PFX server was hosted at:

```text
https://10.117.229.18/reader-test.pfx
```

The PFX server was independently verified to support Basic authentication,
Bearer authentication, anonymous access, and mutual TLS.

## Results

| Download security method | Result on reader | Server observation |
| --- | --- | --- |
| Basic authentication | Success | Reader downloaded PFX and installed certificate |
| Bearer token header | Failed: HTTP 422 | Reader did not contact PFX server |
| None authentication | Failed: HTTP 422 | Reader did not contact PFX server |
| Mutual TLS | Failed: HTTP 422 | Reader connected but did not present a client certificate |

## Working Basic Authentication Request

This request completed successfully. The reader downloaded the PFX and
installed the client certificate.

```json
{
  "name": "scenario-basic",
  "type": "client",
  "url": "https://10.117.229.18/reader-test.pfx",
  "authenticationType": "BASIC",
  "authenticationOptions": {
    "username": "altautoadmin",
    "password": "@1T@uT0dud3"
  },
  "pfxPassword": "Fxr60-Pfx-Setup-2026-47!",
  "verifyPeer": false,
  "verifyHost": false
}
```

## Bearer Token Header Failure

The PFX server accepts a valid Bearer token when directly tested. The reader
does not send a request to the PFX server when this field is included:

```json
{
  "name": "scenario-sync",
  "type": "client",
  "url": "https://10.117.229.18/reader-test.pfx",
  "authenticationType": "NONE",
  "pfxPassword": "Fxr60-Pfx-Setup-2026-47!",
  "verifyPeer": false,
  "verifyHost": false,
  "headers": {
    "Authorization": "Bearer @1T@uT0dud3"
  }
}
```

Reader response:

```text
HTTP 422
CS:'Add/Refresh certificate' failed, Reason: INVALID USER NAME
```

## None Authentication Failure

The PFX server was configured to allow anonymous download. The reader did not
contact the server when this request field was used:

```json
{
  "name": "FXR60_CLIENT_NONE_TEST",
  "type": "client",
  "url": "https://10.117.229.18/reader-test.pfx",
  "authenticationType": "NONE",
  "pfxPassword": "Fxr60-Pfx-Setup-2026-47!",
  "verifyPeer": false,
  "verifyHost": false
}
```

Reader response:

```text
HTTP 422
CS:'Add/Refresh certificate' failed, Reason: INVALID USER NAME
```

## Mutual TLS Failure

The request used a trusted CA certificate and an already installed reader
client certificate:

```json
{
  "name": "FXR60_CLIENT_MTLS_TEST",
  "type": "client",
  "url": "https://10.117.229.18/reader-test.pfx",
  "authenticationType": "BASIC",
  "authenticationOptions": {
    "username": "altautoadmin",
    "password": "@1T@uT0dud3"
  },
  "pfxPassword": "Fxr60-Pfx-Setup-2026-47!",
  "verifyPeer": true,
  "verifyHost": true,
  "CACertificateFileContent": "-----BEGIN CERTIFICATE-----\nMIIDrzCCApegAwIBAgIUb9ovduakrBygqw6Na3Ns6otV0M0wDQYJKoZIhvcNAQEL\nBQAwZzELMAkGA1UEBhMCSU4xCzAJBgNVBAgMAktBMRswGQYDVQQKDBJaZWJyYSBU\nZWNobm9sb2dpZXMxETAPBgNVBAsMCFJGSUQgRGV2MRswGQYDVQQDDBJMb2NhbCBS\nRklEIFRlc3QgQ0EwHhcNMjYwODMxMTAzNTEzWhcNMzEwODMwMTAzNTEzWjBnMQsw\nCQYDVQQGEwJJTjELMAkGA1UECAwCS0ExGzAZBgNVBAoMElplYnJhIFRlY2hub2xv\nd2llczERMA8GA1UECwwIUkZJRCBEZXYxGzAZBgNVBAMMEkxvY2FsIFJGSUQgVGVz\ndCBDQTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAOKV9GtlUGXCruWz\nW5T6MSLbUs4IXv/9kJsPLeADSLRk/1Xjl9+AS6vixBosrkuAsm3X/vU6ykBAjzGi\ncocZngv0aVzgdCNM1J4RR0aS2CUIp1FV31Iz72XJjS3ulxOsgcstM44iEF8on9Is\nVEdKYXqaTTP0YMGG2fD5MtoKAsHEdTxR/FnZrpHGvFLXVrPfYug9G+lAUb2Xsvj5\nM3c/qaAM1PwEvLeFH1MWaGpjmMcXls8n/qomf+uh8lcS/0Of2ksoY0o0Q1oQwgzP\nrOvLYF66Y/tueFEBkTqy1lwgRqRJ/1kKoAsIBn6xttY5UAql2rOYK4NO21HoXyVY\nqQxNhIkCAwEAAaNTMFEwHQYDVR0OBBYEFO1CW4HEW6mN54qvlNeXEEIvT04oMB8G\nA1UdIwQYMBaAFO1CW4HEW6mN54qvlNeXEEIvT04oMA8GA1UdEwEB/wQFMAMBAf8w\nDQYJKoZIhvcNAQELBQADggEBAMVupCrz32H3q3w8KmphvnU9jg5S4OsaunnauDlI\nY84+zYrrJ1o17JvsgVSBcQ7BaeNnWm4e4Ojp7DWspkb13bWL8BBwa2+tU0hMW263\nZ6i0R4xYaG6JFHJWzoSJnU8sW9p80OZYjicygpKn2QYbWBByGqn/cziku2kwqril\n70spL+COE8X2r1EBlzf5vXQ8WRLCVmPFPY3equxW42+LApH+X/5GoD6vW1fM0zGy\nkcFnENqR7ZoaOD63sXUe+EcHPweVi/hG58CsuhdnpwJUrVsqCq5Kljzs2cWgBsw1\npWflnnSH1JgN2dqLDy6bZktSQya5qqohoETOU0fQMJGLK+Q=\n-----END CERTIFICATE-----",
  "installedCertificateType": "client",
  "installedCertificateName": "scenario-basic"
}
```

Reader response:

```text
HTTP 422
CS:'Add/Refresh certificate response' failed
```

PFX server log:

```text
TLS handshake failed from <reader-IP>:
PEER_DID_NOT_RETURN_A_CERTIFICATE
```

## Request for Investigation

Please confirm whether FXR60 Reader Application `5.0.5` supports the following
for `PUT /cloud/certificates`:

- `authenticationType: NONE`
- custom `headers.Authorization` Bearer token authentication
- installed client-certificate selection for mTLS

Basic authentication through `authenticationOptions` is the only tested method
that completed successfully.