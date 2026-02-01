#!/bin/bash
# NullSec Flipper Zero Suite - Upload Script
# Uploads all custom content to Flipper Zero via serial

FLIPPER_PORT="/dev/ttyACM0"
SUITE_DIR="/home/antics/nullsec/flipper-zero"
FLIPPER_SD="/ext"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_banner() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║     _   _       _ _ ____                                  ║"
    echo "║    | \ | |_   _| | / ___|  ___  ___                       ║"
    echo "║    |  \| | | | | | \___ \ / _ \/ __|                      ║"
    echo "║    | |\  | |_| | | |___) |  __/ (__                       ║"
    echo "║    |_| \_|\__,_|_|_|____/ \___|\___|                      ║"
    echo "║                                                           ║"
    echo "║            Flipper Zero Suite Uploader v1.0               ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

check_flipper() {
    if [ ! -e "$FLIPPER_PORT" ]; then
        echo -e "${RED}[!] Flipper Zero not found on $FLIPPER_PORT${NC}"
        echo -e "${YELLOW}[*] Make sure Flipper is connected and not in use by qFlipper${NC}"
        exit 1
    fi
    echo -e "${GREEN}[+] Flipper Zero found on $FLIPPER_PORT${NC}"
}

upload_via_storage() {
    local src="$1"
    local dest="$2"
    echo -e "${CYAN}[*] Uploading: $src -> $dest${NC}"
    
    # Use screen or minicom to send commands, or use ufbt/flipper cli
    # For now, we'll create a command file for manual upload or use Python
}

# Check for ufbt or flipper-cli
check_tools() {
    if command -v ufbt &> /dev/null; then
        echo -e "${GREEN}[+] ufbt found${NC}"
        UPLOAD_METHOD="ufbt"
    elif command -v flipper &> /dev/null; then
        echo -e "${GREEN}[+] flipper-cli found${NC}"
        UPLOAD_METHOD="flipper"
    elif python3 -c "import serial" 2>/dev/null; then
        echo -e "${GREEN}[+] Using Python serial upload${NC}"
        UPLOAD_METHOD="python"
    else
        echo -e "${YELLOW}[!] No upload tool found. Creating manual upload package.${NC}"
        UPLOAD_METHOD="manual"
    fi
}

create_upload_package() {
    echo -e "${CYAN}[*] Creating upload package for qFlipper/manual transfer...${NC}"
    
    PACKAGE_DIR="/tmp/nullsec-flipper-package"
    rm -rf "$PACKAGE_DIR"
    mkdir -p "$PACKAGE_DIR"
    
    # Copy BadUSB
    mkdir -p "$PACKAGE_DIR/badusb"
    cp -r "$SUITE_DIR/badusb/nullsec" "$PACKAGE_DIR/badusb/"
    echo -e "${GREEN}[+] BadUSB payloads: $(ls $SUITE_DIR/badusb/nullsec/ | wc -l)${NC}"
    
    # Copy SubGHz
    mkdir -p "$PACKAGE_DIR/subghz"
    cp -r "$SUITE_DIR/subghz/nullsec" "$PACKAGE_DIR/subghz/"
    echo -e "${GREEN}[+] SubGHz files: $(ls $SUITE_DIR/subghz/nullsec/ | wc -l)${NC}"
    
    # Copy Infrared
    mkdir -p "$PACKAGE_DIR/infrared"
    cp -r "$SUITE_DIR/infrared/nullsec" "$PACKAGE_DIR/infrared/"
    echo -e "${GREEN}[+] IR remotes: $(ls $SUITE_DIR/infrared/nullsec/ | wc -l)${NC}"
    
    # Copy NFC
    mkdir -p "$PACKAGE_DIR/nfc"
    cp -r "$SUITE_DIR/nfc/nullsec" "$PACKAGE_DIR/nfc/"
    echo -e "${GREEN}[+] NFC files: $(ls $SUITE_DIR/nfc/nullsec/ | wc -l)${NC}"
    
    # Copy RFID
    mkdir -p "$PACKAGE_DIR/lfrfid"
    cp -r "$SUITE_DIR/rfid/nullsec" "$PACKAGE_DIR/lfrfid/"
    echo -e "${GREEN}[+] RFID files: $(ls $SUITE_DIR/rfid/nullsec/ | wc -l)${NC}"
    
    # Copy iButton
    mkdir -p "$PACKAGE_DIR/ibutton"
    cp -r "$SUITE_DIR/ibutton/nullsec" "$PACKAGE_DIR/ibutton/"
    echo -e "${GREEN}[+] iButton files: $(ls $SUITE_DIR/ibutton/nullsec/ | wc -l)${NC}"
    
    # Copy Music
    mkdir -p "$PACKAGE_DIR/music_player"
    cp -r "$SUITE_DIR/music_player/nullsec" "$PACKAGE_DIR/music_player/"
    echo -e "${GREEN}[+] Music files: $(ls $SUITE_DIR/music_player/nullsec/ | wc -l)${NC}"
    
    # Copy Asset Pack
    mkdir -p "$PACKAGE_DIR/asset_packs"
    cp -r "$SUITE_DIR/asset_pack/NullSec" "$PACKAGE_DIR/asset_packs/"
    echo -e "${GREEN}[+] Asset pack: NullSec${NC}"
    
    # Create zip
    cd /tmp
    zip -r nullsec-flipper-suite.zip nullsec-flipper-package/
    mv nullsec-flipper-suite.zip "$SUITE_DIR/"
    
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║              Upload Package Created!                      ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}Package location: $SUITE_DIR/nullsec-flipper-suite.zip${NC}"
    echo ""
    echo -e "${YELLOW}To install:${NC}"
    echo "1. Open qFlipper and connect your Flipper Zero"
    echo "2. Go to 'File Manager' tab"
    echo "3. Extract the zip and copy folders to SD card:"
    echo "   - badusb/nullsec -> /ext/badusb/"
    echo "   - subghz/nullsec -> /ext/subghz/"
    echo "   - infrared/nullsec -> /ext/infrared/"
    echo "   - nfc/nullsec -> /ext/nfc/"
    echo "   - lfrfid/nullsec -> /ext/lfrfid/"
    echo "   - ibutton/nullsec -> /ext/ibutton/"
    echo "   - music_player/nullsec -> /ext/music_player/"
    echo "   - asset_packs/NullSec -> /ext/dolphin/asset_packs/"
    echo ""
    echo -e "${CYAN}Or drag the entire package to the SD card root!${NC}"
}

main() {
    print_banner
    check_flipper
    check_tools
    
    case $UPLOAD_METHOD in
        "ufbt"|"flipper"|"python")
            echo -e "${CYAN}[*] Direct upload not implemented yet, creating package...${NC}"
            create_upload_package
            ;;
        "manual")
            create_upload_package
            ;;
    esac
}

main "$@"
