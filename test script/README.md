# Lab tests (REST + MQTT)

Copy this **whole docs repo** to the other PC, then use this folder. The scripts read examples from `mqtt/` and `rest/` next to `test script`.

Default tier is **read** only (GET / `get_*`). Write and danger calls can change the reader.

| File | What it does |
|---|---|
| `test_all_apis.py` | REST, MQTT, or both |
| `test_rest_api.py` | Every REST operation in the YAML spec |
| `test_mqtt_api.py` | Every MQTT command that has a request example |
| `lab_rest.json` | Reader IP, username, password |
| `lab_mqtt.json` | Broker IP and topics |

```powershell
cd "test script"
py -3 -m pip install -r requirements.txt
py -3 test_all_apis.py --list
```

## REST (HTTPS to the reader)

Needs a PC that can open `https://10.233.48.36`.

```powershell
cd "test script"
py -3 test_rest_api.py --only "/cloud/status"
py -3 test_rest_api.py
```

Host and password come from `lab_rest.json`. The script logs in for a fresh token.

## MQTT (through the lab broker)

Needs a PC that can reach `10.117.229.9`.

```powershell
cd "test script"
py -3 test_mqtt_api.py --only get_status
py -3 test_mqtt_api.py
```

| Channel | Command topic (we publish) | Response topic (we listen) |
|---|---|---|
| Management | `fxr60-lab/mcmd` | `fxr60-lab/mrsp` |
| Control | `fxr60-lab/cmd` | `fxr60-lab/rsp` |

Do not publish on `fxr60-lab/tevents` or `fxr60-lab/mevents`. Do not reuse reader client IDs.

## Both

```powershell
cd "test script"
py -3 test_all_apis.py both --only status
```

Reports: `test script/reports/`.

After each run:

| Folder | What goes there |
|---|---|
| `reports/success/` | Tests that **passed** (one `.json` per API/command) |
| `reports/failure/` | Tests that **failed** or **warned** (timeout, HTTP error, schema mismatch, …) |

Each folder also has `_index.md` listing what was saved. The full run summary is still in `reports/api_test_*.md` (REST) or `reports/mqtt_test_*.md` (MQTT).
