# -*- coding: utf-8 -*-
"""绘制「穴之微形凭证」细部示意图：球檐、太极晕、蝉翼、虾须、蟹眼、氊唇、界水、明堂"""
from PIL import Image, ImageDraw, ImageFont
import math, os

S = 2
W, H = 1500, 1050
CX = 700                     # 穴心横坐标
img = Image.new("RGB", (W * S, H * S), "#F7F3E8")
d = ImageDraw.Draw(img)

F = "C:/Windows/Fonts/msyh.ttc"
FB = "C:/Windows/Fonts/msyhbd.ttc"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz * S)

INK = "#2B3A3B"; INK2 = "#4A5A5B"; GOLD = "#A8833F"; WATER = "#6E8E9C"; LEAD = "#8C9C93"; SAND = "#6F8479"

def P(seq): return [(x * S, y * S) for x, y in seq]
def poly(seq, fill, outline=None, width=2):
    d.polygon(P(seq), fill=fill)
    if outline:
        d.line(P(seq + [seq[0]]), fill=outline, width=width * S, joint="curve")

def hill(apex_x, apex_y, base_y, half_w, color, outline=None, k=1.6):
    left, right = [], []
    n = 64
    for i in range(n + 1):
        t = i / n
        yr = apex_y + (base_y - apex_y) * (t ** k)
        right.append((apex_x + half_w * t, yr))
        left.append((apex_x - half_w * t, yr))
    poly(list(reversed(left)) + right, color, outline)

def dashed(p1, p2, color, width=2, dash=12, gap=8):
    x1, y1 = p1; x2, y2 = p2
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0: return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0
    while t < L:
        b = min(t + dash, L)
        d.line([(x1 + ux * t) * S, (y1 + uy * t) * S, (x1 + ux * b) * S, (y1 + uy * b) * S],
               fill=color, width=width * S)
        t = b + gap

def circle_num(cx, cy, num, r=15):
    d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S],
              fill="#FFFFFF", outline=GOLD, width=2 * S)
    ft = font(19, True)
    w = d.textlength(str(num), font=ft)
    d.text((cx * S - w / 2, (cy - 13) * S), str(num), font=ft, fill=INK)

def label(x, y, title, sub="", num=None, anchor="lt", color=INK):
    ft = font(28, True); fs = font(18)
    tw = d.textlength(title, font=ft); sw = d.textlength(sub, font=fs) if sub else 0
    x0 = x - (tw if anchor == "rt" else tw / 2 if anchor == "ct" else 0)
    pw = max(tw, sw); nw = 26 if num else 0; pad = 14
    if anchor == "rt":
        bx0, bx1 = x - pw - pad - nw, x + pad
    elif anchor == "ct":
        bx0, bx1 = x - pw / 2 - pad, x + pw / 2 + pad
    else:
        bx0, bx1 = x0 - pad - nw, x0 + pw + pad
    d.rounded_rectangle([bx0 * S, (y - 10) * S, bx1 * S, (y + (50 if sub else 34)) * S],
                        radius=10 * S, fill="#FAF7EE", outline="#E3DCC9", width=2 * S)
    d.text((x0 * S, y * S), title, font=ft, fill=color)
    if sub:
        s0 = x - sw if anchor == "rt" else x - sw / 2 if anchor == "ct" else x0
        d.text((s0 * S, (y + 36) * S), sub, font=fs, fill=INK2)
    if num is not None:
        circle_num(x0 - 22 if anchor != "rt" else x0 + tw + 24, y + 17, num)

# 天空
for i in range(H):
    t = i / H
    d.line([(0, i * S), (W * S, i * S)], fill=(int(247 - 7 * t), int(243 - 6 * t), int(232 - 5 * t)))

# 明堂
poly([(0, 880), (W, 880), (W, H), (0, H)], fill="#EFEADA")
d.ellipse([(380) * S, (878) * S, (1020) * S, (975) * S], fill="#DCE6E0")
d.line([(400) * S, (920) * S, (1000) * S, (920) * S], fill=WATER, width=2 * S)

# 穴山
hill(CX, 400, 880, 320, "#AEBAB1", outline="#8FA398", k=1.5)
hill(CX, 432, 880, 245, "#A6B3AA", outline="#8FA398", k=1.65)

# 球檐
d.ellipse([(CX - 60) * S, (416) * S, (CX + 60) * S, (460) * S], fill="#9DAFA3", outline="#8FA398", width=2 * S)

# 太极晕
cy = 522
for r, col in ((64, "#BCC8BF"), (47, "#AFBBB2"), (30, "#A2B1A7")):
    d.ellipse([(CX - r) * S, (cy - r * 0.8) * S, (CX + r) * S, (cy + r * 0.8) * S], outline=col, width=2 * S)
d.ellipse([(CX - 12) * S, (cy - 10) * S, (CX + 12) * S, (cy + 10) * S], fill="#8C4B3A")

# 蝉翼（两肩薄砂）
d.arc([(CX - 160) * S, (cy - 55) * S, (CX - 60) * S, (cy + 30) * S], 300, 20, fill=SAND, width=4 * S)
d.arc([(CX + 60) * S, (cy - 55) * S, (CX + 160) * S, (cy + 30) * S], 160, 240, fill=SAND, width=4 * S)

# 虾须（两缕细砂，内曲抱穴）
for sgn in (-1, 1):
    pts, pts2 = [], []
    for i in range(26):
        t = i / 25
        x = CX + sgn * (60 + 55 * t) + sgn * 18 * math.sin(math.pi * t)
        y = cy + 16 + 86 * t
        pts.append((x, y)); pts2.append((x + sgn * 9, y + 5))
    d.line(P(pts), fill=SAND, width=4 * S)
    d.line(P(pts2), fill="#93A69C", width=2 * S)

# 蟹眼
d.ellipse([(CX - 62) * S, (634) * S, (CX - 24) * S, (668) * S], fill="#CFDEDA", outline=WATER, width=2 * S)
d.ellipse([(CX + 24) * S, (634) * S, (CX + 62) * S, (668) * S], fill="#CFDEDA", outline=WATER, width=2 * S)

# 界水
dashed((CX - 60, 670), (CX - 130, 730), WATER, 2, 10, 7)
dashed((CX + 60, 670), (CX + 130, 730), WATER, 2, 10, 7)

# 氊唇
d.rounded_rectangle([(CX - 92) * S, (694) * S, (CX + 92) * S, (736) * S], radius=20 * S,
                    fill="#B8C4BB", outline="#93A69C", width=2 * S)

# 标注
label(452, 350, "球檐", "穴上圆顶，如覆球之檐", num=1, anchor="rt")
dashed((CX - 20, 438), (560, 412), LEAD)

label(1150, 440, "太极晕", "穴心同心圆晕", num=2, anchor="rt")
dashed((CX + 66, 520), (1140, 470), LEAD)

label(452, 512, "蝉翼", "两肩薄砂，如蝉之翼", num=3, anchor="rt")
dashed((CX - 150, 512), (520, 512), LEAD)

label(452, 620, "虾须", "穴旁细砂内曲抱穴", num=4, anchor="rt")
dashed((CX - 95, 600), (520, 632), LEAD)

label(1075, 600, "蟹眼", "两水交会的小圆窝", num=5)
dashed((CX + 62, 652), (1055, 610), LEAD)

label(1075, 690, "氊唇", "穴下余气平吐如唇", num=6)
dashed((CX + 92, 716), (1055, 700), LEAD)

label(430, 780, "界水", "分流界线，界断内外", num=7, anchor="ct")
dashed((CX - 130, 730), (470, 760), WATER)

label(700, 936, "明堂", "", anchor="ct")

# 右侧说明框
box = [(1040, 60), (1462, 330)]
d.rounded_rectangle([(box[0][0]) * S, (box[0][1]) * S, (box[1][0]) * S, (box[1][1]) * S],
                    radius=12 * S, fill="#F7F4EC", outline="#E0D9C6", width=2 * S)
d.text((1062 * S, 78 * S), "穴形四格：窝 · 钳 · 乳 · 突", font=font(22, True), fill=INK)
for i, t in enumerate(["窝：穴心微凹，四围略高，如掌心",
                       "钳：两臂张开如钳，中藏一穴",
                       "乳：脉直下垂，如乳之垂",
                       "突：平地微起一突，气聚于顶",
                       "四格之外，又有盖、撞、倚、并诸法"]):
    d.text((1062 * S, (120 + i * 38) * S), t, font=font(17), fill=INK2)

# 标题
d.text((86 * S, 56 * S), "穴之微形", font=font(50, True), fill=INK)
d.text((90 * S, 120 * S), "穴不靠感觉找，靠几处可以指认的微形：球檐、太极晕、蝉翼、虾须、蟹眼、氊唇、界水。", font=font(20), fill=INK2)
d.text((86 * S, 1005 * S), "示意图，非实地比例；只讲形势位置，不作吉凶判断。", font=font(18), fill="#7D857D")

d.rectangle([(0, 0), (W * S - 1, H * S - 1)], outline="#E3DCC9", width=2 * S)

img = img.resize((W, H), Image.LANCZOS)
out = "G:/mingli-site/docs/assets/fengshui/xuexing-tu.png"
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, optimize=True)
print("saved", out, img.size)

