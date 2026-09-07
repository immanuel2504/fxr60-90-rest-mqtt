# Firewall rule needed for a reader API test — port 443 inbound

Hi team,

I'm testing the `set_updateCertificate` API on an FXR reader. The test requires my machine (`192.168.1.41`) to temporarily serve a test certificate file over HTTPS so the reader can download it — this is the same mechanism used for real certificate installs (`PUT /cloud/certificates`), just pointed at a local test file instead of a production server.

**What I need:** An inbound firewall rule on `192.168.1.41` allowing TCP port 443, so the reader can reach the test server running on my machine. I don't have admin rights to add this myself.

**Command to run** (PowerShell, as Administrator, on `192.168.1.41`):

```powershell
New-NetFirewallRule -DisplayName "FXR-test-https-443" -Direction Inbound -Protocol TCP -LocalPort 443 -Action Allow -Profile Any
```

**Confirmed so far:**
- The test HTTPS server is already running and verified working locally (`curl` from the same machine gets a `200 OK`).
- No connection attempt from the reader has reached the machine at all — checked the server logs directly, only local test traffic shows up.
- No existing firewall rule permits inbound port 443 — checked with `Get-NetFirewallRule`, confirmed empty.
- Windows Firewall is active on all profiles (Domain/Private/Public), so this is a real block, not a red herring.

**Once the rule is added**, no other change is needed on my end — I'll just resend the same test request.

**Alternative, if adding a firewall rule isn't preferred:** I already have a working path via the lab's existing SFTP server (`10.117.229.15`), which the reader can already reach without any firewall change. If it's simpler, I can place the test file there instead and skip the port 443 request entirely — let me know which you'd prefer.

Thanks!
