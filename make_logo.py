from PIL import Image, ImageDraw, ImageFilter
import os

src = r"G:\mingli-site\docs\assets\logo-raw.png"
out = r"G:\mingli-site\docs\assets\logo.png"
fav = r"G:\mingli-site\docs\assets\favicon.png"

im = Image.open(src).convert("RGBA")
w, h = im.size

# find the disc bounds by trimming near-white border
gray = im.convert("RGB").convert("L")
mask = gray.point(lambda p: 0 if p > 246 else 255)
bbox = mask.getbbox()
if bbox:
    im = im.crop(bbox)
    w, h = im.size

side = min(w, h)
im = im.crop(((w - side) // 2, (h - side) // 2, (w - side) // 2 + side, (h - side) // 2 + side))
im = im.resize((512, 512), Image.LANCZOS)

# circular alpha mask with slightly soft edge
big = 8
m = Image.new("L", (512 * big, 512 * big), 0)
d = ImageDraw.Draw(m)
d.ellipse((0, 0, 512 * big - 1, 512 * big - 1), fill=255)
m = m.resize((512, 512), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.6))

im.putalpha(m)
im.save(out)
im.resize((64, 64), Image.LANCZOS).save(fav)
print("ok", os.path.getsize(out), os.path.getsize(fav))
