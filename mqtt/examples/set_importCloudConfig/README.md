# `set_importCloudConfig`

REST: `PUT /cloud/cloudConfig` → `cloud-cloudconfig/`

Stable `command_id`: `req-set-importCloudConfig`

| File | Direction | Example | REST source | Summary |
|---|---|---|---|---|
| `request/importCloudConfig.json` | request | `importCloudConfig` | `cloud-cloudconfig/PUT/importCloudConfig.json` |  |
| `request/importCloudConfig_mqtt.json` | request | `importCloudConfig_mqtt` | `cloud-cloudconfig/PUT/importCloudConfig_mqtt.json` | MQTT data plane import |
| `request/importCloudConfig_aws.json` | request | `importCloudConfig_aws` | `cloud-cloudconfig/PUT/importCloudConfig_aws.json` | AWS IoT mqtt-AWS data plane |
| `request/importCloudConfig_azure.json` | request | `importCloudConfig_azure` | `cloud-cloudconfig/PUT/importCloudConfig_azure.json` | Azure IoT Hub mqtt-AZURE data plane |
| `request/importCloudConfig_httpPost.json` | request | `importCloudConfig_httpPost` | `cloud-cloudconfig/PUT/importCloudConfig_httpPost.json` | HTTP POST webhook data plane |
| `response/success.json` | response | `success` | `—` | Command succeeded |

