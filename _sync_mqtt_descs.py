from collections import OrderedDict
from pathlib import Path
import json
import re

ROOT = Path(".")
MQTT = ROOT / "mqtt" / "openapi_md.json"

COMMAND_SWAPS = [
    ("GET /cloud/impinjGen2X", "get_impinjGen2X"),
    ("PUT /cloud/impinjGen2X", "set_impinjGen2X"),
    ("GET /cloud/bleConfig", "get_bleConfig"),
    ("PUT /cloud/bleConfig", "set_bleConfig"),
    ("GET /cloud/preSelection", "get_preSelection"),
    ("PUT /cloud/preSelection", "set_preSelection"),
    ("GET /cloud/mode", "get_mode"),
    ("PUT /cloud/mode", "set_mode"),
    ("PUT /cloud/start", "start"),
    ("PUT /cloud/stop", "stop"),
    ("GET /cloud/config", "get_config"),
    ("PUT /cloud/config", "set_config"),
    ("PUT /cloud/pass-through", "set_passthru"),
    ("PUT /cloud/cloudConfig", "set_importCloudConfig"),
    ("PUT /cloud/reboot", "reboot"),
    ("PUT /cloud/updatePassword", "set_password"),
    ("GET /cloud/hostName", "get_hostName"),
    ("PUT /cloud/hostName", "set_hostName"),
    ("GET /cloud/app-led", "get_appled"),
    ("PUT /cloud/app-led", "set_appled"),
    ("GET /cloud/stack-led", "get_stackled"),
    ("PUT /cloud/stack-led", "set_stackled"),
    ("GET /cloud/displayConfig", "get_displayConfig"),
    ("PUT /cloud/displayConfig", "set_displayConfig"),
    ("GET /cloud/inputOutputDevices", "get_inputOutputDevices"),
    ("GET /cloud/gpo", "get_gpoStatus"),
    ("PUT /cloud/gpo", "set_gpo"),
    ("GET /cloud/gpi", "get_gpiStatus"),
    ("PUT /cloud/apps/{appname}/pass-through", "set_reqToUserapp"),
    ("PUT /cloud/apps/{appname}/autostart", "set_autostartUserapp"),
    ("PUT /cloud/apps/{appname}/uninstall", "set_uninstallUserapp"),
    ("PUT /cloud/apps/{appname}/start", "set_startUserapp"),
    ("PUT /cloud/apps/{appname}/stop", "set_stopUserapp"),
    ("PUT /cloud/apps/install", "set_installUserapp"),
    ("GET /cloud/apps", "get_userapps"),
    ("PUT /cloud/setdataToRG", "set_dataToRG"),
    ("PUT /cloud/os", "set_os"),
    ("PUT /cloud/revertbackOS", "set_revertbackOS"),
    ("GET /cloud/wifiNetworks", "get_availableWifiNetworks"),
    ("GET /cloud/networkInterfaces", "get_networkInterfaces"),
    ("GET /cloud/network", "get_network"),
    ("PUT /cloud/network", "set_network"),
    ("GET /cloud/readPoints", "get_readPoints"),
    ("GET /cloud/readerLocation", "get_gpsCoordinates"),
    ("GET /cloud/eSimConfig", "get_eSimConfig"),
    ("PUT /cloud/eSimConfig", "set_eSimConfig"),
    ("GET /cloud/cableLossCompensation", "get_cableLossCompensation"),
    ("PUT /cloud/cableLossCompensation", "set_cableLossCompensation"),
    ("GET /cloud/readerCapabilities", "get_readerCapabilities"),
    ("DELETE /cloud/certificates/{certname}", "del_certificate"),
    ("PUT /cloud/certificates/{certname}", "set_refreshCertificate"),
    ("PUT /cloud/certificates", "set_updateCertificate"),
    ("GET /cloud/certificates", "get_certificates"),
    ("GET /cloud/caCertificates", "get_CACertificates"),
    ("PUT /cloud/caCertificates", "set_InstallCACertificate"),
    ("DELETE /cloud/caCertificates", "del_CACertificate"),
    ("GET /cloud/status", "get_status"),
    ("GET /cloud/version", "get_version"),
    ("GET /cloud/region", "get_region"),
    ("PUT /cloud/region", "set_region"),
    ("GET /cloud/supportedRegionList", "get_supportedRegionList"),
    ("GET /cloud/supportedStandardList", "get_supportedStandardList"),
    ("GET /cloud/logs/radioPacketLog", "get_logs_radioPacketLog"),
    ("DELETE /cloud/logs/radioPacketLog", "del_logs_radioPacketLog"),
    ("GET /cloud/logs/RgWarningLog", "get_logs_rgWarningLog"),
    ("GET /cloud/logs/RgErrorLog", "get_logs_rgErrorLog"),
    ("GET /cloud/logs/syslog", "get_logs_syslog"),
    ("DELETE /cloud/logs/syslog", "del_logs_syslog"),
    ("GET /cloud/logs/RcLog", "get_logs_rcLog"),
    ("PUT /cloud/logs", "set_logs"),
    ("GET /cloud/logs", "get_logs"),
    ("GET /cloud/timeZone", "get_timeZone"),
    ("PUT /cloud/timeZone", "set_timeZone"),
    ("GET /cloud/ntpServer", "get_ntpServer"),
    ("PUT /cloud/ntpServer", "set_ntpServer"),
]


def rest_md(name: str) -> str:
    return (ROOT / "rest" / "operation_descriptions" / name).read_text(encoding="utf-8")


def rest_to_mqtt(md: str) -> str:
    lines = []
    for line in md.splitlines(keepends=True):
        if line.startswith("| REST Endpoint |"):
            lines.append(line)
            continue
        text = line
        text = text.replace("When to Use This Endpoint", "When to Use This Command")
        text = text.replace("Endpoint Details", "Command Details")
        text = text.replace("This endpoint", "This command")
        text = text.replace("this endpoint", "this command")
        text = text.replace("Use this endpoint", "Use this command")
        text = text.replace("sending this request", "sending this command")
        text = text.replace("REST endpoint", "command")
        text = text.replace(
            "| Communication Type | Client to Device (HTTP request/response) |",
            "| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |",
        )
        text = text.replace(
            "| HTTPS connectivity | The reader's HTTPS endpoint must be reachable and a valid bearer token must be included in the `Authorization` header of every request. |",
            "| MQTT connectivity | A connected MQTT session to the reader command topic is required. |",
        )
        for rest, mqtt in COMMAND_SWAPS:
            text = text.replace(f"`{rest}`", f"`{mqtt}`")
        lines.append(text)
    out = "".join(lines)
    out = re.sub(
        r"\n\| Authentication \| Bearer token \(`Authorization: Bearer <token>`\) \|\n",
        "\n",
        out,
    )
    return out


def main():
    data = json.loads(MQTT.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    paths = data["paths"]

    def mqtt_cert_path_op(md: str) -> str:
        text = rest_to_mqtt(md)
        text = text.replace("| Path Parameter | `certname` |\n", "")
        text = text.replace(
            "| Required Request Fields | `type` |",
            "| Required Payload Fields | `name`, `type` |",
        )
        text = text.replace(
            "| `certname` | Certificate `name` in the URL path. |",
            "| `name` | Certificate name in the payload. |",
        )
        text = text.replace(
            "- `{certname}` — certificate `name` in the URL\n",
            "- `name` — certificate name\n",
        )
        return text

    def mqtt_app_path_op(md: str) -> str:
        text = rest_to_mqtt(md)
        text = text.replace("| Path Parameter | `appname` |\n", "")
        text = text.replace(
            "| Request Body | None |\n",
            "| Required Payload Fields | `appname` |\n",
        )
        text = text.replace(
            "| Required Request Fields | `autostart` |",
            "| Required Payload Fields | `appname`, `autostart` |",
        )
        text = text.replace(
            "| `appname` | Installed name from `get_userapps`. URL path. |",
            "| `appname` | Installed name from `get_userapps`. Payload. |",
        )
        text = text.replace(
            "- `{appname}` — installed name in the URL\n",
            "- `appname` — installed name\n",
        )
        return text

    def mqtt_passthru_op(md: str) -> str:
        text = rest_to_mqtt(md)
        text = text.replace("| Path Parameter | `appname` |\n", "")
        text = text.replace(
            "| Required Request Fields | `userapp` |",
            "| Required Payload Fields | `userapp` |",
        )
        text = text.replace(
            "| `appname` | Installed name from `get_userapps`. URL path. |\n",
            "",
        )
        text = text.replace(
            "- `{appname}` — installed name in the URL\n",
            "",
        )
        text = text.replace(
            "- `userapp` — same installed name in the JSON body\n",
            "- `userapp` — installed name\n",
        )
        return text

    control = [
        ("getMode.md", "/get_mode"),
        ("setMode.md", "/set_mode"),
        ("startInventory.md", "/start"),
        ("stopInventory.md", "/stop"),
        ("getPreSelection.md", "/get_preSelection"),
        ("setPreSelection.md", "/set_preSelection"),
        ("getImpinjGen2X.md", "/get_impinjGen2X"),
        ("setImpinjGen2X.md", "/set_impinjGen2X"),
        ("getStatus.md", "/get_status"),
        ("getConfig.md", "/get_config"),
        ("setConfigMqtt.md", "/set_config"),
        ("setPassthru.md", "/set_passthru"),
        ("setImportcloudconfig.md", "/set_importCloudConfig"),
        ("getReadercapabilities.md", "/get_readerCapabilities"),
        ("getCablelosscompensation.md", "/get_cableLossCompensation"),
        ("setCablelosscompensation.md", "/set_cableLossCompensation"),
        ("getAvailablewifinetworks.md", "/get_availableWifiNetworks"),
        ("getNetworkinterfaces.md", "/get_networkInterfaces"),
        ("getNetwork.md", "/get_network"),
        ("updateNetwork.md", "/set_network"),
        ("getReadpoints.md", "/get_readPoints"),
        ("getGpsCoordinates.md", "/get_gpsCoordinates"),
        ("getEsimConfig.md", "/get_eSimConfig"),
        ("setEsimConfig.md", "/set_eSimConfig"),
        ("setOs.md", "/set_os"),
        ("setRevertbackos.md", "/revertback"),
        ("reboot.md", "/reboot"),
        ("updatePassword.md", "/set_password"),
        ("getHostName.md", "/get_hostname"),
        ("setHostName.md", "/set_hostname"),
        ("getAppled.md", "/get_appled"),
        ("setAppled.md", "/set_appled"),
        ("getStackled.md", "/get_stackled"),
        ("setStackled.md", "/set_stackled"),
        ("getDisplayConfig.md", "/get_displayConfig"),
        ("setDisplayConfig.md", "/set_displayConfig"),
        ("getInputOutputDevices.md", "/get_inputOutputDevices"),
        ("getGpoStatus.md", "/get_gpostatus"),
        ("setGpo.md", "/set_gpo"),
        ("getGPIStatus.md", "/get_gpi_status"),
        ("getRegion.md", "/get_region"),
        ("setRegion.md", "/set_region"),
        ("getSupportedregionlist.md", "/get_supportedRegionList"),
        ("getSupportedstandardlist.md", "/get_supportedStandardList"),
        ("getLogs.md", "/get_logs"),
        ("setLogs.md", "/set_logs"),
        ("getLogsSyslog.md", "/get_logs_syslog"),
        ("delLogsSyslog.md", "/del_syslogs"),
        ("getRcLog.md", "/get_rc_log"),
        ("getRgWarningLog.md", "/get_rg_warn_logs"),
        ("getRgErrorLog.md", "/get_rg_error_logs"),
        ("getRadioPacketLog.md", "/get_radio_pkt_logs"),
        ("delRadioPacketLog.md", "/del_radio_pkt_logs"),
        ("getTimezone.md", "/get_timeZone"),
        ("setTimezone.md", "/set_timeZone"),
        ("getNtpServer.md", "/get_ntpServer"),
        ("updateNtpServer.md", "/set_ntpServer"),
        ("getCertificates.md", "/get_certs"),
        ("setUpdatecertificate.md", "/set_update_cert"),
        ("getCACertificates.md", "/get_CACertificates"),
        ("setInstallCACertificate.md", "/set_installCACertificate"),
        ("delCACertificate.md", "/del_CACertificate"),
        ("getUserapps.md", "/get_user_apps"),
        ("setInstalluserapp.md", "/install_user_app"),
        ("setDataToRG.md", "/set_dataToRG"),
        ("getBleConfig.md", "/get_bleConfig"),
        ("setBleConfig.md", "/set_bleConfig"),
    ]
    for md_name, path in control:
        paths[path]["post"]["description"] = rest_to_mqtt(rest_md(md_name))

    paths["/del_certs"]["post"]["description"] = mqtt_cert_path_op(rest_md("delCertificate.md"))
    paths["/refresh-cert"]["post"]["description"] = mqtt_cert_path_op(
        rest_md("setRefreshcertificate.md")
    )
    paths["/start_user_app"]["post"]["description"] = mqtt_app_path_op(
        rest_md("setStartuserapp.md")
    )
    paths["/stop_user_app"]["post"]["description"] = mqtt_app_path_op(
        rest_md("setStopuserapp.md")
    )
    paths["/autostart_user_app"]["post"]["description"] = mqtt_app_path_op(
        rest_md("setAutostartuserapp.md")
    )
    paths["/uninstall-user-app"]["post"]["description"] = mqtt_app_path_op(
        rest_md("setUninstalluserapp.md")
    )
    paths["/set_req_usr_app"]["post"]["description"] = mqtt_passthru_op(
        rest_md("setReqtouserapp.md")
    )

    MQTT.write_text(json.dumps(data, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
    print("updated mqtt descriptions")


if __name__ == "__main__":
    main()
