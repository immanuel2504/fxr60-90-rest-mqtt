# CA certificates — `openAPISpec 12.yaml` tested against a live reader

The three CA certificate operations in the latest spec, tested end to end.

| | |
|---|---|
| Spec | `openAPISpec 12.yaml` — IoT Connector REST API v3.0.0 |
| Reader | `10.233.48.36` — FXR60, reader application 5.0.7 |
| Date | 2026-09-08 |
| Operations | `GET /cloud/caCertificates`, `PUT` + `DELETE /cloud/caCertificates/{caname}` |

---

## Results

| Operation | Documented as | Actual | Result |
|---|---|---|---|
| List | `GET /cloud/caCertificates` | same | ✅ **works** |
| Install | `PUT /cloud/caCertificates/{caname}` | **`PUT /cloud/caCertificates`** | 🐛 **404 as documented** |
| Delete | `DELETE /cloud/caCertificates/{caname}` | **`DELETE /cloud/caCertificates`** | 🐛 **404 as documented** |

**Two of the three documented paths do not exist on this firmware.** Both
`{caname}` operations return HTTP 404. The functionality works, but only through
the collection path with the name in the request body.

A full install → list → delete cycle was completed successfully once the correct
shape was found.

---

## 1. ✅ `GET /cloud/caCertificates` — works as documented

```
GET /cloud/caCertificates
→ 200  []
```

Schema and example match: an array of strings. The reader had no CA certificates
installed, so the empty array is correct.

The documented example is `["AmazonRootCA1", "broker.emqx.io-ca"]` — plain names
with no extension. **See [finding 4](#4--the-name-does-not-round-trip)**: the
reader actually returns names *with* `.crt` appended, so the example's format is
wrong too.

---

## 2. 🐛 `PUT /cloud/caCertificates/{caname}` returns 404

The spec documents installation at the item path. Sent exactly as documented:

```
PUT /cloud/caCertificates/AmazonRootCA1
{"content": "-----BEGIN CERTIFICATE-----\n…"}

→ 404 {"message":"/caCertificates/AmazonRootCA1is not a valid URI.Request not valid"}
```

**The path does not exist.** Installation works on the collection instead, with
the name supplied in the body:

```
PUT /cloud/caCertificates
{"name": "lab-rfid-ca", "content": "-----BEGIN CERTIFICATE-----\n…"}

→ 200  (empty body)
```

This inverts what the schema says about `name`:

> **Required for MQTT API** (`set_InstallCACertificate`). **Ignored for local
> REST** where the path parameter `{caname}` is used.

On this firmware the opposite holds — `name` in the body is **required** for
local REST, and the path parameter does not work at all. The schema also marks
only `content` as required, so a client following it omits `name` and has no way
to specify the certificate's name.

> Note the error message is also malformed — `AmazonRootCA1is` runs the path and
> "is" together. The same missing space appears on `/cloud/connectionStatus` and
> `/cloud/logs/nosuchlog`, so it is in shared URI-error formatting.

---

## 3. 🐛 The spec's example certificate is not a valid certificate

Before testing, the example's `content` was checked:

```
base64 body length : 1023 characters
non-base64 chars   : none
base64 decode      : FAILS - "Incorrect padding"
openssl x509       : "unable to load certificate"
```

The PEM ends with `X0Y1Z2a3b4c5d6e7f8g9h0i1j2k3l4m5n` — sequential filler, not
real base64. It is a placeholder dressed as a certificate.

**The reader correctly rejects it.** Sent to the working collection path:

```
PUT /cloud/caCertificates
{"name":"AmazonRootCA1", "content": <the spec's example>}

→ 422 {"code":3,"message":"CS:'addCACertRsp' failed,Reason: INVALID CA CERTIFICATE CONTENT"}
```

Good validation — the reader parses the certificate rather than storing bytes
blindly, and the message names the problem precisely.

But it means **the documented example cannot be copied and run.** Anyone trying
it gets a 404 from the wrong path, and a 422 from the right one.

A real CA (our lab root, 1338 characters, `CN = Local RFID Test CA`) installed
first time with HTTP 200.

---

## 4. 🐛 The name does not round-trip

Install with one name, and the list returns a different one:

| Step | Value |
|---|---|
| Sent to `PUT` | `lab-rfid-ca` |
| Returned by `GET` | **`lab-rfid-ca.crt`** |

The reader appends `.crt`. That would be a cosmetic detail, except **`DELETE`
rejects the value `GET` returns**:

```
DELETE /cloud/caCertificates  {"name":"lab-rfid-ca.crt"}
→ 422 {"code":3,"message":"CS:'delCACertRsp' failed,Reason: INVALID CA CERTIFICATE NAME"}

DELETE /cloud/caCertificates  {"name":"lab-rfid-ca"}
→ 200  (deleted)
```

Verified twice, install-to-delete both times.

So a client that lists certificates and then deletes one — the obvious
workflow — **fails**. It must strip the `.crt` suffix that the reader itself
added. Nothing in the spec mentions the suffix or the stripping.

---

## 5. 🐛 `DELETE /cloud/caCertificates/{caname}` returns 404

Both name forms were tried against the documented path:

```
DELETE /cloud/caCertificates/lab-rfid-ca      → 404
DELETE /cloud/caCertificates/lab-rfid-ca.crt  → 404
```

Deletion works on the collection with a body:

```
DELETE /cloud/caCertificates
{"name": "lab-rfid-ca"}
→ 200
```

The spec documents no request body for `DELETE` at all — it relies entirely on
the path parameter. So the working form is completely undocumented.

Method checks on the collection:

| Request | Response |
|---|---|
| `POST /cloud/caCertificates` | 405 `POST not a valid METHOD for Req :/caCertificates` |
| `DELETE /cloud/caCertificates` with no body | 422 `Invalid payload fields` |
| `DELETE` with `{"caname":"…"}` | 422 `Invalid payload fields` — the key must be `name` |

---

## 6. ✅ The full cycle works

Once the correct shapes are used:

```
GET    /cloud/caCertificates                              → []
PUT    /cloud/caCertificates  {name, content}             → 200
GET    /cloud/caCertificates                              → ["lab-rfid-ca.crt"]
DELETE /cloud/caCertificates  {name: "lab-rfid-ca"}       → 200
GET    /cloud/caCertificates                              → []
```

The feature itself is sound — content is validated, the certificate is stored and
listed, and deletion is clean. Only the documented interface is wrong.

---

## Corrected reference

What actually works on FXR60 5.0.7:

| Operation | Method | Path | Body |
|---|---|---|---|
| List | `GET` | `/cloud/caCertificates` | — |
| Install | `PUT` | `/cloud/caCertificates` | `{"name": "<name>", "content": "<PEM>"}` |
| Delete | `DELETE` | `/cloud/caCertificates` | `{"name": "<name without .crt>"}` |

**Install:**

```json
{
  "name": "lab-rfid-ca",
  "content": "-----BEGIN CERTIFICATE-----\nMIIDx…\n-----END CERTIFICATE-----\n"
}
```

**Delete** — use the name as installed, *not* as listed:

```json
{"name": "lab-rfid-ca"}
```

---

## Questions for Zebra

1. **Do the `{caname}` paths exist on any firmware?** Both `PUT` and `DELETE`
   return 404 on 5.0.7. If the collection form is correct, the spec should
   document it; if `{caname}` is planned, it should be marked as such.

2. **The `name` field description is inverted.** It says "Required for MQTT API,
   ignored for local REST" — but local REST requires it and ignores the path
   parameter. It should also be in the `required` array alongside `content`.

3. **`DELETE` needs a request body.** The spec documents none. Please document
   `{"name": "…"}` and note that the key is `name`, not `caname`.

4. **The `.crt` suffix breaks list-then-delete.** `GET` returns
   `lab-rfid-ca.crt`; `DELETE` rejects that and requires `lab-rfid-ca`. Either
   accept both forms, or return the name without the suffix.

5. **Replace the example certificate.** The current `content` value fails base64
   decoding and `openssl x509`. The reader rejects it with `INVALID CA
   CERTIFICATE CONTENT`, so the documented example cannot work.
   **A working replacement is provided** in
   [`example-ca/`](example-ca/) — a genuine 10-year root CA
   (`CN = Zebra Example Root CA`), with
   [`example-ca/spec-example.yaml`](example-ca/spec-example.yaml) ready to paste
   into the spec. Verified on this reader: installs 200, lists, deletes clean.

6. **The `GET` example format.** `["AmazonRootCA1", "broker.emqx.io-ca"]` shows
   names without extensions; the reader returns them with `.crt`.

---

## Reader state after testing

| | Before | After |
|---|---|---|
| `GET /cloud/caCertificates` | `[]` | **`[]`** ✅ |

Every certificate installed during testing was deleted. The reader is back to no
CA certificates installed, verified by read-back.

---

## Folder contents

```
cloud-caCertificates/
├── CA_CERTIFICATES_TEST_REPORT.md            ← this file
├── 01-GET-list-SUCCESS/
├── 02-PUT-caname-path-404/                   documented path, 404
├── 03-PUT-collection-spec-example-REJECTED/  spec's fake cert, 422
├── 04-PUT-collection-real-CA-SUCCESS/        real CA, 200
├── 05-DELETE-caname-path-404/                documented path, 404
└── 06-DELETE-collection-SUCCESS/             working form, 200
```

Each holds `request body/request.json` and `response body/` with the verbatim
response and `http_status.txt`. Successful `PUT`/`DELETE` calls return HTTP 200
with an empty body, stored as a 0-byte `response.txt`.

The real CA used for tests 04 and 06 is the lab root at `../../ca/ca.crt`
(`CN = Local RFID Test CA`, valid to 2031).

[`example-ca/`](example-ca/) holds a **purpose-built replacement for the spec's
broken example** — `CN = Zebra Example Root CA`, valid to 2036, verified through
a full install/list/delete cycle on this reader. No private key is included in
either case.
