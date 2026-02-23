#!/usr/bin/env python3
# 800x480, 3-color (white/black/red), IBM Plex Mono
# requires: Pillow, fonts-ibm-plex
#   pip3 install Pillow
#   apt install fonts-ibm-plex

from PIL import Image, ImageDraw, ImageFont
import os
import math

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(SCRIPT_DIR, "fonts/IBMPlexMono-Regular.otf")

W, H = 800, 480
WHITE, BLACK, RED = (255,255,255), (0,0,0), (255,0,0)
DATE = "2026-02-24"
SIZE = 20

with open(os.path.join(SCRIPT_DIR, "../contract/still_alive.tz"), "r") as f:
    code = f.read().splitlines()

font = ImageFont.truetype(FONT, SIZE)
img = Image.new("RGB", (W, H), WHITE)
draw = ImageDraw.Draw(img)

# poem
lh = int(SIZE * 1.9)
th = len(code) * lh
mw = max(draw.textbbox((0,0), l, font=font)[2] for l in code)
cx, cy = (W - mw) // 2, (H - th) // 2 - 6

for i, l in enumerate(code):
    draw.text((cx, cy + i * lh), l, font=font, fill=BLACK)

# border
px, py, gap = 32, 24, 8
b = [cx - px, cy - py, cx + mw + px, cy + th + py - 6]
draw.rectangle(b, outline=BLACK, width=2)
draw.rectangle([b[0]-gap, b[1]-gap, b[2]+gap, b[3]+gap], outline=BLACK, width=2)

# message
rad = math.radians(30)
for i, ch in enumerate("STILL ALIVE"):
    if ch == ' ': continue
    x = 24 + i * 14 * math.cos(rad)
    y = 86 - i * 14 * math.sin(rad)
    tmp = Image.new("RGBA", (50,50), (0,0,0,0))
    ImageDraw.Draw(tmp).text((25,25), ch, font=font, fill=RED+(255,), anchor="mm")
    rot = tmp.rotate(30, resample=Image.BICUBIC)
    rgba = img.convert("RGBA")
    rgba.paste(rot, (int(x)-25, int(y)-25), rot)
    img = rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

# redraw borders
draw.rectangle(b, outline=BLACK, width=2)
draw.rectangle([b[0]-gap, b[1]-gap, b[2]+gap, b[3]+gap], outline=BLACK, width=2)

# signature
draw.text((W-24, H-22), f"zeroichi arakawa // {DATE}", font=font, fill=BLACK, anchor="rb")

px = img.load()
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        dw = (r-255)**2 + (g-255)**2 + (b-255)**2
        dk = r**2 + g**2 + b**2
        dr = (r-255)**2 + g**2 + b**2
        m = min(dw, dk, dr)
        px[x, y] = RED if m == dr and r > 100 and g < 150 else BLACK if m == dk else WHITE

img.save("message.bmp", "BMP")
