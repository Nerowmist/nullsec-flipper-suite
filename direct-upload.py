#!/usr/bin/env python3
"""
NullSec Flipper Zero Suite - Direct Upload via Serial CLI
Uploads all content directly to Flipper Zero SD card
"""

import serial
import time
import os
import sys
from pathlib import Path

class FlipperUploader:
    def __init__(self, port="/dev/ttyACM0", baud=230400):
        self.port = port
        self.baud = baud
        self.ser = None
        
    def connect(self):
        """Connect to Flipper Zero"""
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=1)
            time.sleep(0.5)
            # Exit any running app and get to CLI
            self.ser.write(b'\x03')  # Ctrl+C
            time.sleep(0.3)
            self.ser.read(self.ser.in_waiting)
            print(f"[+] Connected to Flipper on {self.port}")
            return True
        except Exception as e:
            print(f"[-] Failed to connect: {e}")
            return False
    
    def send_command(self, cmd, wait=0.5):
        """Send command and get response"""
        if not self.ser:
            return None
        self.ser.write(f"{cmd}\r\n".encode())
        time.sleep(wait)
        response = self.ser.read(self.ser.in_waiting).decode('utf-8', errors='ignore')
        return response
    
    def mkdir(self, path):
        """Create directory on Flipper"""
        response = self.send_command(f"storage mkdir {path}")
        return "exists" in response.lower() or ">:" in response
    
    def upload_file(self, local_path, remote_path):
        """Upload a file to Flipper"""
        try:
            with open(local_path, 'rb') as f:
                data = f.read()
            
            # Use storage write command
            self.send_command(f"storage remove {remote_path}", wait=0.2)
            self.send_command(f"storage write {remote_path}", wait=0.1)
            
            # Send data in chunks
            chunk_size = 512
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i+chunk_size]
                self.ser.write(chunk)
                time.sleep(0.05)
            
            self.ser.write(b'\x03')  # End write
            time.sleep(0.2)
            return True
        except Exception as e:
            print(f"[-] Upload failed for {local_path}: {e}")
            return False
    
    def upload_text_file(self, local_path, remote_path):
        """Upload text file line by line"""
        try:
            with open(local_path, 'r') as f:
                content = f.read()
            
            # Remove existing file
            self.send_command(f"storage remove {remote_path}", wait=0.2)
            
            # Write new file
            cmd = f'storage write_chunk {remote_path} {len(content)}'
            self.ser.write(f"{cmd}\r\n".encode())
            time.sleep(0.1)
            self.ser.write(content.encode())
            time.sleep(0.3)
            
            return True
        except Exception as e:
            print(f"[-] Upload failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from Flipper"""
        if self.ser:
            self.ser.close()
            print("[+] Disconnected")

def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║     _   _       _ _ ____                                  ║
║    | \\ | |_   _| | / ___|  ___  ___                       ║
║    |  \\| | | | | | \\___ \\ / _ \\/ __|                      ║
║    | |\\  | |_| | | |___) |  __/ (__                       ║
║    |_| \\_|\\__,_|_|_|____/ \\___|\\___| FLIPPER              ║
║                                                           ║
║            Direct Upload Script v1.0                      ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    suite_dir = Path("/home/antics/nullsec/flipper-zero")
    
    uploader = FlipperUploader()
    if not uploader.connect():
        print("[-] Could not connect to Flipper Zero")
        print("[*] Falling back to file copy method...")
        sys.exit(1)
    
    # Create directories
    print("[*] Creating directories...")
    dirs = [
        "/ext/badusb/nullsec",
        "/ext/subghz/nullsec", 
        "/ext/infrared/nullsec",
        "/ext/nfc/nullsec",
        "/ext/lfrfid/nullsec",
        "/ext/ibutton/nullsec",
        "/ext/music_player/nullsec",
        "/ext/dolphin/asset_packs/NullSec",
        "/ext/dolphin/asset_packs/NullSec/Anims",
        "/ext/dolphin/asset_packs/NullSec/Icons"
    ]
    
    for d in dirs:
        uploader.mkdir(d)
        print(f"  [+] {d}")
    
    # Upload mappings
    uploads = [
        ("badusb/nullsec", "/ext/badusb/nullsec"),
        ("subghz/nullsec", "/ext/subghz/nullsec"),
        ("infrared/nullsec", "/ext/infrared/nullsec"),
        ("nfc/nullsec", "/ext/nfc/nullsec"),
        ("rfid/nullsec", "/ext/lfrfid/nullsec"),
        ("ibutton/nullsec", "/ext/ibutton/nullsec"),
        ("music_player/nullsec", "/ext/music_player/nullsec"),
    ]
    
    total_files = 0
    for local_dir, remote_dir in uploads:
        local_path = suite_dir / local_dir
        if local_path.exists():
            for f in local_path.iterdir():
                if f.is_file():
                    remote_path = f"{remote_dir}/{f.name}"
                    print(f"  [*] Uploading {f.name}...", end=" ")
                    if uploader.upload_text_file(str(f), remote_path):
                        print("OK")
                        total_files += 1
                    else:
                        print("FAIL")
    
    print(f"\n[+] Uploaded {total_files} files to Flipper Zero!")
    uploader.disconnect()

if __name__ == "__main__":
    main()
