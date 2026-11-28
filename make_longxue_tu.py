# -*- coding: utf-8 -*-
"""绘制「龙穴形势全图」示意：祖山-少祖山-父母山-过峡-胎息-虾须蟹眼-龙虎四势-案山朝山"""
from PIL import Image, ImageDraw, ImageFont
import math, os

S = 2
W, H = 1950, 1200
img = Image.new("RGB", (W * S, H * S), "#F7F3E8")
d = ImageDraw.Draw(img)

F = "C:/Windows/Fonts/msyh.ttc"
FB = "C:/Windows/Fonts/msyhbd.ttc"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz * S)

INK = "#2B3A3B"; INK2 = "#4A5A5B"; GOLD = "#A8833F"; WATER = "#6E8E9C"; LEAD = "#8C9C93"

def P(seq): return [(x * S, y * S) for x, y in seq]

def poly(seq, fill, outline=None, width=2):
    d.polygon(P(seq), fill=fill)
    if outline:
        d.line(P(seq + [seq[0]]), fill=outline, width=width * S, joint="curve")

def hill(apex_x, apex_y, base_y, half_w, color, outline=None, k=1.55, skew=0.0):
    left, right = [], []
    n = 64
    for i in range(n + 1):
        t = i / n
        yr = apex_y + (base_y - apex_y) * (t ** k)
        xr = apex_x + half_w * t
        right.append((xr + skew * (base_y - yr), yr))
        left.append((apex_x - half_w * t + skew * (base_y - yr), yr))
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

def label(x, y, title, sub="", num=None, anchor="lt", plate=False):
    ft = font(30, True); fs = font(19)
    tw = d.textlength(title, font=ft); sw = d.textlength(sub, font=fs) if sub else 0
    x0 = x - (tw if anchor == "rt" else tw / 2 if anchor == "ct" else 0)
    y0 = y - (32 if anchor == "cb" else 0)
    pw = max(tw, sw)
    if plate:
        pad = 14
        nw = 26 if num else 0
        if anchor == "rt":
            bx0 = x - pw - pad - nw
            bx1 = x + pad
        elif anchor == "ct":
            bx0 = x - pw / 2 - pad
            bx1 = x + pw / 2 + pad
        else:
            bx0 = x0 - pad - nw
            bx1 = x0 + pw + pad
        d.rounded_rectangle([bx0 * S, (y0 - 10) * S, bx1 * S, (y0 + (52 if sub else 34)) * S],
                            radius=10 * S, fill="#FAF7EE", outline="#E3DCC9", width=2 * S)
    d.text((x0 * S, y0 * S), title, font=ft, fill=INK)
    if sub:
        if anchor == "rt":
            s0 = x - sw
        elif anchor == "ct":
            s0 = x - sw / 2
        else:
            s0 = x0
        d.text((s0 * S, (y0 + 38) * S), sub, font=fs, fill=INK2)
    if num is not None:
        circle_num(x0 - 22 if anchor != "rt" else x0 + tw + 24, y0 + 18, num)

# 天空
for i in range(H):
    t = i / H
    d.line([(0, i * S), (W * S, i * S)], fill=(int(247 - 7 * t), int(243 - 6 * t), int(232 - 5 * t)))

# 远山：朝山
hill(1800, 520, 940, 240, "#E6EAE1", k=1.45)
hill(1695, 610, 940, 170, "#E1E7DD", k=1.6)

# 案山
hill(1520, 760, 950, 165, "#D3DBCF", k=1.9)
hill(1595, 790, 950, 125, "#CCD5C8", k=2.0)

# 地面
poly([(0, 940), (W, 940), (W, H), (0, H)], fill="#EFEADA")

# 明堂（穴前平展 + 浅水）
d.ellipse([(1150) * S, (872) * S, (1420) * S, (944) * S], fill="#DCE6E0")
d.line([(1160) * S, (908) * S, (1410) * S, (908) * S], fill=WATER, width=2 * S)

# 祖山
hill(330, 300, 940, 330, "#C8D2CB", outline="#AEBCB4", k=1.3)
hill(420, 430, 940, 235, "#C8D2CB", outline="#AEBCB4", k=1.55)

# 少祖山
hill(700, 440, 940, 285, "#BEC9C2", outline="#A5B4AC", k=1.38)
hill(790, 560, 940, 205, "#BEC9C2", outline="#A5B4AC", k=1.6)

# 父母山
hill(1030, 560, 950, 285, "#B2BFB6", outline="#93A69C", k=1.45)
hill(1115, 665, 950, 190, "#B2BFB6", outline="#93A69C", k=1.68)

# 过峡（细腰束气）
poly([(1130, 712), (1178, 700), (1225, 718), (1225, 806), (1178, 778), (1130, 800)],
     fill="#A9B7AE", outline="#8FA398")

# 穴山 + 胎息
hill(1295, 700, 950, 180, "#A4B3A9", outline="#8FA398", k=1.32)
d.ellipse([(1258) * S, (714) * S, (1332) * S, (775) * S], fill="#9AA9A0", outline="#8FA398", width=2 * S)
d.ellipse([(1288) * S, (727) * S, (1302) * S, (741) * S], fill="#8C4B3A")

# 龙虎砂手：左右各一道内抱的砂
poly([(1085, 928), (1185, 944), (1275, 972), (1275, 998), (1170, 968), (1078, 952)],
     fill="#98A99E", outline="#7F9387")
poly([(1325, 972), (1415, 946), (1455, 968), (1425, 990), (1330, 998)],
     fill="#98A99E", outline="#7F9387")

# 虾须蟹眼
for cx, a1, a2 in ((1272, 200, 20), (1322, 340, 160)):
    d.arc([(cx - 18) * S, (748) * S, (cx + 18) * S, (812) * S], a1, a2, fill=WATER, width=3 * S)
d.ellipse([(1264) * S, (758) * S, (1278) * S, (772) * S], fill=WATER)
d.ellipse([(1316) * S, (758) * S, (1330) * S, (772) * S], fill=WATER)

# 龙脉虚线
for a, b in (((330, 315), (700, 455)), ((700, 455), (1030, 575)), ((1030, 575), (1178, 712)), ((1178, 712), (1295, 740))):
    dashed(a, b, GOLD, 2, 13, 9)

# ---- 标注 ----
label(215, 190, "祖山", "龙脉发源，最高最远，一派之根", num=1, plate=True)
dashed((330, 330), (470, 320), LEAD)

label(560, 348, "少祖山", "分枝换骨，第二次起顶", num=2, plate=True)
dashed((700, 470), (690, 405), LEAD)

label(855, 462, "父母山", "穴后贴身靠山，落脉结穴", num=3, plate=True)
dashed((1030, 585), (1005, 528), LEAD)

label(935, 690, "过峡", "束气细腰，龙脉收紧再起", num=6, plate=True)
dashed((1178, 752), (1150, 715), LEAD)

label(1495, 600, "胎息孕育", "落脉处微隆起，如胎之息", num=4, anchor="rt", plate=True)
dashed((1332, 750), (1470, 660), LEAD)

label(1330, 840, "虾须蟹眼", "细砂如虾须，两水交为蟹眼", num=5, plate=True)
dashed((1315, 775), (1360, 800), LEAD)

label(1095, 1010, "青龙", "左砂内抱", num=7, plate=True)
label(1405, 1010, "白虎", "右砂内抱", num=8, plate=True)
label(1300, 966, "明堂", "", anchor="ct", plate=True)

label(1660, 700, "案山", "近而低，关拦堂气", num=9, anchor="rt", plate=True)
dashed((1525, 782), (1600, 745), LEAD)

label(1862, 468, "朝山", "远而高，朝揖有情", anchor="rt", plate=True)
dashed((1800, 545), (1830, 520), LEAD)

# 标题
d.text((90 * S, 58 * S), "龙穴形势全图", font=font(54, True), fill=INK)
d.text((94 * S, 128 * S), "自祖山发脉，经少祖、父母，过峡束气，胎息结穴；两砂内抱成明堂，近案远朝以关堂气。",
       font=font(22), fill=INK2)
d.text((90 * S, 1120 * S), "示意图，非实地比例；只讲形势位置，不作吉凶判断。", font=font(20), fill="#7D857D")

d.rectangle([(0, 0), (W * S - 1, H * S - 1)], outline="#E3DCC9", width=2 * S)

img = img.resize((W, H), Image.LANCZOS)
out = "G:/mingli-site/docs/assets/fengshui/longxue-tu.png"
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, optimize=True)
print("saved", out, img.size)
