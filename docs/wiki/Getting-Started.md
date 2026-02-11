# Getting Started

## Prerequisites

- Flipper Zero with firmware v0.89.0+
- microSD card (recommended 32GB+)
- USB-C cable or qFlipper app

## Installation Methods

### Method 1: qFlipper (Recommended)
```bash
git clone https://github.com/bad-antics/nullsec-flipper-suite
```
1. Connect Flipper via USB
2. Open qFlipper
3. Navigate to SD Card tab
4. Drag & drop desired folders

### Method 2: Direct SD Card Copy
```bash
git clone https://github.com/bad-antics/nullsec-flipper-suite
cd nullsec-flipper-suite

# Copy categories you want
cp -r badusb/nullsec/ /path/to/flipper-sd/badusb/
cp -r subghz/nullsec/ /path/to/flipper-sd/subghz/
cp -r infrared/nullsec/ /path/to/flipper-sd/infrared/
```

### Method 3: Web Installer
Download the latest release ZIP and extract to your Flipper SD card.

## Folder Structure
```
nullsec-flipper-suite/
├── badusb/         # 80 DuckyScript payloads
├── subghz/         # 40 RF signal files
├── infrared/       # 16 IR remote databases
├── nfc/            # NFC card templates
├── rfid/           # RFID card templates
├── ibutton/        # iButton key templates
├── music/          # Speaker tunes
├── animations/     # Custom animations
├── apps/           # App resources
└── assets/         # Icons and graphics
```

## First Steps

1. Start with **BadUSB** → Try `hello_world.txt` to verify setup
2. Test **Infrared** → Point at a TV and try the universal remote
3. Explore **SubGHz** → Browse saved RF captures
