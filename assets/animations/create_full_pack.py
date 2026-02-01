#!/usr/bin/env python3
"""
NullSec Flipper Zero Complete Asset Pack Generator
Creates boot animations, idle animations, level-up animations, and icons
"""

from PIL import Image, ImageDraw, ImageFont
import os
import random

WIDTH, HEIGHT = 128, 64

def get_font(size=10):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", size)
    except:
        try:
            return ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf", size)
        except:
            return ImageFont.load_default()

def draw_hacker_skull(draw, x, y, size=1):
    """Draw a pixel skull"""
    skull = [
        "  ████  ",
        " ██████ ",
        "█ ▓▓▓▓ █",
        "██ ██ ██",
        " ██████ ",
        "  █  █  ",
    ]
    py = y
    for row in skull:
        px = x
        for c in row:
            if c in ['█', '▓']:
                draw.rectangle([px, py, px+size, py+size], fill=1)
            px += size + 1
        py += size + 2

def draw_matrix_rain(draw, frame, density=15):
    """Draw matrix-style falling characters"""
    random.seed(42)  # Consistent pattern
    chars = "01アイウエオカキクケコサシスセソ"
    font = get_font(6)
    for i in range(density):
        x = (i * 9) % WIDTH
        for j in range(8):
            y = ((frame * 3 + j * 8 + i * 5) % (HEIGHT + 20)) - 10
            if 0 <= y < HEIGHT:
                c = chars[(i + j + frame) % len(chars)]
                brightness = 1 if j < 2 else (1 if random.random() > 0.3 else 0)
                if brightness:
                    draw.text((x, y), c, font=font, fill=1)

def draw_glitch_lines(draw, frame, intensity=3):
    """Draw glitch effect lines"""
    random.seed(frame)
    for _ in range(intensity):
        y = random.randint(0, HEIGHT-1)
        x1 = random.randint(0, WIDTH//2)
        x2 = random.randint(WIDTH//2, WIDTH)
        draw.line([(x1, y), (x2, y)], fill=1, width=1)

def create_boot_sequence():
    """Create boot animation - Matrix style with NullSec branding"""
    frames = []
    font = get_font(10)
    font_small = get_font(8)
    font_tiny = get_font(6)
    
    # Phase 1: Matrix initialization (frames 0-4)
    for i in range(5):
        img = Image.new('1', (WIDTH, HEIGHT), 0)
        draw = ImageDraw.Draw(img)
        draw_matrix_rain(draw, i, density=10 + i*2)
        if i > 1:
            draw.rectangle([20, 25, 108, 40], fill=0)
            draw.text((24, 27), "INITIALIZING...", font=font_small, fill=1)
        frames.append(img)
    
    # Phase 2: System loading (frames 5-9)
    loading_texts = [
        ("LOADING KERNEL", 20),
        ("DECRYPTING", 40),
        ("LOADING MODULES", 60),
        ("BYPASSING SECURITY", 80),
        ("SYSTEM ARMED", 100),
    ]
    for i, (text, pct) in enumerate(loading_texts):
        img = Image.new('1', (WIDTH, HEIGHT), 0)
        draw = ImageDraw.Draw(img)
        draw_matrix_rain(draw, i+5, density=8)
        draw_glitch_lines(draw, i, intensity=2)
        
        # Progress bar
        draw.rectangle([10, 20, 118, 35], outline=1)
        bar_width = int(100 * pct / 100)
        draw.rectangle([12, 22, 12 + bar_width, 33], fill=1)
        
        draw.rectangle([10, 38, 118, 50], fill=0)
        draw.text((14, 40), text, font=font_small, fill=1)
        draw.text((90, 40), f"{pct}%", font=font_small, fill=1)
        frames.append(img)
    
    # Phase 3: NullSec logo reveal (frames 10-14)
    logo_lines = [
        "╔═══════════════════════╗",
        "║     N U L L S E C     ║",
        "║    FLIPPER  SUITE     ║",
        "╚═══════════════════════╝",
    ]
    for i in range(5):
        img = Image.new('1', (WIDTH, HEIGHT), 0)
        draw = ImageDraw.Draw(img)
        
        if i < 3:
            draw_glitch_lines(draw, i*3, intensity=5-i)
        
        y = 15
        for j, line in enumerate(logo_lines):
            if j <= i or i >= 3:
                draw.text((10, y), line, font=font_small, fill=1)
            y += 12
        
        if i >= 3:
            draw.text((40, 54), "[ READY ]", font=font_small, fill=1)
        
        frames.append(img)
    
    return frames

def create_level_animations():
    """Create level 1-3 idle animations"""
    animations = {}
    font = get_font(8)
    
    # Level 1 animations
    level1_anims = {
        "L1_NullSec_Hacking_128x64": create_hacking_animation,
        "L1_NullSec_Scanning_128x64": create_scanning_animation,
        "L1_NullSec_Idle_128x64": create_idle_animation,
        "L1_NullSec_Matrix_128x64": create_matrix_idle,
    }
    
    # Level 2 animations
    level2_anims = {
        "L2_NullSec_Coding_128x64": create_coding_animation,
        "L2_NullSec_Pwned_128x64": create_pwned_animation,
    }
    
    # Level 3 animations
    level3_anims = {
        "L3_NullSec_Victory_128x64": create_victory_animation,
        "L3_NullSec_Elite_128x64": create_elite_animation,
    }
    
    return {**level1_anims, **level2_anims, **level3_anims}

def create_hacking_animation():
    """Hacking terminal animation"""
    frames = []
    font = get_font(7)
    
    hack_lines = [
        "> nmap -sV target",
        "> exploiting...",
        "> shell obtained",
        "> pwned!",
    ]
    
    for i in range(8):
        img = Image.new('1', (WIDTH, HEIGHT), 0)
        draw = ImageDraw.Draw(img)
        
        # Terminal header
        draw.rectangle([0, 0, 127, 10], fill=1)
        draw.text((2, 1), "NULLSEC TERMINAL", font=font, fill=0)
        
        # Terminal content
        y = 14
        for j, line in enumerate(hack_lines[:min(i//2+1, 4)]):
            if i % 2 == 0 and j == min(i//2, 3):
                line = line + "_"
            draw.text((4, y), line, font=font, fill=1)
            y += 10
        
        # Cursor blink
        if i % 2 == 0:
            draw.rectangle([4 + len(hack_lines[min(i//2, 3)])*5, y-10, 8 + len(hack_lines[min(i//2, 3)])*5, y-2], fill=1)
        
        frames.append(img)
    
    return frames

def create_scanning_animation():
    """Network scanning animation"""
    frames = []
    font = get_font(7)
    
    for i in range(6):
        img = Image.new('1', (WIDTH, HEIGHT), 0)
        draw = ImageDraw.Draw(img)
        
        # Radar sweep
        cx, cy = 32, 32
        draw.ellipse([cx-25, cy-25, cx+25, cy+25], outline=1)
        draw.ellipse([cx-15, cy-15, cx+15, cy+15], outline=1)
        draw.ellipse([cx-5, cy-5, cx+5, cy+5], fill=1)
        
        # Sweep line
        import math
        angle = (i * 60) * math.pi / 180
        x2 = cx + int(25 * math.cos(angle))
        y2 = cy + int(25 * math.sin(angle))
        draw.line([(cx, cy), (x2, y2)], fill=1, width=2)
        
        # Blips
        for j in range(3):
            bx = cx + int(20 * math.cos(angle - 0.5 - j*0.3))
            by = cy + int(20 * math.sin(angle - 0.5 - j*0.3))
            if 5 < bx < 58 and 5 < by < 58:
                draw.ellipse([bx-2, by-2, bx+2, by+2], fill=1)
        
        # Side panel
        draw.rectangle([65, 5, 125, 58], outline=1)
        draw.text((68, 8), "SCAN MODE", font=font, fill=1)
        draw.text((68, 20), f"NETS: {i+1}", font=font, fill=1)
        draw.text((68, 32), f"DEVS: {(i+1)*3}", font=font, fill=1)
        draw.text((68, 44), "ACTIVE", font=font, fill=1)
        
        frames.append(img)
    
    return frames

def create_idle_animation():
    """Simple idle with skull"""
    frames = []
    font = get_font(8)
    
    for i in range(4):
        img = Image.new('1', (WIDTH, HEIGHT), 0)
        draw = ImageDraw.Draw(img)
        
        # Draw skull
        skull_y = 5 + (i % 2)
        draw_hacker_skull(draw, 45, skull_y, size=2)
        
        draw.text((35, 45), "NULLSEC", font=font, fill=1)
        draw.text((30, 54), "[ ARMED ]", font=font, fill=1)
        
        frames.append(img)
    
    return frames

def create_matrix_idle():
    """Matrix rain idle"""
    frames = []
    for i in range(8):
        img = Image.new('1', (WIDTH, HEIGHT), 0)
        draw = ImageDraw.Draw(img)
        draw_matrix_rain(draw, i, density=12)
        
        # NullSec text overlay
        draw.rectangle([25, 25, 103, 40], fill=0)
        draw.rectangle([25, 25, 103, 40], outline=1)
        font = get_font(10)
        draw.text((30, 27), "NULLSEC", font=font, fill=1)
        
        frames.append(img)
    
    return frames

def create_coding_animation():
    """Coding/programming animation"""
    frames = []
    font = get_font(6)
    
    code_lines = [
        "def exploit():",
        "  target.scan()",
        "  vuln = find()",
        "  shell = pwn()",
        "  return shell",
        "# NULLSEC",
    ]
    
    for i in range(8):
        img = Image.new('1', (WIDTH, HEIGHT), 0)
        draw = ImageDraw.Draw(img)
        
        y = 5
        for j, line in enumerate(code_lines):
            shown = line[:min(len(line), (i-j+1)*3)] if j <= i else ""
            draw.text((4, y), shown, font=font, fill=1)
            y += 9
        
        # Cursor
        if i % 2 == 0:
            cy = 5 + min(i, 5) * 9
            draw.rectangle([4 + min(len(code_lines[min(i,5)]), (i+1)*3)*4, cy, 8 + min(len(code_lines[min(i,5)]), (i+1)*3)*4, cy+7], fill=1)
        
        frames.append(img)
    
    return frames

def create_pwned_animation():
    """PWNED celebration"""
    frames = []
    font = get_font(12)
    font_small = get_font(8)
    
    for i in range(6):
        img = Image.new('1', (WIDTH, HEIGHT), 0)
        draw = ImageDraw.Draw(img)
        
        if i % 2 == 0:
            draw.rectangle([0, 0, 127, 63], outline=1)
            draw.rectangle([2, 2, 125, 61], outline=1)
        
        draw.text((25, 20), "PWNED!", font=font, fill=1)
        draw.text((20, 40), "Target owned", font=font_small, fill=1)
        
        # Particles
        for j in range(5):
            px = 64 + int(30 * ((i+j) % 3 - 1))
            py = 15 + int(20 * ((i+j*2) % 3 - 1))
            draw.text((px, py), "*", font=font_small, fill=1)
        
        frames.append(img)
    
    return frames

def create_victory_animation():
    """Level 3 victory animation"""
    frames = []
    font = get_font(10)
    font_small = get_font(8)
    
    for i in range(8):
        img = Image.new('1', (WIDTH, HEIGHT), 0)
        draw = ImageDraw.Draw(img)
        
        draw_matrix_rain(draw, i, density=6)
        
        # Crown
        crown = [
            "  █   █   █  ",
            " ███████████ ",
            "  █████████  ",
        ]
        y = 5
        for row in crown:
            x = 40
            for c in row:
                if c == '█':
                    draw.rectangle([x, y, x+3, y+4], fill=1)
                x += 3
            y += 5
        
        draw.text((20, 25), "ELITE HACKER", font=font, fill=1)
        draw.text((25, 40), "NULLSEC PRO", font=font_small, fill=1)
        draw.text((35, 52), "LVL MAX", font=font_small, fill=1)
        
        frames.append(img)
    
    return frames

def create_elite_animation():
    """Elite status animation"""
    frames = []
    font = get_font(10)
    
    for i in range(6):
        img = Image.new('1', (WIDTH, HEIGHT), 0)
        draw = ImageDraw.Draw(img)
        
        # Animated border
        for j in range(0, 128, 8):
            offset = (i * 2 + j // 8) % 4
            if offset < 2:
                draw.rectangle([j, 0, j+4, 2], fill=1)
                draw.rectangle([j, 61, j+4, 63], fill=1)
        
        for j in range(0, 64, 8):
            offset = (i * 2 + j // 8) % 4
            if offset < 2:
                draw.rectangle([0, j, 2, j+4], fill=1)
                draw.rectangle([125, j, 127, j+4], fill=1)
        
        draw.text((15, 22), "NULLSEC ELITE", font=font, fill=1)
        draw.text((30, 38), "[ ARMED ]", font=get_font(8), fill=1)
        
        frames.append(img)
    
    return frames

def save_flipper_animation(frames, name, base_dir):
    """Save in Flipper-compatible format (BM files)"""
    anim_dir = os.path.join(base_dir, name)
    os.makedirs(anim_dir, exist_ok=True)
    
    # Save each frame as BM (Flipper bitmap format)
    for i, frame in enumerate(frames):
        # Save as PNG first
        png_path = os.path.join(anim_dir, f"frame_{i}.png")
        frame.save(png_path)
        
        # Convert to BM format (1-bit bitmap)
        bm_path = os.path.join(anim_dir, f"frame_{i}.bm")
        
        # BM format: raw 1-bit packed pixels, 128x64 = 1024 bytes
        pixels = list(frame.getdata())
        bm_data = bytearray()
        
        for row in range(64):
            for col_byte in range(16):  # 128 pixels / 8 bits = 16 bytes per row
                byte = 0
                for bit in range(8):
                    pixel_idx = row * 128 + col_byte * 8 + bit
                    if pixels[pixel_idx]:
                        byte |= (1 << (7 - bit))
                bm_data.append(byte)
        
        with open(bm_path, 'wb') as f:
            f.write(bm_data)
    
    # Create meta.txt
    meta = f"""Filetype: Flipper Animation
Version: 1

Width: 128
Height: 64

Passive frames: {len(frames)}
Active frames: 0
Frames order: {' '.join(str(i) for i in range(len(frames)))}
Active cycles: 1
Frame rate: 2
Duration: {len(frames) * 500}
Active cooldown: 0

Bubble slots: 0
"""
    with open(os.path.join(anim_dir, "meta.txt"), 'w') as f:
        f.write(meta)
    
    print(f"  ✓ {name} ({len(frames)} frames)")
    return anim_dir

def main():
    base_dir = "/home/antics/nullsec/flipper-zero/assets/animations"
    
    print("\n╔══════════════════════════════════════╗")
    print("║  NullSec Flipper Asset Pack Creator  ║")
    print("╚══════════════════════════════════════╝\n")
    
    # Create boot animation
    print("[*] Creating boot sequence...")
    boot_frames = create_boot_sequence()
    save_flipper_animation(boot_frames, "NullSec_Boot_128x64", base_dir)
    
    # Create all level animations
    print("\n[*] Creating level animations...")
    anim_funcs = create_level_animations()
    for name, func in anim_funcs.items():
        frames = func()
        save_flipper_animation(frames, name, base_dir)
    
    # Create manifest
    print("\n[*] Creating manifest...")
    manifest_content = """Filetype: Flipper Animation Manifest
Version: 1

# NullSec Flipper Suite Animation Pack
# https://github.com/bad-antics/nullsec-flipper-suite

"""
    
    anims = os.listdir(base_dir)
    for anim in sorted(anims):
        if os.path.isdir(os.path.join(base_dir, anim)) and anim.startswith(("L1_", "L2_", "L3_", "NullSec")):
            manifest_content += f"Name: {anim}\n"
            if anim.startswith("L1_"):
                manifest_content += "Min level: 1\nMax level: 10\nWeight: 8\n\n"
            elif anim.startswith("L2_"):
                manifest_content += "Min level: 11\nMax level: 20\nWeight: 8\n\n"
            elif anim.startswith("L3_"):
                manifest_content += "Min level: 21\nMax level: 30\nWeight: 8\n\n"
    
    manifest_path = os.path.join(base_dir, "manifest.txt")
    with open(manifest_path, 'w') as f:
        f.write(manifest_content)
    
    print(f"\n[✓] Asset pack created at: {base_dir}")
    print(f"    Total animations: {len([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])}")

if __name__ == "__main__":
    main()
