# Bluetooth PAN (`bnep0`) — how to reach the reader without Ethernet or Wi-Fi

**Interface:** `bnep0`  
**REST:** `GET /cloud/network` and `PUT /cloud/network`  
**MQTT:** `get_network` / `set_network`  
**Applies to:** FXR60 and FXR90

Bluetooth PAN is a **management path**. A person stands next to the reader with a laptop or phone, pairs over Bluetooth, and opens the reader in a browser or REST client. It is **not** used to read RFID tags or scan BLE beacons (that is `GET`/`PUT /cloud/bleConfig`).

Ethernet (`eth0`) and Wi-Fi client (`mlan0`) remain the normal day-to-day paths. Use `bnep0` when those are not available yet, or when they have failed.

---

## Live capture (FXR60 `FXR609BE34A`)

PUT body sent (same as [PUT/Network_bluetooth.json](PUT/Network_bluetooth.json)):

```json
{
  "bnep0": {
    "dhcpEndAddress": "192.168.0.10",
    "dhcpStartAddress": "192.168.0.2",
    "discoverable": true,
    "pairable": true,
    "passKey": "1233",
    "usePassKey": false,
    "enable": true
  }
}
```

GET `{ "interface": "bnep0" }` after that PUT (same as [GET/Bluetooth.json](GET/Bluetooth.json)):

```json
{
  "hostName": "FXR609BE34A",
  "networkInterface": {
    "bnep0": {
      "Status": "active",
      "deviceDiscoverableName": "FXR609BE34A",
      "dhcpEndAddress": "192.168.0.10",
      "dhcpStartAddress": "192.168.0.2",
      "ipAddress": "192.168.227.74",
      "isDiscoverable": true,
      "isEnabled": true,
      "isPairable": true,
      "macAddress": "90:75:DE:14:FC:FB",
      "passKey": "1233",
      "subnetMask": "255.255.0.0",
      "usePassKey": false
    }
  }
}
```

What this means on this reader:

| You see | Meaning |
|---|---|
| `Status: "active"` and `isEnabled: true` | Bluetooth PAN is on |
| `deviceDiscoverableName: "FXR609BE34A"` | Name to tap in the phone/laptop Bluetooth list |
| `usePassKey: false` | Pairing does **not** ask for PIN `1233` |
| `ipAddress: "192.168.227.74"` | Open **`https://192.168.227.74`** after you pair |
| Laptop will get | An address in `192.168.0.2`–`192.168.0.10` — that is the laptop, not the reader |

PUT succeeded: GET echoed the same pool, PIN, and flags. The two GET bodies above are the same capture twice.

---

## When to use it

| Situation | Why Bluetooth |
|---|---|
| Reader just unboxed | No cable, no Wi-Fi configured yet |
| Mounted on a door or portal, Ethernet not pulled | Installer commissions it from a laptop a few metres away |
| Ethernet or Wi-Fi is down | Field tech pairs, checks status, fixes network, leaves |

When Ethernet or Wi-Fi works, use that instead. Turn pairing off so random phones cannot connect.

---

## What it is (one picture)

```
Your laptop  ---- Bluetooth ----  Reader FXR609BE34A
  gets 192.168.0.2 … 192.168.0.10    ipAddress 192.168.227.74
```

- The **reader** gives the laptop an address from `dhcpStartAddress`–`dhcpEndAddress`.
- You open **the reader’s** `ipAddress` in the browser (`https://192.168.227.74`), not the laptop’s address.

This is the opposite of Ethernet DHCP, where the LAN gives the **reader** an IP.

There is no cable, no `IPV4`/`IPV6` block, and no 802.1X on `bnep0`.

---

## Procedure

### 1. Turn Bluetooth PAN on (on the reader)

If the reader already appears in a Bluetooth scan, skip this step.

If you already have *any* path to the reader (Ethernet, Wi-Fi, or factory default), send **one interface per request**:

```http
PUT /cloud/network
Authorization: Bearer <token>
Content-Type: application/json
```

Use the live body in [Live capture](#live-capture-fxr60-fxr609be34a). Success body is an empty string (`""`). Confirm with GET.

| PUT field | Meaning |
|---|---|
| `enable` | Bluetooth network on or off |
| `discoverable` | Visible in a phone or laptop Bluetooth scan |
| `pairable` | Accept new pairings |
| `usePassKey` | `true` = require the PIN. Live capture used `false` (no PIN prompt) |
| `passKey` | PIN (send the field even when `usePassKey` is `false`) |
| `dhcpStartAddress` / `dhcpEndAddress` | Address pool for **the laptop**, not the building LAN |

All of those PUT fields are required in the spec.

### 2. Pair from the laptop or phone

Stand next to the reader (Bluetooth range).

1. Open Bluetooth settings.
2. Scan for devices.
3. Tap **`FXR609BE34A`** (`deviceDiscoverableName`).
4. Because `usePassKey` is `false` on this reader, it should **not** ask for `1233`. If a PIN appears, enter `1233`.
5. Wait until it says **Connected**.

The laptop is now on a small private network that the reader is serving.

### 3. Get the address to open in the browser

On this live reader the address is already known from GET: **`192.168.227.74`**.

**Way A — you already have Ethernet or Wi-Fi to the reader**

```http
GET /cloud/network
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{ "interface": "bnep0" }
```

Copy `networkInterface.bnep0.ipAddress`. Open `https://<that ipAddress>`.

**Way B — Bluetooth only (no cable, no Wi-Fi)**

After pairing, on the laptop:

1. Open Command Prompt.
2. Run `ipconfig`.
3. Find the adapter that appeared after pairing (often a Bluetooth or Ethernet adapter with a `192.168.x.x` address).
4. Read **Default Gateway** — expect **`192.168.227.74`** on this reader.

The laptop address in `192.168.0.2`–`192.168.0.10` is **you**. Do not put that in the browser.

### 4. Log in and do the real work

1. Open `https://192.168.227.74`.
2. Log in as admin (or call `GET /cloud/localRestLogin` with HTTP Basic, then use the bearer token).
3. Configure what you came for: Wi-Fi (`mlan0`), hostname, region, and so on.

### 5. Confirm PAN is up

Healthy GET on this reader:

| Field | This reader |
|---|---|
| `Status` | `active` |
| `isEnabled` | `true` |
| `isDiscoverable` | `true` |
| `isPairable` | `true` |
| `ipAddress` | `192.168.227.74` |

GET uses different names than PUT: `isEnabled` / `isDiscoverable` / `isPairable` (PUT uses `enable` / `discoverable` / `pairable`). `ipAddress`, `subnetMask`, `macAddress`, `Status`, and `deviceDiscoverableName` are GET-only.

### 6. Finish and walk away

When Ethernet or Wi-Fi works, use that path. Optionally stop new pairings:

```json
{
  "bnep0": {
    "dhcpStartAddress": "192.168.0.2",
    "dhcpEndAddress": "192.168.0.10",
    "discoverable": false,
    "pairable": false,
    "passKey": "1233",
    "usePassKey": false,
    "enable": false
  }
}
```

`enable: false` turns the Bluetooth **network** off. It does not change BLE tag scanning (`/cloud/bleConfig`).

---

## PUT vs GET field names

| Intent | PUT (write) | GET (read) |
|---|---|---|
| On? | `enable` | `isEnabled` |
| Visible in scan? | `discoverable` | `isDiscoverable` |
| Allow new pairings? | `pairable` | `isPairable` |
| Reader PAN IP | — | `ipAddress` |

---

## Not this interface

| You want | Use |
|---|---|
| Wired LAN | `eth0` on `/cloud/network` |
| Join site Wi-Fi | `mlan0` on `/cloud/network` |
| Scan iBeacon / BLE tags | `/cloud/bleConfig` (and GET `blescan` on `/cloud/network`) |

---

## Related examples

| File | What it is |
|---|---|
| [PUT/Network_bluetooth.json](PUT/Network_bluetooth.json) | Enable Bluetooth PAN (this live PUT) |
| [GET/request_bnep0.json](GET/request_bnep0.json) | GET filter `{ "interface": "bnep0" }` |
| [GET/Bluetooth.json](GET/Bluetooth.json) | Live GET response from `FXR609BE34A` |
