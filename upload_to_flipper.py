#!/usr/bin/env python3
"""
NullSec Flipper Zero Suite Uploader
Uploads all assets to Flipper via serial
"""

import serial
import time
import os
import sys

class FlipperUploader:
    def __init__(self, port='/dev/ttyACM0', baud=230400):
        self.port = port
        self.baud = baud
        self.serial = None
        
    def connect(self):
        try:
            self.serial = serial.Serial(self.port, self.baud, timeout=2)
            time.sleep(0.5)
            self.serial.read(self.serial.in_waiting)
            print(f"[✓] Connected to Flipper on {self.port}")
            return True
        except Exception as e:
            print(f"[✗] Connection failed: {e}")
            return False
    
    def send_command(self, cmd, wait=0.5):
        if not self.serial:
            return None
        self.serial.write(f"{cmd}\r\n".encode())
        time.sleep(wait)
        response = self.serial.read(self.serial.in_waiting).decode(errors='ignore')
        return response
    
    def mkdir(self, path):
        return self.send_command(f"storage mkdir {path}")
    
    def write_file(self, remote_path, local_path):
        """Write a file to Flipper via CLI"""
        with open(local_path, 'rb') as f:
            data = f.read()
        
        # For text files, use storage write
        self.send_command(f"storage remove {remote_path}", wait=0.2)
        
        # Write in chunks
        chunk_size = 200
        self.send_command(f"storage write {remote_path}", wait=0.1)
        
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i+chunk_size]
            self.serial.write(chunk)
            time.sleep(0.05)
        
        self.serial.write(b'\x03')  # Ctrl+C to end
        time.sleep(0.2)
        return True
    
    def upload_directory(self, local_dir, remote_dir):
        """Upload entire directory structure"""
        print(f"\n[*] Uploading {local_dir} -> {remote_dir}")
        
        self.mkdir(remote_dir)
        
        for root, dirs, files in os.walk(local_dir):
            rel_path = os.path.relpath(root, local_dir)
            if rel_path == '.':
                remote_subdir = remote_dir
            else:
                remote_subdir = f"{remote_dir}/{rel_path}"
                self.mkdir(remote_subdir)
            
            for file in files:
                if file.endswith(('.py', '.pyc', '.sh')):
                    continue
                local_path = os.path.join(root, file)
                remote_path = f"{remote_subdir}/{file}"
                print(f"  -> {file}")
                self.write_file(remote_path, local_path)
    
    def disconnect(self):
        if self.serial:
            self.serial.close()
            print("[✓] Disconnected")

def main():
    base_dir = "/home/antics/nullsec/flipper-zero"
    
    print("\n╔═══════════════════════════════════════════════╗")
    print("║     NullSec Flipper Suite Uploader            ║")
    print("╚═══════════════════════════════════════════════╝\n")
    
    uploader = FlipperUploader()
    
    if not uploader.connect():
        print("Make sure Flipper is connected and no other app is using it")
        sys.exit(1)
    
    # Create NullSec directories
    print("[*] Creating NullSec directories...")
    uploader.mkdir("/ext/nullsec")
    uploader.mkdir("/ext/nullsec/badusb")
    uploader.mkdir("/ext/nullsec/subghz")
    uploader.mkdir("/ext/nullsec/infrared")
    uploader.mkdir("/ext/nullsec/nfc")
    
    # Upload content
    uploads = [
        (f"{base_dir}/apps/badusb", "/ext/nullsec/badusb"),
        (f"{base_dir}/apps/subghz", "/ext/nullsec/subghz"),
        (f"{base_dir}/apps/infrared", "/ext/nullsec/infrared"),
    ]
    
    for local, remote in uploads:
        if os.path.exists(local):
            uploader.upload_directory(local, remote)
    
    # Upload animations as asset pack
    print("\n[*] Uploading animation pack...")
    uploader.mkdir("/ext/asset_packs/NullSec")
    uploader.mkdir("/ext/asset_packs/NullSec/Anims")
    
    anim_dir = f"{base_dir}/assets/animations"
    for anim in os.listdir(anim_dir):
        anim_path = os.path.join(anim_dir, anim)
        if os.path.isdir(anim_path) and anim.endswith("_128x64"):
            remote_anim = f"/ext/asset_packs/NullSec/Anims/{anim}"
            uploader.mkdir(remote_anim)
            for f in os.listdir(anim_path):
                if f.endswith('.bm') or f == 'meta.txt':
                    local_file = os.path.join(anim_path, f)
                    remote_file = f"{remote_anim}/{f}"
                    print(f"  -> {anim}/{f}")
                    uploader.write_file(remote_file, local_file)
    
    uploader.disconnect()
    print("\n[✓] Upload complete!")
    print("    Go to Momentum Settings > Protocols > Asset Packs")
    print("    Select 'NullSec' to activate the theme\n")

if __name__ == "__main__":
    main()
