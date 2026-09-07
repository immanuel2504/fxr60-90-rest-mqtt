# FXR60 Certificate Download Authentication — Reader Application 5.0.7

Retest of `PUT /cloud/certificates` download authentication on a newer firmware,
repeating the 5.0.5 tests in `CERTIFICATE_AUTH_TEST_REPORT_505.md` (same folder).

## Scope

| | 5.0.5 test | 5.0.7 test (this one) |
|---|---|---|
| Reader | `10.117.229.9` | `10.233.48.36` |
| Reader application | 5.0.5 | **5.0.7** |
| Serial | — | 260975251E0049 |
| File server | `https://10.117.229.18` | same |

Note the reader is on a different subnet (`10.233.48.x`) from the file server
(`10.117.229.x`) and routed across successfully — cross-subnet fetch is not a
problem.

Raw request/response captures: the five numbered folders alongside this report.

## Results

| # | Download auth method | 5.0.5 | 5.0.7 | Changed? |
|---|---|---|---|---|
| 1 | `BASIC` via `authenticationOptions` | ✅ 200 | ✅ **200** | no |
| 2 | Bearer token in `headers.Authorization` | ❌ 422 | ❌ **422** | no |
| 3 | `authenticationType: NONE` (anonymous) | ❌ 422 | ❌ **422** | no |
| 4 | mTLS where server does *not* require a client cert | not tested | ✅ **200** | new result |
| 5 | mTLS where server *does* require a client cert | ❌ 422 | ❌ **422** | no |

**Conclusion: 5.0.7 behaves identically to 5.0.5.** Basic authentication remains
the only working method. None of the three previously reported failures are fixed.

---

## 1. BASIC authentication — works

```json
{
  "name": "TEST-BASIC-507",
  "type": "client",
  "url": "https://10.117.229.18/fxr60-lab-client.pfx",
  "authenticationType": "BASIC",
  "authenticationOptions": {
    "username": "altautoadmin",
    "password": "@1T@uT0dud3"
  },
  "pfxPassword": "Fxr60-Client-Pfx-2026!",
  "verifyPeer": false,
  "verifyHost": false
}
```

`HTTP 200`, empty body. Confirmed installed via `GET /cloud/certificates`:

```
TEST-BASIC-507   type=client  installed=Sat Sep  5 13:27:21 2026
```

File server log shows the reader's fetch:

```
10.233.48.36 - - [05/Sep/2026 13:27:21] GET /fxr60-lab-client.pfx (auth=Basic)
10.233.48.36 - - [05/Sep/2026 13:27:21] "GET /fxr60-lab-client.pfx HTTP/1.1" 200 -
```

---

## 2. Bearer token header — fails

```json
{
  "authenticationType": "NONE",
  "headers": { "Authorization": "Bearer @1T@uT0dud3" }
}
```

```json
{"code":3,"message":"CS:'Add/Refresh certificate' failed,Reason: INVALID USER NAME"}
```
`HTTP 422` — identical to 5.0.5.

---

## 3. `authenticationType: NONE` — fails, and the reader never tries

This test was run more carefully than on 5.0.5, to separate a reader-side refusal
from a download failure.

The file server was switched to **anonymous mode** and verified serving without
credentials:

```
$ curl -sk -o /dev/null -w "%{http_code}\n" https://10.117.229.18/fxr60-lab-client.pfx
200
```

The reader still refused:

```json
{"code":3,"message":"CS:'Add/Refresh certificate' failed,Reason: INVALID USER NAME"}
```

**The file server log contains no request from the reader at all.** Only the
verification fetch from `10.117.229.18` appears:

```
10.117.229.18 - - [05/Sep/2026 13:29:03] GET /fxr60-lab-client.pfx (auth=<none>)
10.117.229.18 - - [05/Sep/2026 13:29:03] "GET /fxr60-lab-client.pfx HTTP/1.1" 200 -
```

### What this establishes

The reader **rejects `authenticationType: NONE` internally and makes no HTTP
request**. It is not that anonymous download fails — the reader never attempts it.

The error text is also misleading: `INVALID USER NAME` is reported when no
username was supplied and none was required.

Since `NONE` is a documented enum value for `authenticationType`, this looks like
unimplemented functionality rather than intended behaviour.

---

## 4. mTLS where the server does not require a client cert — works

```json
{
  "authenticationType": "BASIC",
  "authenticationOptions": { "username": "altautoadmin", "password": "@1T@uT0dud3" },
  "verifyPeer": true,
  "verifyHost": true,
  "CACertificateFileContent": "<ca/ca.crt>",
  "installedCertificateType": "client",
  "installedCertificateName": "FXR60-LAB-CLIENT"
}
```

`HTTP 200`, installed at 13:30:29. Server log confirms the reader fetched it.

### Careful reading of this result

The file server was running **without** `require_certificate`, so it never asked
the reader for a client certificate. What this test actually proves:

- ✅ `verifyPeer` / `verifyHost` work — the reader validated the server's
  certificate against the supplied CA and proceeded
- ✅ `CACertificateFileContent` is accepted and used
- ❌ It does **not** show the reader can present a client certificate — nothing
  asked it to

That distinction is what test 5 addresses. Reporting this as "mTLS works" would be
wrong.

---

## 5. mTLS where the server requires a client cert — fails

The file server was restarted with `--mtls` (`require_certificate`), and its
behaviour verified first:

```
without client cert : rejected during TLS handshake
with lab-CA cert    : HTTP 200, logged peer_cn=FXR60-LAB-CLIENT
```

Same request body as test 4. Result:

```json
{"code":3,"message":"CS:'Add/Refresh certificate response' failed"}
```
`HTTP 422`

**The reader does not appear in the server log at all** — only the verification
fetch from this host:

```
10.117.229.18 - - [05/Sep/2026 13:33:13] GET /fxr60-lab-client.pfx (auth=Basic peer_cn=FXR60-LAB-CLIENT)
```

### What this establishes

The reader **fails the TLS handshake without presenting a client certificate**,
even though `installedCertificateName: "FXR60-LAB-CLIENT"` names a certificate
confirmed present in its own store via `GET /cloud/certificates`.

This matches the 5.0.5 finding exactly, where the server logged
`PEER_DID_NOT_RETURN_A_CERTIFICATE`.

`installedCertificateType` / `installedCertificateName` appear to be accepted and
ignored for the purpose of client authentication during download.

---

## Request for investigation

Unchanged from the 5.0.5 report — all three issues persist on 5.0.7.

1. **`authenticationType: NONE`** — documented enum value, but the reader refuses
   it without making any HTTP request. Is anonymous download supported? If not,
   the enum value should be removed or documented as unsupported.

2. **`headers.Authorization` Bearer token** — accepted in the request body but the
   reader makes no HTTP request. Same question.

3. **`installedCertificateName` / `installedCertificateType` for mTLS** — accepted
   without error, but the reader presents no client certificate during the TLS
   handshake. Confirmed against a server that demands one.

4. **Misleading error text** — `INVALID USER NAME` is returned for cases where no
   username was supplied or required. A message such as
   `authentication type not supported` would have saved considerable time.

Basic authentication via `authenticationOptions` remains the only method confirmed
working, on both firmware versions.

---

## Reproducing

Raw captures for all five tests, request and response:

```
01-BASIC-success/
02-BEARER-header-failed/
03-NONE-anonymous-failed/
04-mTLS-optional-success/
05-mTLS-required-failed/
```

Each contains `request body/request.json` and `response body/response.json` plus
`http_status.txt`, with server-side evidence recorded in the response notes where
relevant.

The file server modes used:

Run from the project root (`/home/altautoadmin/pfx_server`):

```bash
# tests 1, 2, 4 - normal service
sudo systemctl start pfx-file-server

# test 3 - anonymous
sudo -n env PFX_USER=x PFX_PASS=x .venv/bin/python3 server.py --auth none --port 443

# test 5 - client cert required
sudo -n env PFX_USER='altautoadmin' PFX_PASS='@1T@uT0dud3' \
  .venv/bin/python3 server.py --auth basic --mtls --port 443
```

The normal `pfx-file-server` service was restored afterwards and verified serving.
