# Overview

This REST API controls Zebra **FXR** RFID readers. FXR documentation includes **FXR60** and **FXR90**.

Use it to run inventory, set operating mode, configure network and certificates, manage firmware and user applications, and read status, GPIO, and logs.

Send each request to the reader. At the top of this page, replace `YOUR_READER_IP` with the reader IP address or hostname.

## Authentication

1. Open **Authorize** and enter the reader admin credentials under **basicAuth**.
2. Call `GET /cloud/localRestLogin` and copy the token from `message`.
3. Open **Authorize** again, paste the token under **bearerAuth**, and use it for all other `/cloud/*` calls.

If you already have a token from the reader dashboard, skip to step 3.
