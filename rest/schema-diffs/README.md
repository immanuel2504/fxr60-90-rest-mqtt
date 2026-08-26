# Schema difference notes

**Date:** 25 August 2026

One file per operation that still differs between developer firmware spec and the current docs source.

| File | Role |
|---|---|
| `rest/openAPISpec 10.yaml` | Developer spec |
| `rest/RestDeveloperfile.yaml` | Current docs source |

Nothing in these per-endpoint notes has been merged unless a row in [DISCUSS-AND-FINALIZE.md](DISCUSS-AND-FINALIZE.md) is marked **Final**.

**Working session (questions, device tests, keep/align):** [DISCUSS-AND-FINALIZE.md](DISCUSS-AND-FINALIZE.md)

**Overview of the three download APIs** (apps, certificates, OS): [HTTPS-download-control.md](HTTPS-download-control.md)

**Where `type` goes on certificate delete** (query vs body): [DELETE-certificate-type-location.md](DELETE-certificate-type-location.md)

[PUT `/cloud/apps/install`](PUT-cloud-apps-install.md) is the per-endpoint template (runtime, mapping, examples). Certificates and OS use the same download-control pattern.

## Client-breaking (wrong JSON key or location)

| Method | Path | Markdown |
|---|---|---|
| PUT | `/cloud/apps/install` | [PUT-cloud-apps-install.md](PUT-cloud-apps-install.md) |
| PUT | `/cloud/certificates` | [PUT-cloud-certificates.md](PUT-cloud-certificates.md) |
| PUT | `/cloud/os` | [PUT-cloud-os.md](PUT-cloud-os.md) |
| DELETE | `/cloud/certificates/{certname}` | [DELETE-cloud-certificates-certname.md](DELETE-cloud-certificates-certname.md) |
| PUT | `/cloud/network` | [PUT-cloud-network.md](PUT-cloud-network.md) |
| GET | `/cloud/network` | [GET-cloud-network.md](GET-cloud-network.md) |

## New or moved request fields

| Method | Path | Markdown |
|---|---|---|
| GET | `/cloud/config` | [GET-cloud-config.md](GET-cloud-config.md) |
| PUT | `/cloud/config` | [PUT-cloud-config.md](PUT-cloud-config.md) |
| GET | `/cloud/mode` | [GET-cloud-mode.md](GET-cloud-mode.md) |
| PUT | `/cloud/apps/{appname}/start` | [PUT-cloud-apps-appname-start.md](PUT-cloud-apps-appname-start.md) |
| PUT | `/cloud/apps/{appname}/stop` | [PUT-cloud-apps-appname-stop.md](PUT-cloud-apps-appname-stop.md) |
| PUT | `/cloud/apps/{appname}/uninstall` | [PUT-cloud-apps-appname-uninstall.md](PUT-cloud-apps-appname-uninstall.md) |
| PUT | `/cloud/apps/{appname}/pass-through` | [PUT-cloud-apps-appname-pass-through.md](PUT-cloud-apps-appname-pass-through.md) |

## Shape / enum polish (same JSON, tighter FXR docs)

| Method | Path | Markdown |
|---|---|---|
| PUT | `/cloud/mode` | [PUT-cloud-mode.md](PUT-cloud-mode.md) |
| PUT | `/cloud/start` | [PUT-cloud-start.md](PUT-cloud-start.md) |
| PUT | `/cloud/stop` | [PUT-cloud-stop.md](PUT-cloud-stop.md) |
| GET | `/cloud/stack-led` | [GET-cloud-stack-led.md](GET-cloud-stack-led.md) |
| GET | `/cloud/status` | [GET-cloud-status.md](GET-cloud-status.md) |
| GET | `/cloud/version` | [GET-cloud-version.md](GET-cloud-version.md) |
| GET | `/cloud/cableLossCompensation` | [GET-cloud-cableLossCompensation.md](GET-cloud-cableLossCompensation.md) |
| PUT | `/cloud/cableLossCompensation` | [PUT-cloud-cableLossCompensation.md](PUT-cloud-cableLossCompensation.md) |
| PUT | `/cloud/impinjGen2X` | [PUT-cloud-impinjGen2X.md](PUT-cloud-impinjGen2X.md) |
| GET | `/cloud/readerCapabilities` | [GET-cloud-readerCapabilities.md](GET-cloud-readerCapabilities.md) |
