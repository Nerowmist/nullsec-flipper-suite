#!/bin/bash

IR_DIR="/home/antics/nullsec/flipper-zero/apps/infrared"
mkdir -p "$IR_DIR"/{tv,projector,ac,universal}

echo "Creating NullSec IR Remote Files..."

# Universal TV Power Off
cat > "$IR_DIR/universal/TVKiller.ir" << 'EOF'
Filetype: IR signals file
Version: 1
# NullSec TV Killer - Universal Power Off
# Cycles through common TV power codes
#
name: Samsung_Power
type: parsed
protocol: Samsung32
address: 07 00 00 00
command: 02 00 00 00
#
name: LG_Power
type: parsed
protocol: NEC
address: 04 00 00 00
command: 08 00 00 00
#
name: Sony_Power
type: parsed
protocol: SIRC
address: 01 00 00 00
command: 15 00 00 00
#
name: Vizio_Power
type: parsed
protocol: NEC
address: 04 00 00 00
command: 08 00 00 00
#
name: TCL_Power
type: parsed
protocol: NEC
address: 00 00 00 00
command: 08 00 00 00
#
name: Hisense_Power
type: parsed
protocol: NEC
address: 00 BD 00 00
command: 02 00 00 00
#
name: Philips_Power
type: parsed
protocol: RC5
address: 00 00 00 00
command: 0C 00 00 00
#
name: Panasonic_Power
type: parsed
protocol: Kaseikyo
address: 00 02 20 00
command: 00 00 3D 00
#
name: Sharp_Power
type: parsed
protocol: NEC
address: AA 00 00 00
command: 1B 00 00 00
#
name: Toshiba_Power
type: parsed
protocol: NEC
address: 40 00 00 00
command: 12 00 00 00
EOF

# Universal Volume Controls
cat > "$IR_DIR/universal/VolumeMax.ir" << 'EOF'
Filetype: IR signals file
Version: 1
# NullSec Volume Maximizer
#
name: Samsung_VolUp
type: parsed
protocol: Samsung32
address: 07 00 00 00
command: 07 00 00 00
#
name: LG_VolUp
type: parsed
protocol: NEC
address: 04 00 00 00
command: 02 00 00 00
#
name: Sony_VolUp
type: parsed
protocol: SIRC
address: 01 00 00 00
command: 12 00 00 00
EOF

# Projector Controls
cat > "$IR_DIR/projector/ProjectorOff.ir" << 'EOF'
Filetype: IR signals file
Version: 1
# NullSec Projector Power Off
#
name: Epson_Power
type: parsed
protocol: NEC
address: 05 00 00 00
command: 02 00 00 00
#
name: BenQ_Power
type: parsed
protocol: NEC
address: 30 00 00 00
command: 02 00 00 00
#
name: Optoma_Power
type: parsed
protocol: NEC
address: 83 00 00 00
command: 02 00 00 00
EOF

# AC Controls
cat > "$IR_DIR/ac/AC_Universal.ir" << 'EOF'
Filetype: IR signals file
Version: 1
# NullSec Universal AC Control
#
name: AC_Off
type: raw
frequency: 38000
duty_cycle: 0.330000
data: 9024 4512 564 564 564 564 564 1692 564 564 564 564 564 564 564 564 564 564 564 1692 564 1692 564 564 564 1692 564 1692 564 1692 564 1692 564 1692 564 564 564 1692 564 564 564 564 564 564 564 564 564 564 564 564 564 1692 564 564 564 1692 564 1692 564 1692 564 1692 564 1692 564 1692 564 39756
#
name: AC_18C
type: raw
frequency: 38000
duty_cycle: 0.330000
data: 9024 4512 564 564 564 564 564 1692 564 564 564 564 564 564 564 564 564 564 564 1692 564 1692 564 564 564 1692 564 1692 564 1692 564 1692 564 1692 564 1692 564 564 564 564 564 564 564 1692 564 564 564 564 564 564 564 564 564 1692 564 1692 564 1692 564 564 564 1692 564 1692 564 1692 564 39756
#
name: AC_24C
type: raw
frequency: 38000
duty_cycle: 0.330000
data: 9024 4512 564 564 564 564 564 1692 564 564 564 564 564 564 564 564 564 564 564 1692 564 1692 564 564 564 1692 564 1692 564 1692 564 1692 564 1692 564 564 564 564 564 1692 564 1692 564 564 564 564 564 564 564 564 564 1692 564 1692 564 564 564 564 564 1692 564 1692 564 1692 564 1692 564 39756
EOF

echo ""
echo "╔═══════════════════════════════════════════════╗"
echo "║     NullSec IR Remote Files Created!          ║"
echo "╚═══════════════════════════════════════════════╝"
find "$IR_DIR" -name "*.ir" | wc -l
echo " IR files created"
