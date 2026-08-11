# REST ↔ MQTT example map (full pack)

Auto-generated from `grok-examples/` + `mqtt/openapi_md.json`.

| REST file | MQTT file | Kind |
|---|---|---|
| `cloud-mode/GET/default_configured_only.json` | `get_mode/request/default_configured_only.json` | request payload |
| `cloud-mode/GET/verbose_full.json` | `get_mode/request/verbose_full.json` | request payload |
| `cloud-mode/GET/inline.json` | `get_mode/response/inline.json` | response payload |
| `cloud-mode/GET/SIMPLE.json` | `get_mode/response/SIMPLE.json` | response payload |
| `cloud-mode/GET/INVENTORY.json` | `get_mode/response/INVENTORY.json` | response payload |
| `cloud-mode/GET/PORTAL.json` | `get_mode/response/PORTAL.json` | response payload |
| `cloud-mode/PUT/mode.json` | `set_mode/request/mode.json` | request payload |
| `cloud-mode/PUT/mode_default_FXR90.json` | `set_mode/request/mode_default_FXR90.json` | request payload |
| `cloud-mode/PUT/mode_TAG_FOCUS.json` | `set_mode/request/mode_TAG_FOCUS.json` | request payload |
| `cloud-mode/PUT/mode_INVENTORY.json` | `set_mode/request/mode_INVENTORY.json` | request payload |
| `cloud-mode/PUT/mode_PORTAL.json` | `set_mode/request/mode_PORTAL.json` | request payload |
| `cloud-mode/PUT/mode_CONVEYOR.json` | `set_mode/request/mode_CONVEYOR.json` | request payload |
| `cloud-mode/PUT/mode_SIMPLE_minimal.json` | `set_mode/request/mode_SIMPLE_minimal.json` | request payload |
| `—` | `set_mode/response/success.json` | synthetic success |
| `cloud-start/PUT/start_Inventory.json` | `start/request/start_Inventory.json` | request payload |
| `cloud-start/PUT/start_Inventory_with_AutoStart.json` | `start/request/start_Inventory with AutoStart.json` | request payload |
| `cloud-start/PUT/start_Inventory_with_ImpinjGen2X.json` | `start/request/start_Inventory with ImpinjGen2X.json` | request payload |
| `cloud-start/PUT/start_BLE_only.json` | `start/request/start_BLE_only.json` | request payload |
| `cloud-start/PUT/start_RFID_only.json` | `start/request/start_RFID_only.json` | request payload |
| `cloud-start/PUT/start_BLE_and_RFID.json` | `start/request/start_BLE_and_RFID.json` | request payload |
| `—` | `start/response/success.json` | synthetic success |
| `cloud-stop/PUT/stop_RFID_default.json` | `stop/request/stop_RFID_default.json` | request payload |
| `cloud-stop/PUT/stop_RFID_explicit.json` | `stop/request/stop_RFID_explicit.json` | request payload |
| `cloud-stop/PUT/stop_BLE_only.json` | `stop/request/stop_BLE_only.json` | request payload |
| `cloud-stop/PUT/stop_BLE_and_RFID.json` | `stop/request/stop_BLE_and_RFID.json` | request payload |
| `—` | `stop/response/success.json` | synthetic success |
| `—` | `get_preSelection/request/default.json` | synthetic empty request |
| `cloud-preselection/GET/pre_selection.json` | `get_preSelection/response/pre_selection.json` | response payload |
| `cloud-preselection/PUT/preSelection.json` | `set_preSelection/request/preSelection.json` | request payload |
| `cloud-preselection/PUT/enable_preSelection.json` | `set_preSelection/request/enable_preSelection.json` | request payload |
| `cloud-preselection/PUT/disable_preSelection.json` | `set_preSelection/request/disable_preSelection.json` | request payload |
| `—` | `set_preSelection/response/success.json` | synthetic success |
| `—` | `get_impinjGen2X/request/default.json` | synthetic empty request |
| `cloud-impinjgen2x/GET/empty.json` | `get_impinjGen2X/response/empty.json` | response payload |
| `cloud-impinjgen2x/GET/fastID_configured.json` | `get_impinjGen2X/response/fastID_configured.json` | response payload |
| `cloud-impinjgen2x/GET/tagFocus_configured.json` | `get_impinjGen2X/response/tagFocus_configured.json` | response payload |
| `cloud-impinjgen2x/GET/tagProtect_configured.json` | `get_impinjGen2X/response/tagProtect_configured.json` | response payload |
| `cloud-impinjgen2x/GET/tagQuieting_basic_configured.json` | `get_impinjGen2X/response/tagQuieting_basic_configured.json` | response payload |
| `cloud-impinjgen2x/GET/tagQuieting_advanced_configured.json` | `get_impinjGen2X/response/tagQuieting_advanced_configured.json` | response payload |
| `cloud-impinjgen2x/PUT/enable_fastID.json` | `set_impinjGen2X/request/enable_fastID.json` | request payload |
| `cloud-impinjgen2x/PUT/disable_fastID.json` | `set_impinjGen2X/request/disable_fastID.json` | request payload |
| `cloud-impinjgen2x/PUT/protect_tag.json` | `set_impinjGen2X/request/protect_tag.json` | request payload |
| `cloud-impinjgen2x/PUT/unprotect_tag.json` | `set_impinjGen2X/request/unprotect_tag.json` | request payload |
| `cloud-impinjgen2x/PUT/enable_protect_read.json` | `set_impinjGen2X/request/enable_protect_read.json` | request payload |
| `cloud-impinjgen2x/PUT/disable_protect_read.json` | `set_impinjGen2X/request/disable_protect_read.json` | request payload |
| `cloud-impinjgen2x/PUT/enable_tagFocus.json` | `set_impinjGen2X/request/enable_tagFocus.json` | request payload |
| `cloud-impinjgen2x/PUT/disable_tagFocus.json` | `set_impinjGen2X/request/disable_tagFocus.json` | request payload |
| `cloud-impinjgen2x/PUT/quiet_tags.json` | `set_impinjGen2X/request/quiet_tags.json` | request payload |
| `cloud-impinjgen2x/PUT/unquiet_tags.json` | `set_impinjGen2X/request/unquiet_tags.json` | request payload |
| `cloud-impinjgen2x/PUT/advanced_quiet_tags.json` | `set_impinjGen2X/request/advanced_quiet_tags.json` | request payload |
| `cloud-impinjgen2x/PUT/advanced_unquiet_tags.json` | `set_impinjGen2X/request/advanced_unquiet_tags.json` | request payload |
| `—` | `set_impinjGen2X/response/success.json` | synthetic success |
| `—` | `get_version/request/default.json` | synthetic empty request |
| `cloud-version/GET/inline.json` | `get_version/response/inline.json` | response payload |
| `—` | `get_status/request/default.json` | synthetic empty request |
| `cloud-status/GET/inline.json` | `get_status/response/inline.json` | response payload |
| `cloud-status/GET/running.json` | `get_status/response/running.json` | response payload |
| `—` | `get_config/request/default.json` | synthetic empty request |
| `cloud-config/GET/inline.json` | `get_config/response/inline.json` | response payload |
| `cloud-config/GET/gpio_led_not_configured.json` | `get_config/response/gpio_led_not_configured.json` | response payload |
| `cloud-config/PUT/config_data_mqtt_async.json` | `set_config/request/config_data_mqtt_async.json` | request payload |
| `cloud-config/PUT/config_data_aws.json` | `set_config/request/config_data_aws.json` | request payload |
| `cloud-config/PUT/config_data_azure_mqtt.json` | `set_config/request/config_data_azure_mqtt.json` | request payload |
| `cloud-config/PUT/config_data_clear.json` | `set_config/request/config_data_clear.json` | request payload |
| `cloud-config/PUT/config_data_httpPost.json` | `set_config/request/config_data_httpPost.json` | request payload |
| `cloud-config/PUT/config_data_mqtt.json` | `set_config/request/config_data_mqtt.json` | request payload |
| `cloud-config/PUT/config_data_tcp_ip.json` | `set_config/request/config_data_tcp_ip.json` | request payload |
| `cloud-config/PUT/config_data_websocket.json` | `set_config/request/config_data_websocket.json` | request payload |
| `cloud-config/PUT/config_global_batching.json` | `set_config/request/config_global_batching.json` | request payload |
| `cloud-config/PUT/config_global_retention.json` | `set_config/request/config_global_retention.json` | request payload |
| `cloud-config/PUT/config_management_events.json` | `set_config/request/config_management_events.json` | request payload |
| `cloud-config/PUT/config_gpio_led.json` | `set_config/request/config_gpio_led.json` | request payload |
| `—` | `set_config/response/success.json` | synthetic success |
| `cloud-pass-through/PUT/passthru.json` | `set_passthru/request/passthru.json` | request payload |
| `cloud-pass-through/PUT/status.json` | `set_passthru/request/status.json` | request payload |
| `cloud-pass-through/PUT/passthru_version.json` | `set_passthru/request/passthru_version.json` | request payload |
| `cloud-pass-through/PUT/rc_status.json` | `set_passthru/response/rc_status.json` | response payload |
| `cloud-cloudconfig/PUT/importCloudConfig.json` | `set_importCloudConfig/request/importCloudConfig.json` | request payload |
| `cloud-cloudconfig/PUT/importCloudConfig_mqtt.json` | `set_importCloudConfig/request/importCloudConfig_mqtt.json` | request payload |
| `cloud-cloudconfig/PUT/importCloudConfig_aws.json` | `set_importCloudConfig/request/importCloudConfig_aws.json` | request payload |
| `cloud-cloudconfig/PUT/importCloudConfig_azure.json` | `set_importCloudConfig/request/importCloudConfig_azure.json` | request payload |
| `cloud-cloudconfig/PUT/importCloudConfig_httpPost.json` | `set_importCloudConfig/request/importCloudConfig_httpPost.json` | request payload |
| `—` | `set_importCloudConfig/response/success.json` | synthetic success |
| `—` | `get_readerCapabilities/request/default.json` | synthetic empty request |
| `cloud-readercapabilities/GET/inline.json` | `get_readerCapabilities/response/inline.json` | response payload |
| `—` | `get_cableLossCompensation/request/default.json` | synthetic empty request |
| `cloud-cablelosscompensation/GET/inline.json` | `get_cableLossCompensation/response/inline.json` | response payload |
| `cloud-cablelosscompensation/PUT/cableLossCompensation.json` | `set_cableLossCompensation/request/cableLossCompensation.json` | request payload |
| `cloud-cablelosscompensation/PUT/cableLoss_single_port.json` | `set_cableLossCompensation/request/cableLoss_single_port.json` | request payload |
| `—` | `set_cableLossCompensation/response/success.json` | synthetic success |
| `cloud-reboot/PUT/success.json` | `reboot/response/success.json` | response payload |
| `cloud-updatepassword/PUT/password.json` | `set_password/request/password.json` | request payload |
| `cloud-updatepassword/PUT/password_rfidadm.json` | `set_password/request/password_rfidadm.json` | request payload |
| `—` | `set_password/response/success.json` | synthetic success |
| `—` | `get_hostname/request/default.json` | synthetic empty request |
| `cloud-hostname/GET/configured.json` | `get_hostname/response/configured.json` | response payload |
| `cloud-hostname/PUT/hostName.json` | `set_hostname/request/hostName.json` | request payload |
| `cloud-hostname/PUT/hostName_lab.json` | `set_hostname/request/hostName_lab.json` | request payload |
| `—` | `set_hostname/response/success.json` | synthetic success |
| `—` | `get_appled/request/default.json` | synthetic empty request |
| `cloud-app-led/GET/default_state.json` | `get_appled/response/default_state.json` | response payload |
| `cloud-app-led/GET/overridden_state.json` | `get_appled/response/overridden_state.json` | response payload |
| `cloud-app-led/PUT/app_led.json` | `set_appled/request/app_led.json` | request payload |
| `—` | `set_appled/response/success.json` | synthetic success |
| `—` | `get_gpostatus/request/default.json` | synthetic empty request |
| `cloud-gpo/GET/gpo_status.json` | `get_gpostatus/response/gpo_status.json` | response payload |
| `cloud-gpo/PUT/gpo.json` | `set_gpo/request/gpo.json` | request payload |
| `cloud-gpo/PUT/gpo_port1_high.json` | `set_gpo/request/gpo_port1_high.json` | request payload |
| `cloud-gpo/PUT/gpo_port3_low.json` | `set_gpo/request/gpo_port3_low.json` | request payload |
| `—` | `set_gpo/response/success.json` | synthetic success |
| `—` | `get_gpi_status/request/default.json` | synthetic empty request |
| `cloud-gpi/GET/gpi_status.json` | `get_gpi_status/response/gpi_status.json` | response payload |
| `—` | `get_region/request/default.json` | synthetic empty request |
| `cloud-region/GET/multiple_values.json` | `get_region/response/multiple_values.json` | response payload |
| `cloud-region/GET/india.json` | `get_region/response/india.json` | response payload |
| `cloud-region/PUT/region.json` | `set_region/request/region.json` | request payload |
| `cloud-region/PUT/region_india.json` | `set_region/request/region_india.json` | request payload |
| `cloud-region/PUT/region_usa.json` | `set_region/request/region_usa.json` | request payload |
| `—` | `set_region/response/success.json` | synthetic success |
| `—` | `get_SupportedRegionList/request/default.json` | synthetic empty request |
| `cloud-supportedregionlist/GET/inline.json` | `get_SupportedRegionList/response/inline.json` | response payload |
| `—` | `get_supportedStandardList/request/default.json` | synthetic empty request |
| `cloud-supportedstandardlist/GET/inline.json` | `get_supportedStandardList/response/inline.json` | response payload |
| `—` | `get_logs/request/default.json` | synthetic empty request |
| `cloud-logs/GET/inline.json` | `get_logs/response/inline.json` | response payload |
| `cloud-logs/PUT/logs.json` | `set_logs/request/logs.json` | request payload |
| `cloud-logs/PUT/logs_debug_all.json` | `set_logs/request/logs_debug_all.json` | request payload |
| `cloud-logs/PUT/logs_back_to_info.json` | `set_logs/request/logs_back_to_info.json` | request payload |
| `—` | `set_logs/response/success.json` | synthetic success |
| `—` | `get_logs_syslog/request/default.json` | synthetic empty request |
| `cloud-logs-syslog/GET/download.json` | `get_logs_syslog/response/download.json` | response payload |
| `—` | `del_syslogs/request/default.json` | synthetic empty request |
| `cloud-logs-syslog/GET/download.json` | `del_syslogs/response/download.json` | response payload |
| `—` | `get_rc_log/request/default.json` | synthetic empty request |
| `cloud-logs-rclog/GET/download.json` | `get_rc_log/response/download.json` | response payload |
| `—` | `get_rg_warn_logs/request/default.json` | synthetic empty request |
| `cloud-logs-rgwarninglog/GET/download.json` | `get_rg_warn_logs/response/download.json` | response payload |
| `—` | `get_rg_error_logs/request/default.json` | synthetic empty request |
| `cloud-logs-rgerrorlog/GET/download.json` | `get_rg_error_logs/response/download.json` | response payload |
| `—` | `get_radio_pkt_logs/request/default.json` | synthetic empty request |
| `cloud-logs-radiopacketlog/GET/download.json` | `get_radio_pkt_logs/response/download.json` | response payload |
| `—` | `del_radio_pkt_logs/request/default.json` | synthetic empty request |
| `cloud-logs-radiopacketlog/GET/download.json` | `del_radio_pkt_logs/response/download.json` | response payload |
| `—` | `get_timeZone/request/default.json` | synthetic empty request |
| `cloud-timezone/GET/time_zone.json` | `get_timeZone/response/time_zone.json` | response payload |
| `cloud-timezone/PUT/timeZone.json` | `set_timeZone/request/timeZone.json` | request payload |
| `cloud-timezone/PUT/timeZone_utc.json` | `set_timeZone/request/timeZone_utc.json` | request payload |
| `cloud-timezone/PUT/timeZone_kolkata_short.json` | `set_timeZone/request/timeZone_kolkata_short.json` | request payload |
| `—` | `set_timeZone/response/success.json` | synthetic success |
| `—` | `get_ntpServer/request/default.json` | synthetic empty request |
| `cloud-ntpserver/GET/ntp_server.json` | `get_ntpServer/response/ntp_server.json` | response payload |
| `cloud-ntpserver/PUT/ntpServer.json` | `set_ntpServer/request/ntpServer.json` | request payload |
| `cloud-ntpserver/PUT/ntpServer_legacy.json` | `set_ntpServer/request/ntpServer_legacy.json` | request payload |
| `cloud-ntpserver/PUT/ntpServer_single.json` | `set_ntpServer/request/ntpServer_single.json` | request payload |
| `—` | `set_ntpServer/response/success.json` | synthetic success |
| `—` | `get_certs/request/default.json` | synthetic empty request |
| `cloud-certificates/GET/installed.json` | `get_certs/response/installed.json` | response payload |
| `cloud-certificates/GET/none_installed.json` | `get_certs/response/none_installed.json` | response payload |
| `cloud-certificates-certname/PUT/refreshCertificate_server.json` | `del_certs/request/refreshCertificate_server.json` | request payload |
| `cloud-certificates-certname/PUT/refreshCertificate_client.json` | `del_certs/request/refreshCertificate_client.json` | request payload |
| `—` | `del_certs/response/success.json` | synthetic success |
| `cloud-certificates/PUT/updateCertificate.json` | `set_update_cert/request/updateCertificate.json` | request payload |
| `cloud-certificates/PUT/updateCertificate_client.json` | `set_update_cert/request/updateCertificate_client.json` | request payload |
| `cloud-certificates/PUT/updateCertificate_app.json` | `set_update_cert/request/updateCertificate_app.json` | request payload |
| `cloud-certificates/PUT/updateCertificate_inline_pem.json` | `set_update_cert/request/updateCertificate_inline_pem.json` | request payload |
| `—` | `set_update_cert/response/success.json` | synthetic success |
| `cloud-certificates-certname/PUT/refreshCertificate_server.json` | `refresh-cert/request/refreshCertificate_server.json` | request payload |
| `cloud-certificates-certname/PUT/refreshCertificate_client.json` | `refresh-cert/request/refreshCertificate_client.json` | request payload |
| `—` | `refresh-cert/response/success.json` | synthetic success |
| `—` | `get_CACertificates/request/default.json` | synthetic empty request |
| `cloud-cacertificates/GET/CACertificates.json` | `get_CACertificates/response/CACertificates.json` | response payload |
| `cloud-cacertificates-caname/PUT/InstallCACertificate.json` | `set_installCACertificate/request/InstallCACertificate.json` | request payload |
| `cloud-cacertificates-caname/PUT/InstallCACertificate_named.json` | `set_installCACertificate/request/InstallCACertificate_named.json` | request payload |
| `—` | `set_installCACertificate/response/success.json` | synthetic success |
| `cloud-cacertificates-caname/PUT/InstallCACertificate.json` | `del_CACertificate/request/InstallCACertificate.json` | request payload |
| `cloud-cacertificates-caname/PUT/InstallCACertificate_named.json` | `del_CACertificate/request/InstallCACertificate_named.json` | request payload |
| `—` | `del_CACertificate/response/success.json` | synthetic success |
| `—` | `get_network/request/default.json` | synthetic empty request |
| `cloud-network/GET/Ethernet.json` | `get_network/response/Ethernet.json` | response payload |
| `cloud-network/GET/WiFi.json` | `get_network/response/WiFi.json` | response payload |
| `cloud-network/GET/Bluetooth.json` | `get_network/response/Bluetooth.json` | response payload |
| `cloud-network/GET/WAN.json` | `get_network/response/WAN.json` | response payload |
| `cloud-network/GET/Hotspot.json` | `get_network/response/Hotspot.json` | response payload |
| `cloud-network/PUT/Network_ethernet_dhcp.json` | `set_network/request/Network_ethernet_dhcp.json` | request payload |
| `cloud-network/PUT/Network_ethernet_static.json` | `set_network/request/Network_ethernet_static.json` | request payload |
| `cloud-network/PUT/Network_ethernet_static_8021x_tls.json` | `set_network/request/Network_ethernet_static_8021x_tls.json` | request payload |
| `cloud-network/PUT/Network_ethernet_dhcp_8021x_tls.json` | `set_network/request/Network_ethernet_dhcp_8021x_tls.json` | request payload |
| `cloud-network/PUT/Network_ethernet_dhcp_8021x_ttls_mschapv2.json` | `set_network/request/Network_ethernet_dhcp_8021x_ttls_mschapv2.json` | request payload |
| `cloud-network/PUT/Network_ethernet_dhcp_8021x_peap_mschapv2.json` | `set_network/request/Network_ethernet_dhcp_8021x_peap_mschapv2.json` | request payload |
| `cloud-network/PUT/Network_wifi_static.json` | `set_network/request/Network_wifi_static.json` | request payload |
| `cloud-network/PUT/Network_wifi_dhcp.json` | `set_network/request/Network_wifi_dhcp.json` | request payload |
| `cloud-network/PUT/Network_wifi_security_wpa2_personal.json` | `set_network/request/Network_wifi_security_wpa2_personal.json` | request payload |
| `cloud-network/PUT/Network_wifi_wpa2_enterprise_tls.json` | `set_network/request/Network_wifi_wpa2_enterprise_tls.json` | request payload |
| `cloud-network/PUT/Network_wifi_wpa3_enterprise_ttls_mschapv2.json` | `set_network/request/Network_wifi_wpa3_enterprise_ttls_mschapv2.json` | request payload |
| `cloud-network/PUT/Network_wifi_wpa2_enterprise_peap_tls.json` | `set_network/request/Network_wifi_wpa2_enterprise_peap_tls.json` | request payload |
| `cloud-network/PUT/Network_wifi_wpa2_enterprise_ttls_tls.json` | `set_network/request/Network_wifi_wpa2_enterprise_ttls_tls.json` | request payload |
| `cloud-network/PUT/Network_wifi_wpa3_enterprise_peap_mschapv2.json` | `set_network/request/Network_wifi_wpa3_enterprise_peap_mschapv2.json` | request payload |
| `cloud-network/PUT/Network_bluetooth.json` | `set_network/request/Network_bluetooth.json` | request payload |
| `cloud-network/PUT/Network_wan.json` | `set_network/request/Network_wan.json` | request payload |
| `cloud-network/PUT/Network_hotspot.json` | `set_network/request/Network_hotspot.json` | request payload |
| `—` | `set_network/response/success.json` | synthetic success |
| `—` | `get_availableWifiNetworks/request/default.json` | synthetic empty request |
| `cloud-wifinetworks/GET/inline.json` | `get_availableWifiNetworks/response/inline.json` | response payload |
| `—` | `get_networkInterfaces/request/default.json` | synthetic empty request |
| `cloud-networkinterfaces/GET/application_json.json` | `get_networkInterfaces/response/application/json.json` | response payload |
| `—` | `get_readPoints/request/default.json` | synthetic empty request |
| `cloud-readpoints/GET/inline.json` | `get_readPoints/response/inline.json` | response payload |
| `—` | `get_gpsCoordinates/request/default.json` | synthetic empty request |
| `cloud-readerlocation/GET/fix_acquired.json` | `get_gpsCoordinates/response/fix_acquired.json` | response payload |
| `cloud-readerlocation/GET/no_fix.json` | `get_gpsCoordinates/response/no_fix.json` | response payload |
| `—` | `get_eSimConfig/request/default.json` | synthetic empty request |
| `cloud-esimconfig/GET/profiles_present.json` | `get_eSimConfig/response/profiles_present.json` | response payload |
| `cloud-esimconfig/GET/no_profiles.json` | `get_eSimConfig/response/no_profiles.json` | response payload |
| `cloud-esimconfig/PUT/eSimConfig_enable.json` | `set_eSimConfig/request/eSimConfig_enable.json` | request payload |
| `cloud-esimconfig/PUT/eSimConfig_add.json` | `set_eSimConfig/request/eSimConfig_add.json` | request payload |
| `cloud-esimconfig/PUT/eSimConfig_delete.json` | `set_eSimConfig/request/eSimConfig_delete.json` | request payload |
| `—` | `set_eSimConfig/response/success.json` | synthetic success |
| `cloud-os/PUT/os.json` | `set_os/request/os.json` | request payload |
| `cloud-os/PUT/os_basic_auth.json` | `set_os/request/os_basic_auth.json` | request payload |
| `cloud-os/PUT/os_scp.json` | `set_os/request/os_scp.json` | request payload |
| `cloud-os/PUT/os_https_pinned_ca.json` | `set_os/request/os_https_pinned_ca.json` | request payload |
| `—` | `set_os/response/success.json` | synthetic success |
| `cloud-revertbackos/PUT/revertbackOS.json` | `revertback/request/revertbackOS.json` | request payload |
| `—` | `revertback/response/success.json` | synthetic success |
| `cloud-apps-install/PUT/installUserapp.json` | `install_user_app/request/installUserapp.json` | request payload |
| `cloud-apps-install/PUT/installUserapp_no_auth.json` | `install_user_app/request/installUserapp_no_auth.json` | request payload |
| `cloud-apps-install/PUT/installUserapp_pinned_ca.json` | `install_user_app/request/installUserapp_pinned_ca.json` | request payload |
| `—` | `install_user_app/response/success.json` | synthetic success |
| `cloud-apps-appname-start/PUT/startUserapp.json` | `start_user_app/request/startUserapp.json` | request payload |
| `cloud-apps-appname-start/PUT/success.json` | `start_user_app/response/success.json` | response payload |
| `cloud-apps-appname-stop/PUT/stopUserapp.json` | `stop_user_app/request/stopUserapp.json` | request payload |
| `cloud-apps-appname-stop/PUT/success.json` | `stop_user_app/response/success.json` | response payload |
| `cloud-apps-appname-autostart/PUT/autostartUserapp.json` | `autostart_user_app/request/autostartUserapp.json` | request payload |
| `cloud-apps-appname-autostart/PUT/autostartUserapp-false.json` | `autostart_user_app/request/autostartUserapp-false.json` | request payload |
| `—` | `autostart_user_app/response/success.json` | synthetic success |
| `—` | `get_user_apps/request/default.json` | synthetic empty request |
| `cloud-apps/GET/inline.json` | `get_user_apps/response/inline.json` | response payload |
| `cloud-setdatatorg/PUT/dataToRG.json` | `set_dataToRG/request/dataToRG.json` | request payload |
| `—` | `set_dataToRG/response/success.json` | synthetic success |
| `cloud-apps-appname-pass-through/PUT/reqToUserapp.json` | `set_req_usr_app/request/reqToUserapp.json` | request payload |
| `cloud-apps-appname-pass-through/PUT/reqToUserapp_command.json` | `set_req_usr_app/request/reqToUserapp_command.json` | request payload |
| `cloud-apps-appname-pass-through/PUT/reqToUserapp_reload.json` | `set_req_usr_app/request/reqToUserapp_reload.json` | request payload |
| `cloud-apps-appname-pass-through/PUT/app_reply.json` | `set_req_usr_app/response/app_reply.json` | response payload |
| `cloud-apps-appname-uninstall/PUT/uninstallUserapp.json` | `uninstall-user-app/request/uninstallUserapp.json` | request payload |
| `cloud-apps-appname-uninstall/PUT/success.json` | `uninstall-user-app/response/success.json` | response payload |
| `—` | `get_bleConfig/request/default.json` | synthetic empty request |
| `cloud-bleconfig/GET/inline.json` | `get_bleConfig/response/inline.json` | response payload |
| `cloud-bleconfig/GET/disabled.json` | `get_bleConfig/response/disabled.json` | response payload |
| `cloud-bleconfig/PUT/enable_ble.json` | `set_bleConfig/request/enable_ble.json` | request payload |
| `cloud-bleconfig/PUT/enable_with_interval.json` | `set_bleConfig/request/enable_with_interval.json` | request payload |
| `cloud-bleconfig/PUT/enable_with_rssi_filter.json` | `set_bleConfig/request/enable_with_rssi_filter.json` | request payload |
| `cloud-bleconfig/PUT/enable_with_protocols.json` | `set_bleConfig/request/enable_with_protocols.json` | request payload |
| `cloud-bleconfig/PUT/disable_ble.json` | `set_bleConfig/request/disable_ble.json` | request payload |
| `—` | `set_bleConfig/response/success.json` | synthetic success |

