# Troubleshooting

## Common Issues

### BadUSB not executing
- **Cause**: Flipper not recognized as HID device
- **Fix**: Unplug and replug USB. Try a different cable. Check firmware is up to date.
- **Fix**: On Linux, check if Flipper has HID permissions

### SubGHz won't transmit
- **Cause**: Region lock on official firmware
- **Fix**: Use custom firmware (Momentum/Unleashed) or set region in settings
- **Note**: Some frequencies are restricted by hardware

### Animations not showing
- **Cause**: Wrong folder structure or file format
- **Fix**: Animations go in `SD/dolphin/` with proper `manifest.txt`
- **Format**: Must be 128x64 BMP frames

### SD Card errors
- **Cause**: Card not formatted correctly
- **Fix**: Format as FAT32 (not exFAT). Max 32GB recommended.
- **Fix**: Try a different SD card — some brands are incompatible

### qFlipper not connecting
- **Cause**: Driver issues on Windows
- **Fix**: Install/reinstall qFlipper. Try different USB port.
- **Linux**: Add udev rules: `sudo cp flip.rules /etc/udev/rules.d/`

## Getting Help

- [GitHub Issues](https://github.com/bad-antics/nullsec-flipper-suite/issues)
- [Flipper Zero Discord](https://discord.gg/flipper)
- [NullSec Framework](https://github.com/bad-antics)
