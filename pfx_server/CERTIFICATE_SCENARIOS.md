# Certificate Installation Scenarios

This guide tests `PUT /cloud/certificates` on the FXR60 reader at
`https://10.233.48.36`.

The certificate source is this Linux host:

```text
https://10.117.229.18
```

`reader-test.pfx` is a password-protected client certificate. Its password is
stored locally in `.credentials` and is read automatically by the scenario
runner.

## Before Running a Scenario

Set the reader REST API token and the certificate file-server token in the
Linux terminal:

```bash
export READER_TOKEN='your-reader-token'
export FILE_TOKEN='your-file-server-token'
```

List available scenarios:

```bash
python3 certificate_scenarios.py --list
```

Run a dry run first. It prints the outgoing request but does not contact the
reader:

```bash
python3 certificate_scenarios.py sync-success
```

Add `--execute` only when ready to send the request to the reader.

## 1. Synchronous Success

Installs `reader-test.pfx` as a client certificate named `scenario-sync`.
The API call waits for the final installation result.

Request body:

```json
{
	"name": "scenario-sync",
	"type": "client",
	"url": "https://10.117.229.18/reader-test.pfx",
	"authenticationType": "NONE",
	"pfxPassword": "<PFX_READER_TEST_PASSWORD>",
	"verifyPeer": false,
	"verifyHost": false,
	"headers": {
		"Authorization": "Bearer <FILE_TOKEN>"
	}
}
```

```bash
python3 certificate_scenarios.py sync-success --execute
```

Expected result: an HTTP 200 reader response and an installed client
certificate named `scenario-sync`.

## 2. Retry Then Success

The file server returns HTTP 500 for the first two download attempts, then
serves the PFX. The request is asynchronous because it includes `retry`.

Request body:

```json
{
	"name": "scenario-retry",
	"type": "client",
	"url": "https://10.117.229.18/fail/2/reader-test.pfx",
	"authenticationType": "NONE",
	"pfxPassword": "<PFX_READER_TEST_PASSWORD>",
	"verifyPeer": false,
	"verifyHost": false,
	"headers": {
		"Authorization": "Bearer <FILE_TOKEN>"
	},
	"retry": {
		"type": "randomWait",
		"policy": {
			"retries": 3,
			"wait": {
				"min": 1,
				"max": 2
			}
		}
	},
	"timeouts": {
		"connection": 5,
		"read": 15
	}
}
```

In terminal one, observe management messages:

```bash
python3 mqtt_test.py --listen-seconds 120
```

In terminal two, submit the scenario:

```bash
python3 certificate_scenarios.py retry-success --execute
```

Expected result: the REST endpoint immediately acknowledges the request. The
final success or failure is published to `fxr60-lab/mevents`.

## 3. Read Timeout

The file server deliberately sends `reader-test.pfx` slowly. The reader uses a
two-second read timeout and one retry. This is asynchronous.

Request body:

```json
{
	"name": "scenario-timeout",
	"type": "client",
	"url": "https://10.117.229.18/slow/30/reader-test.pfx",
	"authenticationType": "NONE",
	"pfxPassword": "<PFX_READER_TEST_PASSWORD>",
	"verifyPeer": false,
	"verifyHost": false,
	"headers": {
		"Authorization": "Bearer <FILE_TOKEN>"
	},
	"retry": {
		"type": "randomWait",
		"policy": {
			"retries": 1,
			"wait": {
				"min": 1,
				"max": 2
			}
		}
	},
	"timeouts": {
		"connection": 5,
		"read": 2
	}
}
```

In terminal one:

```bash
python3 mqtt_test.py --listen-seconds 120
```

In terminal two:

```bash
python3 certificate_scenarios.py read-timeout --execute
```

Expected result: an immediate REST acknowledgment followed by a timeout or
retry failure event on `fxr60-lab/mevents`. No certificate should be installed
under `scenario-timeout`.

## 4. Invalid File-Server Token

The reader receives a deliberately invalid Bearer token for the certificate
source. This scenario is synchronous.

Request body:

```json
{
	"name": "scenario-bad-token",
	"type": "client",
	"url": "https://10.117.229.18/reader-test.pfx",
	"authenticationType": "NONE",
	"pfxPassword": "<PFX_READER_TEST_PASSWORD>",
	"verifyPeer": false,
	"verifyHost": false,
	"headers": {
		"Authorization": "Bearer invalid-token"
	}
}
```

```bash
python3 certificate_scenarios.py bad-file-token --execute
```

Expected result: the reader reports a download authentication failure. No
certificate should be installed under `scenario-bad-token`.

## MQTT Topics

The MQTT broker is `10.117.229.9:1883`.

| Purpose | Topic |
| --- | --- |
| Send management commands | `fxr60-lab/mcmd` |
| Receive command responses | `fxr60-lab/mrsp` |
| Receive management events | `fxr60-lab/mevents` |

`mqtt_test.py` subscribes to the response and event topics by default. It only
publishes when supplied with `--payload path/to/command.json`.