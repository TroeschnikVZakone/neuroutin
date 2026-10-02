"""Генерирует иконку Neuroutin (build/icon.ico)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SIZE = 256
GOLD = (212, 160, 23, 255)
GOLD_LIGHT = (240, 192, 64, 255)
DARK = (26, 18, 0, 255)

img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

draw.ellipse((8, 8, SIZE - 8, SIZE - 8), fill=GOLD)
draw.ellipse((22, 22, SIZE - 22, SIZE - 22), outline=GOLD_LIGHT, width=5)

font = None
for name in ("arialbd.ttf", "arial.ttf", "segoeuib.ttf"):
    try:
        font = ImageFont.truetype(name, 150)
        break
    except Exception:
        continue
if font is None:
    font = ImageFont.load_default()

text = "N"
bbox = draw.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
x = (SIZE - tw) // 2 - bbox[0]
y = (SIZE - th) // 2 - bbox[1]
draw.text((x, y), text, fill=DARK, font=font)

out = Path(__file__).parent / "build" / "icon.ico"
out.parent.mkdir(exist_ok=True)
img.save(out, format="ICO",
         sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print(f"OK: {out}")