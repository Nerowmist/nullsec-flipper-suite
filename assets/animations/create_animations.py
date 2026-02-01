#!/usr/bin/env python3
"""
NullSec Flipper Zero Animation Generator
Creates custom boot animations and dolphin animations
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Flipper Zero screen is 128x64 pixels, 1-bit (black/white)
WIDTH, HEIGHT = 128, 64

def create_frame(text_lines, frame_num=0, glitch=False):
    """Create a single animation frame"""
    img = Image.new('1', (WIDTH, HEIGHT), 0)  # Black background
    draw = ImageDraw.Draw(img)
    
    # Try to use a font, fall back to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 10)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 8)
    except:
        font = ImageFont.load_default()
        font_small = font
    
    if glitch and frame_num % 3 == 0:
        # Add glitch effect
        for i in range(5):
            y = (frame_num * 7 + i * 13) % HEIGHT
            draw.line([(0, y), (WIDTH, y)], fill=1, width=1)
    
    # Draw text
    y_offset = 5
    for line in text_lines:
        draw.text((4, y_offset), line, font=font, fill=1)
        y_offset += 12
    
    return img

def create_boot_animation():
    """Create NullSec boot animation frames"""
    frames = []
    
    # Frame sequence for boot
    sequences = [
        ["", "", "  INITIALIZING...", ""],
        ["  ███▒▒▒▒▒▒▒  10%", "", "  LOADING SYSTEM", ""],
        ["  █████▒▒▒▒▒  40%", "", "  LOADING MODULES", ""],
        ["  ████████▒▒  70%", "", "  DECRYPTING...", ""],
        ["  ██████████ 100%", "", "  SYSTEM READY", ""],
        ["", " ╔═╗╦ ╦╦  ╦  ╔═╗╔═╗╔═╗", " ║║║║ ║║  ║  ╚═╗║╣ ║  ", " ╝╚╝╚═╝╩═╝╩═╝╚═╝╚═╝╚═╝", ""],
        [" ┌─────────────────┐", " │   N U L L S E C │", " │  FLIPPER SUITE  │", " └─────────────────┘", "   [ ARMED ]"],
    ]
    
    for i, seq in enumerate(sequences):
        img = create_frame(seq, i, glitch=(i < 4))
        frames.append(img)
    
    return frames

def create_idle_animation():
    """Create idle/passport animation"""
    frames = []
    
    skull_frames = [
        [
            "    ██████████    ",
            "  ██▓▓▓▓▓▓▓▓▓▓██  ",
            " █▓▓██▓▓▓▓██▓▓▓█ ",
            " █▓▓▓▓▓██▓▓▓▓▓▓█ ",
            "  █▓█▓▓▓▓▓▓█▓█  ",
            "   ██▓▓▓▓▓▓██   ",
            "    ████████    ",
        ],
        [
            "    ██████████    ",
            "  ██░░░░░░░░░░██  ",
            " █░░██░░░░██░░░█ ",
            " █░░░░░██░░░░░░█ ",
            "  █░█░░░░░░█░█  ",
            "   ██░░░░░░██   ",
            "    ████████    ",
        ]
    ]
    
    for i, skull in enumerate(skull_frames * 3):  # Repeat for animation
        img = Image.new('1', (WIDTH, HEIGHT), 0)
        draw = ImageDraw.Draw(img)
        
        # Draw skull
        y = 5
        for line in skull:
            # Convert block chars to pixels
            x = 30
            for char in line:
                if char in ['█', '▓', '░']:
                    draw.rectangle([x, y, x+2, y+6], fill=1)
                x += 3
            y += 7
        
        # Add text below
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 8)
        except:
            font = ImageFont.load_default()
        
        draw.text((35, 54), "NULLSEC", font=font, fill=1)
        frames.append(img)
    
    return frames

def save_animation(frames, name, output_dir):
    """Save animation frames in Flipper format"""
    anim_dir = os.path.join(output_dir, name)
    os.makedirs(anim_dir, exist_ok=True)
    
    # Save frames
    for i, frame in enumerate(frames):
        frame.save(os.path.join(anim_dir, f"frame_{i}.png"))
    
    # Create meta.txt
    meta = f"""Filetype: Flipper Animation
Version: 1

Width: 128
Height: 64

Passive frames: {len(frames)}
Active frames: 0
Frames order: {' '.join(str(i) for i in range(len(frames)))}
Active cycles: 1
Frame rate: 3
Duration: {len(frames) * 333}
Active cooldown: 0

Bubble slots: 0
"""
    with open(os.path.join(anim_dir, "meta.txt"), 'w') as f:
        f.write(meta)
    
    print(f"Created animation: {name} ({len(frames)} frames)")

# Create animations
print("Creating NullSec boot animation...")
boot_frames = create_boot_animation()
save_animation(boot_frames, "NullSec_Boot_128x64", ".")

print("Creating NullSec idle animation...")
idle_frames = create_idle_animation()
save_animation(idle_frames, "NullSec_Idle_128x64", ".")

print("Done!")
