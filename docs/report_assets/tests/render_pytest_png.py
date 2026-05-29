"""Render pytest_output.txt as a terminal-style PNG for the report."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
text = (HERE / "pytest_output.txt").read_text(encoding="utf-8", errors="replace").rstrip()
lines = text.splitlines()[-40:]

try:
    font = ImageFont.truetype("consola.ttf", 14)
    bold = ImageFont.truetype("consolab.ttf", 14)
except OSError:
    font = ImageFont.load_default()
    bold = font

PAD = 16
LINE_H = 18
W = 1100
H = PAD * 2 + 28 + LINE_H * len(lines)

img = Image.new("RGB", (W, H), "#1e1e1e")
d = ImageDraw.Draw(img)

d.rectangle([0, 0, W, 28], fill="#323233")
d.ellipse([10, 8, 22, 20], fill="#ff5f56")
d.ellipse([28, 8, 40, 20], fill="#ffbd2e")
d.ellipse([46, 8, 58, 20], fill="#27c93f")
d.text((W // 2 - 90, 6), "pytest -q  -  Multi-Agent", fill="#cccccc", font=font)

y = 28 + PAD
for line in lines:
    color = "#d4d4d4"
    if "passed" in line and "failed" not in line:
        color = "#5cdb5c"
    elif "failed" in line or "error" in line.lower():
        color = "#f48771"
    elif line.startswith("="):
        color = "#9cdcfe"
    d.text((PAD, y), line, fill=color, font=font)
    y += LINE_H

img.save(HERE / "pytest_output.png")
print(f"Saved {HERE / 'pytest_output.png'}  size={img.size}")
