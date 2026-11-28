# -*- coding: utf-8 -*-
"""绘制「过峡（束气）细部」示意图"""
from PIL import Image, ImageDraw, ImageFont
import math, os

S = 2
W, H = 1500, 1000
img = Image.new("RGB", (W * S, H * S), "#F7F3E8")
d = ImageDraw.Draw(img)

F = "C:/Windows/Fonts/msyh.ttc"
FB = "C:/Windows/Fonts/msyhbd.ttc"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz * S)

INK = "#2B3A3B"; INK2 = "#4A5A5B"; GOLD = "#A8833F"; WATER = "#6E8E9C"; LEAD = "#8C9C93"; RED = "#8C4B3A"

def P(seq): return [(x * S, y * S) for x, y in seq]
def poly(seq, fill, outline=None, width=2):
    d.polygon(P(seq), fill=fill)
    if outline:
        d.line(P(seq + [seq[0]]), fill=outline, width=width * S, joint="curve")

def hill(apex_x, apex_y, base_y, half_w, color, outline=None, k=1.5):
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

def label(x, y, title, sub="", num=None, anchor="lt", plate=True, color=INK):
    ft = font(29, True); fs = font(19)
    tw = d.textlength(title, font=ft); sw = d.textlength(sub, font=fs) if sub else 0
    x0 = x - (tw if anchor == "rt" else tw / 2 if anchor == "ct" else 0)
    pw = max(tw, sw); nw = 26 if num else 0; pad = 14
    if plate:
        if anchor == "rt":
            bx0, bx1 = x - pw - pad - nw, x + pad
        elif anchor == "ct":
            bx0, bx1 = x - pw / 2 - pad, x + pw / 2 + pad
        else:
            bx0, bx1 = x0 - pad - nw, x0 + pw + pad
        d.rounded_rectangle([bx0 * S, (y - 10) * S, bx1 * S, (y + (52 if sub else 34)) * S],
                            radius=10 * S, fill="#FAF7EE", outline="#E3DCC9", width=2 * S)
    d.text((x0 * S, y * S), title, font=ft, fill=color)
    if sub:
        s0 = x - sw if anchor == "rt" else x - sw / 2 if anchor == "ct" else x0
        d.text((s0 * S, (y + 38) * S), sub, font=fs, fill=INK2)
    if num is not None:
        circle_num(x0 - 22 if anchor != "rt" else x0 + tw + 24, y + 18, num)

# 天空
for i in range(H):
    t = i / H
    d.line([(0, i * S), (W * S, i * S)], fill=(int(247 - 7 * t), int(243 - 6 * t), int(232 - 5 * t)))

# 地面
poly([(0, 880), (W, 880), (W, H), (0, H)], fill="#EFEADA")

# 左：父母山
hill(330, 300, 880, 320, "#B6C2B9", outline="#93A69C", k=1.4)
hill(420, 450, 880, 225, "#B6C2B9", outline="#93A69C", k=1.6)

# 右：穴山（再起之山）
hill(1120, 400, 880, 300, "#AEBAB1", outline="#93A69C", k=1.42)
hill(1030, 520, 880, 200, "#AEBAB1", outline="#93A69C", k=1.65)

# 过峡束气：中间细腰 + 蜂腰鹤膝
poly([(600, 828), (655, 790), (700, 806), (712, 776), (745, 792),
      (790, 810), (800, 866), (740, 848), (712, 830), (688, 850), (648, 848), (610, 860)],
     fill="#A2B1A7", outline="#8FA398")

# 峡中水流（束气处水须绕行）
d.arc([(640) * S, (800) * S, (770) * S, (900) * S], 200, 340, fill=WATER, width=4 * S)
d.arc([(628) * S, (786) * S, (782) * S, (912) * S], 200, 340, fill=WATER, width=2 * S)

# 两侧护砂（小丘，夹护过峡）
hill(560, 800, 890, 95, "#9DAFA3", outline="#7F9387", k=1.9)
hill(845, 792, 890, 90, "#9DAFA3", outline="#7F9387", k=1.9)

# 龙脉虚线：穿过峡心
dashed((330, 330), (620, 780), GOLD, 2, 13, 9)
dashed((620, 780), (712, 800), GOLD, 3, 8, 6)
dashed((712, 800), (1010, 560), GOLD, 2, 13, 9)

# 标注
label(150, 175, "父母山", "来龙一侧，高大开张", num=1)
dashed((330, 340), (420, 320), LEAD)

label(1430, 405, "穴山", "过峡之后重新起顶", num=2, anchor="rt")
dashed((1120, 430), (1180, 420), LEAD)

label(600, 545, "过峡", "两山夹峙，中间细窄=束气", num=3, anchor="rt")
dashed((620, 770), (640, 610), LEAD)

label(700, 600, "蜂腰", "窄到极处，如蜂之腰", num=4, anchor="lt")
dashed((712, 778), (730, 680), LEAD)

label(905, 715, "鹤膝", "峡中两处微隆，如鹤之膝", num=5, anchor="lt")
dashed((775, 800), (880, 730), LEAD)

label(455, 855, "护砂", "两侧小丘夹护，气不外泄", num=6, anchor="ct")
dashed((520, 845), (500, 852), LEAD)

label(1235, 870, "水须绕行", "水从峡外绕，忌直冲峡口", anchor="rt")
dashed((950, 866), (1090, 880), WATER)

# 忌讳小框
box = [(1010, 60), (1460, 320)]
d.rounded_rectangle([(box[0][0]) * S, (box[0][1]) * S, (box[1][0]) * S, (box[1][1]) * S],
                    radius=12 * S, fill="#FBF4ED", outline="#E0C9B8", width=2 * S)
d.text((1035 * S, 78 * S), "峡之三忌", font=font(24, True), fill=RED)
for i, t in enumerate(["一忌凿断：开山取石、挖渠、修路横切",
                       "二忌水冲：溪流直穿峡心，气随水散",
                       "三忌阔大：峡口松散不束，气不收聚"]):
    d.text((1035 * S, (120 + i * 40) * S), t, font=font(19), fill=INK2)

# 标题
d.text((86 * S, 56 * S), "过峡细部", font=font(52, True), fill=INK)
d.text((90 * S, 124 * S), "龙脉行至两山之间，必须收紧成峡，谓之束气；束得住，后面才有气可聚。", font=font(21), fill=INK2)
d.text((86 * S, 962 * S), "示意图，非实地比例；只讲形势位置，不作吉凶判断。", font=font(19), fill="#7D857D")

d.rectangle([(0, 0), (W * S - 1, H * S - 1)], outline="#E3DCC9", width=2 * S)

img = img.resize((W, H), Image.LANCZOS)
out = "G:/mingli-site/docs/assets/fengshui/guoxia-tu.png"
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, optimize=True)
print("saved", out, img.size)
