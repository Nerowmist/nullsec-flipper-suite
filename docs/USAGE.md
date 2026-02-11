# Usage Guide

## BadUSB Payloads

### Running a Payload
1. Connect Flipper to target via USB
2. Navigate: `BadUSB > nullsec > [category] > [payload]`
3. Press ▶️ to execute
4. Wait for completion indicator

### Customizing Payloads
Edit `.txt` files with any text editor. DuckyScript syntax reference:
- `DELAY [ms]` — Wait in milliseconds
- `STRING [text]` — Type text
- `ENTER` — Press Enter
- `GUI r` — Windows+R
- `ALT F4` — Alt+F4

## SubGHz Operations

### Read Mode
Passively capture RF signals from nearby devices.

### Read RAW
Capture raw RF data for unknown protocols.

### Saved
Replay previously captured signals.

## Infrared

### Universal Remotes
Pre-built databases for common devices. Point Flipper at device and select commands.

### Learning Mode
Capture new IR signals from existing remotes.

## NFC/RFID

### Read
Hold card against Flipper to read data.

### Emulate
Replay saved card data from Flipper.

### Saved
Manage your card collection.
