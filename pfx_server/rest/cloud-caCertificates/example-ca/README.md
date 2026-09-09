# A working CA certificate for the spec example

The `set_InstallCACertificate` example in `openAPISpec 12.yaml` contains a
placeholder that is **not a valid certificate** — it fails base64 decoding and
`openssl x509`, and the reader rejects it with `INVALID CA CERTIFICATE CONTENT`.

These files are a drop-in replacement, generated and **verified working** on a
live reader.

## The certificate

```
Subject   C=US, ST=CA, L=Irvine, O=Zebra Technologies,
          OU=Engineering, CN=Zebra Example Root CA
Valid     2026-09-08 to 2036-09-05  (10 years)
Key       RSA 2048, SHA-256
X509v3    basicConstraints = critical, CA:TRUE
          keyUsage         = critical, Certificate Sign, CRL Sign
Size      1424 bytes PEM
```

A genuine self-signed root CA — `CA:TRUE` and the correct key usage, so it is
suitable as a real example rather than a stand-in.

**No private key is included.** Installing a CA only needs the certificate, and
shipping a key alongside a published example would be a hazard. The key was
generated, used to self-sign, and deleted.

## Verified on the reader

Reader `10.233.48.36`, FXR60 reader application 5.0.7, 2026-09-08:

```
PUT    /cloud/caCertificates   {name, content}        → 200
GET    /cloud/caCertificates                          → ["ZebraExampleRootCA.crt"]
DELETE /cloud/caCertificates   {"name":"ZebraExampleRootCA"}  → 200
GET    /cloud/caCertificates                          → []
```

Full install → list → delete cycle, clean at both ends.

## Files

| File | Use |
|---|---|
[`example-ca.crt`](example-ca.crt) | The certificate, PEM |
[`spec-example.yaml`](spec-example.yaml) | **Paste this into the spec** — the YAML example block |
[`install-request.json`](install-request.json) | The REST request body, exactly as sent |
[`delete-request.json`](delete-request.json) | The REST delete body |
[`mqtt-install-command.json`](mqtt-install-command.json) | MQTT `set_InstallCACertificate` form |
[`mqtt-delete-command.json`](mqtt-delete-command.json) | MQTT `del_CACertificate` form |

`spec-example.yaml` was checked by parsing it back as YAML, unescaping the
`\n` sequences, and running `openssl x509` on the result — it reproduces the
original PEM byte for byte and openssl reads it. So the escaping is correct for
pasting straight into the spec.

## Two caveats for whoever updates the spec

**1. The path in the spec does not work.** `PUT /cloud/caCertificates/{caname}`
returns 404 on this firmware. The example above uses the collection path with
`name` in the body, which is what the reader accepts. See
[`../CA_CERTIFICATES_TEST_REPORT.md`](../CA_CERTIFICATES_TEST_REPORT.md).

**2. `name` must be in the body.** The schema currently says `name` is *"ignored
for local REST"* and lists only `content` as required. On 5.0.7 the opposite is
true — omit `name` and there is no way to name the certificate.

## Regenerating it

```bash
openssl req -x509 -newkey rsa:2048 -sha256 -days 3650 -nodes \
  -keyout example-ca.key -out example-ca.crt \
  -subj "/C=US/ST=CA/L=Irvine/O=Zebra Technologies/OU=Engineering/CN=Zebra Example Root CA" \
  -addext "basicConstraints=critical,CA:TRUE" \
  -addext "keyUsage=critical,keyCertSign,cRLSign"
rm example-ca.key
```
