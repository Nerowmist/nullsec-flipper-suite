# Installation Guide

## System Requirements

- Flipper Zero hardware (any revision)
- Firmware v0.89.0 or newer
- microSD card (FAT32, 2-32GB)
- Computer with USB port

## Quick Install

```bash
git clone https://github.com/bad-antics/nullsec-flipper-suite.git
cd nullsec-flipper-suite
```

## Selective Install

Only want specific categories? Copy individual folders:

```bash
# Just BadUSB payloads
cp -r badusb/ /path/to/flipper-sd/

# Just SubGHz captures
cp -r subghz/ /path/to/flipper-sd/

# Just animations
cp -r animations/ /path/to/flipper-sd/dolphin/
```

## Firmware Compatibility Matrix

| Feature | Official | Momentum | Unleashed | Xtreme |
|---------|:--------:|:--------:|:---------:|:------:|
| BadUSB | ✅ | ✅ | ✅ | ✅ |
| SubGHz TX | ⚠️ | ✅ | ✅ | ✅ |
| Extended freq | ❌ | ✅ | ✅ | ✅ |
| Custom anims | ✅ | ✅ | ✅ | ✅ |

## Updating

```bash
cd nullsec-flipper-suite
git pull origin main
# Re-copy updated files to Flipper SD
```
