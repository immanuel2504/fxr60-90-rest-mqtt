# MQTT `command` issues

**Date:** 26 August 2026

Compared:

| File | What we used |
|---|---|
| `rest/openAPISpec 10.yaml` | `MQTT API :-` line (command the REST spec says to send) |
| `mqtt/openapi_md.json` | JSON `command` enum (schema) |
| `mqtt/examples/*/request/*.json` | `command` in copied examples |

MQTT only works if JSON **`command`** is the exact string the reader expects.

`command_id` is only a request ticket. It does not select the API.

```json
{
  "command": "get_certificates",
  "command_id": "req-get-certs",
  "payload": {}
}
```

Excel: [MQTT-command-issues_2026-08-26.xlsx](MQTT-command-issues_2026-08-26.xlsx)

**Status: applied 26 August 2026.** MQTT `command` (enum, examples, and MQTT Command docs) follows `MQTT API :-` from `openAPISpec 10.yaml`, except GET display: the firmware Display table and MQTT JSON use `get_displayConfig`. `openAPISpec 10.yaml` still has `get_displayCOnfig` and was not edited. Folder names were left unchanged.

The tables below are the original issue list (kept for history). All of those rows are fixed.

---

## A. Schema and examples both use the wrong `command` (6)

If firmware follows the REST description, these MQTT calls fail today.

| REST path | REST says send | MQTT currently sends |
|---|---|---|
| PUT `/cloud/apps/install` | `set_installUserapp` | `install_user_app` |
| PUT `/cloud/apps/{appname}/start` | `set_startUserapp` | `start_user_app` |
| PUT `/cloud/apps/{appname}/stop` | `set_stopUserapp` | `stop_user_app` |
| PUT `/cloud/apps/{appname}/autostart` | `set_autostartUserapp` | `autostart_user_app` |
| PUT `/cloud/apps/{appname}/uninstall` | `set_uninstallUserapp` | `uninstall-user-app` |
| PUT `/cloud/apps/{appname}/pass-through` | `set_reqToUserapp` | `set_req_usr_app` |

---

## B. Schema `command` is correct; examples still send the old folder name (14)

Copying the MQTT example will send the wrong `command`.

| REST path | Correct `command` | Example currently sends |
|---|---|---|
| GET `/cloud/certificates` | `get_certificates` | `get_certs` |
| DELETE `/cloud/certificates/{certname}` | `del_certificate` | `del_certs` |
| PUT `/cloud/certificates/{certname}` | `set_refreshCertificate` | `refresh-cert` |
| GET `/cloud/apps` | `get_userapps` | `get_user_apps` |
| PUT `/cloud/caCertificates/{caname}` | `set_InstallCACertificate` | `set_installCACertificate` |
| GET `/cloud/gpi` | `get_gpiStatus` | `get_gpi_status` |
| GET `/cloud/gpo` | `get_gpoStatus` | `get_gpostatus` |
| DELETE `/cloud/logs/syslog` | `del_logs_syslog` | `del_syslogs` |
| GET `/cloud/logs/RcLog` | `get_logs_rcLog` | `get_rc_log` |
| GET `/cloud/logs/RgErrorLog` | `get_logs_rgErrorLog` | `get_rg_error_logs` |
| GET `/cloud/logs/RgWarningLog` | `get_logs_rgWarningLog` | `get_rg_warn_logs` |
| GET `/cloud/logs/radioPacketLog` | `get_logs_radioPacketLog` | `get_radio_pkt_logs` |
| DELETE `/cloud/logs/radioPacketLog` | `del_logs_radioPacketLog` | `del_radio_pkt_logs` |
| PUT `/cloud/revertbackOS` | `set_revertbackOS` | `revertback` |

---

## C. Casing only (5)

The reader may reject these if `command` is case-sensitive.

| REST path | REST says | MQTT `command` |
|---|---|---|
| GET `/cloud/displayConfig` | `get_displayCOnfig` (typo in `openAPISpec 10.yaml`) | `get_displayConfig` (firmware Display table and MQTT JSON `command`) |
| GET `/cloud/hostName` | `get_hostName` | `get_hostname` |
| PUT `/cloud/hostName` | `set_hostName` | `set_hostname` |
| GET `/cloud/supportedRegionList` | `get_SupportedRegionList` | `get_supportedRegionList` |
| GET `/cloud/supportedStandardList` | `get_SupportedStandardList` | `get_supportedStandardList` |

---

## Not an issue

`PUT /cloud/certificates` — REST documents both names: `set_updateCertificate (set_update_cert)`. MQTT enum, examples, and MQTT Command now use the primary name `set_updateCertificate`.

---

## Count

| Group | How many |
|---|---:|
| A — schema + example wrong | 6 |
| B — example wrong | 14 |
| C — casing | 5 |
| **Total** | **25** |
