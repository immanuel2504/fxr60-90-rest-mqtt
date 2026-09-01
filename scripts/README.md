# Live API tests moved

All live REST and MQTT testers now live in **`test script/`**.

```powershell
cd "test script"
py -3 -m pip install -r requirements.txt
py -3 test_rest_api.py --only "/cloud/status"
py -3 test_mqtt_api.py --only get_status
```

See `test script/README.md`.
