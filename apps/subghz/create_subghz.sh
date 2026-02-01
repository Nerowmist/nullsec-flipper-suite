#!/bin/bash

# NullSec SubGHz Payload Suite
# Creates custom SubGHz signals

SUBGHZ_DIR="/home/antics/nullsec/flipper-zero/apps/subghz"
mkdir -p "$SUBGHZ_DIR"/{garage,car,rf_bruteforce,replay,custom}

echo "Creating NullSec SubGHz Files..."

# ============= GARAGE DOOR SIGNALS =============

cat > "$SUBGHZ_DIR/garage/GenericGarage_315.sub" << 'EOF'
Filetype: Flipper SubGhz RAW File
Version: 1
# NullSec Generic Garage Opener 315MHz
Frequency: 315000000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: RAW
RAW_Data: 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -334 668 -334 668 -334 668 -334 668 -334 668 -334 668 -334 668 -334 668 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334
EOF

cat > "$SUBGHZ_DIR/garage/GenericGarage_390.sub" << 'EOF'
Filetype: Flipper SubGhz RAW File
Version: 1
# NullSec Generic Garage Opener 390MHz
Frequency: 390000000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: RAW
RAW_Data: 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -334 668 -334 668 -334 668 -334 668 -334 668 -334 668 -334 668 -334 668 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334
EOF

cat > "$SUBGHZ_DIR/garage/GenericGarage_433.sub" << 'EOF'
Filetype: Flipper SubGhz RAW File
Version: 1
# NullSec Generic Garage Opener 433.92MHz
Frequency: 433920000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: RAW
RAW_Data: 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -334 668 -334 668 -334 668 -334 668 -334 668 -334 668 -334 668 -334 668 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334 -668 334
EOF

# ============= CAR FOB SIGNALS =============

cat > "$SUBGHZ_DIR/car/GenericCarFob_315.sub" << 'EOF'
Filetype: Flipper SubGhz RAW File
Version: 1
# NullSec Generic Car Fob 315MHz
Frequency: 315000000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: RAW
RAW_Data: 500 -500 500 -500 500 -1000 1000 -500 500 -1000 1000 -1000 500 -500 500 -500 1000 -1000 500 -500 500 -1000 1000 -500 500 -500 500 -500 1000 -1000 1000 -500 500 -500 500 -500 500 -500 500 -5000
EOF

cat > "$SUBGHZ_DIR/car/GenericCarFob_433.sub" << 'EOF'
Filetype: Flipper SubGhz RAW File
Version: 1
# NullSec Generic Car Fob 433.92MHz  
Frequency: 433920000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: RAW
RAW_Data: 500 -500 500 -500 500 -1000 1000 -500 500 -1000 1000 -1000 500 -500 500 -500 1000 -1000 500 -500 500 -1000 1000 -500 500 -500 500 -500 1000 -1000 1000 -500 500 -500 500 -500 500 -500 500 -5000
EOF

# ============= CUSTOM SIGNALS =============

cat > "$SUBGHZ_DIR/custom/Jammer_315.sub" << 'EOF'
Filetype: Flipper SubGhz RAW File
Version: 1
# NullSec RF Jammer Pattern 315MHz
# FOR EDUCATIONAL PURPOSES ONLY
Frequency: 315000000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: RAW
RAW_Data: 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100
EOF

cat > "$SUBGHZ_DIR/custom/Jammer_433.sub" << 'EOF'
Filetype: Flipper SubGhz RAW File
Version: 1
# NullSec RF Jammer Pattern 433MHz
# FOR EDUCATIONAL PURPOSES ONLY
Frequency: 433920000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: RAW
RAW_Data: 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100 -100 100
EOF

cat > "$SUBGHZ_DIR/custom/DoorBell_433.sub" << 'EOF'
Filetype: Flipper SubGhz RAW File
Version: 1
# NullSec Doorbell Signal 433MHz
Frequency: 433920000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: RAW
RAW_Data: 350 -1050 350 -1050 350 -1050 1050 -350 350 -1050 1050 -350 1050 -350 350 -1050 350 -1050 1050 -350 350 -1050 1050 -350 350 -1050 350 -1050 1050 -350 1050 -350 350 -10000
EOF

cat > "$SUBGHZ_DIR/custom/FanRemote_433.sub" << 'EOF'
Filetype: Flipper SubGhz RAW File
Version: 1
# NullSec Fan Remote 433MHz
Frequency: 433920000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: RAW
RAW_Data: 400 -400 400 -800 800 -400 400 -800 400 -400 800 -800 400 -400 400 -400 800 -400 400 -800 400 -400 400 -400 400 -800 800 -400 400 -5000
EOF

# ============= REPLAY TEMPLATES =============

cat > "$SUBGHZ_DIR/replay/README.txt" << 'EOF'
NullSec SubGHz Replay Templates

To capture and replay signals:

1. Go to Sub-GHz > Read RAW
2. Select your frequency (315/433/868 MHz)
3. Press record and trigger the target device
4. Save the captured signal
5. Go to Sub-GHz > Saved
6. Select your capture and Send

Tips:
- For rolling codes, use the RollingFlaws plugin
- Some frequencies may be restricted in your region
- Always ensure you have permission

NullSec Flipper Suite
EOF

echo ""
echo "╔═══════════════════════════════════════════════╗"
echo "║     NullSec SubGHz Files Created!             ║"
echo "╚═══════════════════════════════════════════════╝"
echo ""
find "$SUBGHZ_DIR" -name "*.sub" -o -name "*.txt" | wc -l
echo " files created"
