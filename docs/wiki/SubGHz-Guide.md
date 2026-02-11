# SubGHz Guide

## Overview

40 RF signal captures and templates covering 315 MHz to 915 MHz frequencies.

## Supported Protocols

| Protocol | Frequency | Use Case |
|----------|-----------|----------|
| AM270/AM650 | 315 MHz | Garage doors (US) |
| FM238/FM476 | 433.92 MHz | European devices |
| CAME | 433.92 MHz | Gate remotes |
| Nice FLO | 433.92 MHz | Gate systems |
| Princeton | 315/433 MHz | Various remotes |
| Holtek | 433 MHz | Key fobs |

## Legal Disclaimer

⚠️ **IMPORTANT**: Only use these captures on devices you own or have explicit permission to test. Transmitting on certain frequencies may violate local regulations.

## Capturing Signals

1. Navigate to `Sub-GHz > Read` on your Flipper
2. Press the remote button near the Flipper
3. Save the captured signal
4. Files are saved in `.sub` format on SD card

## Replaying Signals

1. Navigate to `Sub-GHz > Saved`
2. Select the `.sub` file
3. Press `Send` to replay

## File Format

```
Filetype: Flipper SubGhz RAW File
Version: 1
Frequency: 433920000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: RAW
RAW_Data: 5000 -500 500 -500 ...
```
