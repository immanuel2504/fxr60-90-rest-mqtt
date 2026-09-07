# FXR60 Download Security Test Summary

## Test Environment

- Reader: `https://10.233.48.36`
- HTTPS file server: `https://10.117.229.18`
- Reader model: FXR60
- Final reader application version: `5.0.5-6`

## HTTPS Test Server

- Host and port: `https://10.117.229.18:443`
- Server implementation: [server.py](server.py)
- Served directory: [files](files)
- TLS certificate: [cert.pem](cert.pem)
- TLS private key: [key.pem](key.pem)
- CA used for mutual TLS: [ca/ca.crt](ca/ca.crt)

Available test files include:

```text
reader-test.pfx
sampleNew_1.0.5.deb
sampleAntenna_1.0.4.deb
FXR_5.0.5-6.tar.bz2
```

The server can be started in these modes:

| Mode | Command option | Client requirement |
| --- | --- | --- |
| Anonymous | `--auth none` | No server credentials required |
| Basic | `--auth basic` | HTTP Basic username and password |
| Bearer | `--auth bearer` | `Authorization: Bearer <token>` header |
| Basic plus mTLS | `--auth basic --mtls` | Basic credentials and a client certificate signed by [ca/ca.crt](ca/ca.crt) |

For mTLS, the reader must trust the server CA through
`CACertificateFileContent` and send an installed client certificate through
`installedCertificateType` and `installedCertificateName`.

## Certificate Installation

Endpoint: `PUT /cloud/certificates`

| Download security method | Result | Evidence |
| --- | --- | --- |
| Basic authentication | Works | Reader downloaded the PFX with Basic authentication and installed certificates `scenario-basic` and `FXR60_CLIENT_RETRY_TEST` |
| None authentication | Does not work | Reader returned HTTP 422 `INVALID USER NAME` before contacting the PFX server |
| Bearer header | Does not work | Reader returned HTTP 422 `INVALID USER NAME` before contacting the PFX server |
| Mutual TLS | Does not work | Reader did not present a client certificate; server reported `PEER_DID_NOT_RETURN_A_CERTIFICATE` |

Conclusion: use `authenticationType: BASIC` with `authenticationOptions` for
certificate downloads on this reader.

## User-App Installation

Endpoint: `PUT /cloud/apps/install`

| Download security method | Result | Evidence |
| --- | --- | --- |
| Basic authentication | Works | Reader downloaded and installed the app |
| None authentication | Works | Reader downloaded from an anonymous server and installed the app |
| Bearer header | Works | Reader sent a Bearer header and installed the app |
| Mutual TLS plus Basic | Works | Reader presented client certificate `scenario-basic`; server logged `peer_cn=reader` |

Installed sample applications:

```text
sampleNew
sampleAntenna
```

Conclusion: all four tested security methods work for user-app installation.

## OS Update

Endpoint: `PUT /cloud/os`

| Download security method | Result | Evidence |
| --- | --- | --- |
| Basic authentication | Works | Reader downloaded the firmware, flashed it, rebooted, and reported version `5.0.5-6` |
| None authentication | Works with caveat | Reader downloaded from an anonymous server, but still sent a Basic Authorization header |
| Bearer header | Does not work | Reader ignored the supplied Bearer header, sent Basic authentication, and the Bearer-only server returned HTTP 401 |
| Mutual TLS plus Basic | Does not work | Reader did not present a client certificate; server reported `PEER_DID_NOT_RETURN_A_CERTIFICATE` |

Conclusion: Basic authentication is the verified secure OS-download method.
Anonymous download works only when the server accepts the reader's unexpected
Basic Authorization header. Bearer-header and mTLS download were not successful.

## Saved Request Bodies

- Certificate requests: [request-certificate-basic.json](request-certificate-basic.json) and [request-certificate-retry.json](request-certificate-retry.json)
- App-install requests: [app](app)
- Successful OS request: [os/os-update-basic.json](os/os-update-basic.json)
- Detailed reports: [CERTIFICATE_AUTH_TEST_REPORT.md](CERTIFICATE_AUTH_TEST_REPORT.md), [APP_INSTALL_AUTH_TEST_REPORT.md](APP_INSTALL_AUTH_TEST_REPORT.md), and [OS_UPDATE_AUTH_TEST_REPORT.md](OS_UPDATE_AUTH_TEST_REPORT.md)