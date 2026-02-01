#!/usr/bin/env python3
"""
NullSec Flipper Zero - Storage CLI Upload
Uses the Flipper's built-in storage CLI commands
"""

import serial
import time
import os
import sys
import base64
from pathlib import Path

SUITE_DIR = Path("/home/antics/nullsec/flipper-zero")
FLIPPER_PORT = "/dev/ttyACM0"

def flipper_cmd(ser, cmd, wait=0.3):
    """Send command to Flipper and get response"""
    # Clear any pending data
    ser.reset_input_buffer()
    
    # Send command
    ser.write(f"{cmd}\r".encode())
    time.sleep(wait)
    
    # Read response
    response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
    return response

def storage_mkdir(ser, path):
    """Create directory on Flipper"""
    return flipper_cmd(ser, f"storage mkdir {path}")

def storage_write(ser, remote_path, data):
    """Write file to Flipper storage using storage write"""
    # Remove existing file first
    flipper_cmd(ser, f"storage remove {remote_path}", 0.1)
    
    # Use storage write with data
    # The Flipper CLI expects: storage write <path>
    # Then you can send data and end with Ctrl+C
    
    # For text files, we can use storage write directly
    ser.write(f"storage write {remote_path}\r".encode())
    time.sleep(0.1)
    ser.write(data)
    time.sleep(0.1)
    ser.write(b'\x03')  # Ctrl+C to end
    time.sleep(0.2)
    return ser.read(ser.in_waiting)

def upload_file(ser, local_path, remote_path):
    """Upload a single file to Flipper"""
    try:
        with open(local_path, 'rb') as f:
            data = f.read()
        
        storage_write(ser, remote_path, data)
        return True
    except Exception as e:
        print(f"  [-] Error: {e}")
        return False

def upload_directory(ser, local_dir, remote_base, category):
    """Upload all files from a directory"""
    local_path = Path(local_dir)
    
    if not local_path.exists():
        print(f"[-] Not found: {local_dir}")
        return 0
    
    files = list(local_path.glob('*'))
    print(f"[*] Uploading {len(files)} {category} files...")
    
    # Create remote directory
    storage_mkdir(ser, remote_base)
    
    count = 0
    for item in files:
        if item.is_file():
            remote_path = f"{remote_base}/{item.name}"
            print(f"    {item.name}", end=" ")
            if upload_file(ser, str(item), remote_path):
                print("✓")
                count += 1
            else:
                print("✗")
    
    return count

def main():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║   _   _       _ _ ____             _____ _ _                  ║
║  | \ | |_   _| | / ___|  ___  ___ |  ___| (_)_ __  _ __   ___ ║
║  |  \| | | | | | \___ \ / _ \/ __|| |_  | | | '_ \| '_ \ / _ \\║
║  | |\  | |_| | | |___) |  __/ (__ |  _| | | | |_) | |_) |  __/║
║  |_| \_|\__,_|_|_|____/ \___|\___||_|   |_|_| .__/| .__/ \___|║
║                                             |_|   |_|         ║
║                  Flipper Zero Suite Uploader                  ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Connect to Flipper
    print(f"[*] Connecting to Flipper Zero on {FLIPPER_PORT}...")
    try:
        ser = serial.Serial(FLIPPER_PORT, 230400, timeout=1)
        time.sleep(0.5)
        
        # Test connection
        response = flipper_cmd(ser, "device_info", 0.5)
        if "hardware" in response.lower() or "firmware" in response.lower():
            print("[+] Connected to Flipper Zero!")
        else:
            # Try another command
            response = flipper_cmd(ser, "", 0.2)
            print("[+] Flipper Zero detected")
            
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        print("    Make sure qFlipper is closed and Flipper is connected")
        sys.exit(1)
    
    stats = {}
    
    try:
        # Upload BadUSB
        stats['BadUSB'] = upload_directory(
            ser, 
            SUITE_DIR / "badusb/nullsec", 
            "/ext/badusb/nullsec",
            "BadUSB"
        )
        
        # Upload SubGHz
        stats['SubGHz'] = upload_directory(
            ser, 
            SUITE_DIR / "subghz/nullsec", 
            "/ext/subghz/nullsec",
            "SubGHz"
        )
        
        # Upload Infrared
        stats['Infrared'] = upload_directory(
            ser, 
            SUITE_DIR / "infrared/nullsec", 
            "/ext/infrared/nullsec",
            "Infrared"
        )
        
        # Upload NFC
        stats['NFC'] = upload_directory(
            ser, 
            SUITE_DIR / "nfc/nullsec", 
            "/ext/nfc/nullsec",
            "NFC"
        )
        
        # Upload RFID
        stats['RFID'] = upload_directory(
            ser, 
            SUITE_DIR / "rfid/nullsec", 
            "/ext/lfrfid/nullsec",
            "RFID"
        )
        
        # Upload iButton
        stats['iButton'] = upload_directory(
            ser, 
            SUITE_DIR / "ibutton/nullsec", 
            "/ext/ibutton/nullsec",
            "iButton"
        )
        
        # Upload Music
        stats['Music'] = upload_directory(
            ser, 
            SUITE_DIR / "music_player/nullsec", 
            "/ext/music_player/nullsec",
            "Music"
        )
        
        print("\n" + "="*60)
        print("[+] Upload Summary:")
        for cat, count in stats.items():
            print(f"    {cat}: {count} files")
        print("="*60)
        
        print("""
[!] Asset Pack must be uploaded via qFlipper File Manager:
    Copy: asset_pack/NullSec -> /ext/dolphin/asset_packs/

[*] To activate:
    1. Settings > Desktop > Animations
    2. Select "NullSec"
    3. Reboot Flipper
        """)
        
    finally:
        ser.close()

if __name__ == "__main__":
    main()
