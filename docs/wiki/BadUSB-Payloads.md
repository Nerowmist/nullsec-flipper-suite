# BadUSB Payloads

## Overview

80 DuckyScript payloads organized by category for penetration testing and security research.

## Categories

### 🔍 Reconnaissance (10 payloads)
- `recon/system_info.txt` — Enumerate OS, hardware, network
- `recon/wifi_survey.txt` — List nearby WiFi networks
- `recon/installed_apps.txt` — Inventory installed software
- `recon/browser_history.txt` — Extract browsing history
- `recon/network_map.txt` — Map local network topology

### 📤 Exfiltration (10 payloads)
- `exfil/wifi_passwords.txt` — Extract saved WiFi credentials
- `exfil/ssh_keys.txt` — Copy SSH private keys
- `exfil/browser_creds.txt` — Dump browser saved passwords
- `exfil/clipboard_steal.txt` — Capture clipboard contents
- `exfil/discord_tokens.txt` — Extract Discord tokens

### 🔐 Persistence (10 payloads)
- `persist/reverse_shell.txt` — Establish reverse shell
- `persist/scheduled_task.txt` — Create persistent scheduled task
- `persist/startup_entry.txt` — Add to startup programs
- `persist/ssh_backdoor.txt` — Install SSH backdoor
- `persist/cron_persist.txt` — Linux cron job persistence

### 🎭 Social Engineering (10 payloads)
- `social/fake_update.txt` — Display fake update screen
- `social/phish_portal.txt` — Deploy credential capture page

## Writing Custom Payloads

```duckyscript
REM My custom payload
DELAY 1000
GUI r
DELAY 500
STRING powershell
ENTER
DELAY 1000
STRING Write-Output "Hello from NullSec"
ENTER
```

## OS Compatibility

| Payload | Windows | macOS | Linux |
|---------|:-------:|:-----:|:-----:|
| Recon | ✅ | ✅ | ✅ |
| Exfil | ✅ | ✅ | ✅ |
| Persist | ✅ | ⚠️ | ✅ |
| Social | ✅ | ✅ | ❌ |
