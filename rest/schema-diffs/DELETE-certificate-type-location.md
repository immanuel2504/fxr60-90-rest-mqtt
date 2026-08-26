# DELETE a certificate — where does `type` go?

**Date:** 25 August 2026

API: `DELETE /cloud/certificates/{certname}` (`delCertificate` / MQTT `del_certificate`)

This is **not** about retry, timeout, or async behaviour. The deletion API is the same. Only the **location** of `type` changed.

Per-endpoint schema note: [DELETE-cloud-certificates-certname.md](DELETE-cloud-certificates-certname.md)

Nothing in this note has been merged into RestDeveloperfile.

**Updated 26 August 2026:** Device test confirms `type` in the request body. Docs aligned. See [DISCUSS-AND-FINALIZE.md](DISCUSS-AND-FINALIZE.md) item 5.

---

## Scenario: you want to delete a certificate from the reader

The reader has certificates:

```
Reader
├── mqtt-client-cert
├── app-cert
└── server-cert
```

You want to delete:

```
mqtt-client-cert
```

The API is:

```
DELETE /cloud/certificates/{certname}
```

So the request targets:

```
DELETE /cloud/certificates/mqtt-client-cert
```

The reader also needs to know:

> What type of certificate is `mqtt-client-cert`?

You need to tell it:

```
type = client
```

This is where the problem occurs.

---

## Your current documentation says one thing

`RestDeveloperfile.yaml` tells the developer:

> Put `type=client` in the URL.

So the developer sends:

```http
DELETE /cloud/certificates/mqtt-client-cert?type=client
```

```
                 URL
                  ↓
DELETE /cloud/certificates/mqtt-client-cert?type=client
                                                ↑
                                             type
```

There is **nothing in the request body**.

---

## The current firmware expects something different

The developer specification says:

> Don't put `type` in the URL. Put it in the request body.

So the correct request is:

```http
DELETE /cloud/certificates/mqtt-client-cert
```

with:

```json
{
  "type": "client"
}
```

```
                 URL
                  ↓
DELETE /cloud/certificates/mqtt-client-cert

                 BODY
                  ↓
          { "type": "client" }
```

---

## What happens inside the reader

### What the firmware expects

The reader receives:

```
DELETE /cloud/certificates/mqtt-client-cert
```

Then it looks inside the body:

```
Body
 ↓
type
 ↓
client
```

Now it knows:

> Okay, delete `mqtt-client-cert`, and it is a client certificate.

Then it can perform the deletion.

---

## What happens if the developer follows the old documentation?

The developer sends:

```
DELETE /cloud/certificates/mqtt-client-cert?type=client
```

The developer thinks:

> I gave the reader `type=client`, so everything is fine.

But the firmware is looking for:

```
Request Body
    ↓
   type
```

Instead, it receives:

```
Request Body
    ↓
   NOTHING
```

The `type` is sitting in:

```
URL Query
    ↓
?type=client
```

So the firmware may say, essentially:

> I was expecting `type` in the request body, but it isn't there.

And the request can fail.

---

## Think about it like sending a parcel

There are two places where you can put information:

### 1. Address on the parcel

```
URL / Query
```

### 2. Letter inside the parcel

```
Request Body
```

**Old documentation** says: put `type=client` on the address.

```
Address:
DELETE /cloud/certificates/mqtt-client-cert?type=client
```

**New firmware** says: I expect `type=client` inside the parcel.

```
Parcel contents:
{
    "type": "client"
}
```

You provided the information, but **you put it in the wrong place**. That is the entire issue.

---

## Why this matters

These two requests look similar:

### Request 1 — old (current docs)

```http
DELETE /cloud/certificates/mqtt-client-cert?type=client
```

### Request 2 — new (firmware / developer spec)

```http
DELETE /cloud/certificates/mqtt-client-cert

{
  "type": "client"
}
```

They are **different API contracts**.

| Request | Where `type` goes |
|---|---|
| Old | Query parameter (`?type=client`) |
| New | Request body (`{ "type": "client" }`) |

---

## Why MQTT makes this clearer

MQTT command: `del_certificate`

MQTT does not use an HTTP URL query like `?type=client`. The message contains data:

```json
{
  "type": "client"
}
```

The developer REST specification aligned the REST request body with the MQTT payload. MQTT has no query string, so the REST body matches the MQTT payload shape.

---

## What about `server`?

You can delete:

```
client
app
```

You **cannot** delete:

```
server
```

### Valid

```json
{ "type": "client" }
```

```json
{ "type": "app" }
```

### Invalid for delete

```json
{ "type": "server" }
```

(Refresh on the same path still allows `server` | `client` | `app` in the body.)

---

## What needs to change in the docs

### Current documentation

```http
DELETE /cloud/certificates/mqtt-client-cert?type=client
```

### New documentation

```http
DELETE /cloud/certificates/mqtt-client-cert
```

Body:

```json
{
  "type": "client"
}
```

---

## The easiest sentence to remember

The certificate deletion API itself has not changed; only the location of the `type` parameter has changed — from the URL query parameter in the old documentation to the JSON request body in the current developer/firmware specification.

Unlike the [three download APIs](HTTPS-download-control.md), this one is not about retry, timeout, or asynchronous behaviour.

It is simply:

**Same information, but put it in the correct place.**
