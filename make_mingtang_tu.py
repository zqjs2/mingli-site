# -*- coding: utf-8 -*-
"""明堂三格：剖面阶梯示意"""
from PIL import Image, ImageDraw, ImageFont
import math, os

S = 2
W, H = 1600, 920
img = Image.new("RGB", (W*S, H*S), "#F7F3E8")
d = ImageDraw.Draw(img)

F = "C:/Windows/Fonts/msyh.ttc"; FB = "C:/Windows/Fonts/msyhbd.ttc"
def font(sz, bold=False): return ImageFont.truetype(FB if bold else F, sz*S)
INK = "#2B3A3B"; SUB = "#4A5A5B"; GOLD = "#A8833F"; WATER = "#5E8896"

def P(s): return [(x*S, y*S) for x, y in s]
def poly(s, fill, outline=None, width=2):
    d.polygon(P(s), fill=fill)
    if outline: d.line(P(s+[s[0]]), fill=outline, width=width*S, joint="curve")
def line(s, color, width=2):
    d.line(P(s), fill=color, width=width*S, joint="curve")
def dashed(p1, p2, color, width=2, dash=12, gap=9):
    x1, y1 = p1; x2, y2 = p2
    L = math.hypot(x2-x1, y2-y1)
    if L == 0: return
    ux, uy = (x2-x1)/L, (y2-y1)/L
    t = 0
    while t < L:
        b = min(t+dash, L)
        d.line([(x1+ux*t)*S, (y1+uy*t)*S, (x1+ux*b)*S, (y1+uy*b)*S], fill=color, width=width*S)
        t = b+gap
def circle_num(cx, cy, num, r=14):
    d.ellipse([(cx-r)*S, (cy-r)*S, (cx+r)*S, (cy+r)*S], fill="#FFFFFF", outline=GOLD, width=2*S)
    ft = font(18, True); w = d.textlength(str(num), font=ft)
    d.text((cx*S-w/2, (cy-12)*S), str(num), font=ft, fill=INK)
def label(x, y, title, sub="", num=None, anchor="lt"):
    ft = font(25, True); fs = font(15)
    tw = d.textlength(title, font=ft); sw = d.textlength(sub, font=fs) if sub else 0
    x0 = x - (tw if anchor == "rt" else tw/2 if anchor == "ct" else 0)
    pw = max(tw, sw); nw = 26 if num else 0; pad = 13
    if anchor == "rt": bx0, bx1 = x-pw-pad-nw, x+pad
    elif anchor == "ct": bx0, bx1 = x-pw/2-pad, x+pw/2+pad
    else: bx0, bx1 = x0-pad-nw, x0+pw+pad
    d.rounded_rectangle([bx0*S, (y-9)*S, bx1*S, (y+(39 if sub else 30))*S], radius=9*S,
                        fill="#FAF7EE", outline="#E3DCC9", width=2*S)
    d.text((x0*S, y*S), title, font=ft, fill=INK)
    if sub:
        s0 = x-sw if anchor == "rt" else x-sw/2 if anchor == "ct" else x0
        d.text((s0*S, (y+29)*S), sub, font=fs, fill=SUB)
    if num is not None:
        circle_num(x0-20 if anchor != "rt" else x0+tw+22, y+13, num)

BASE = 790     # 剖面底线

# 1) 远景：朝山、案山
poly([(1400, BASE), (1490, 420), (1600, 640), (1600, BASE)], "#DFE5DF", "#CBD5CD", 2)
poly([(1240, BASE), (1290, 600), (1340, 556), (1400, BASE)], "#CBD5CD", "#B5C2B8", 2)

# 2) 剖面台地（一条连续的阶梯线）
stair = [(300, 566), (566, 566), (566, 638), (906, 638), (906, 710), (1252, 710),
         (1252, 756), (1400, 756), (1400, BASE), (300, BASE)]
poly(stair, "#D7E3DA", "#AFC2B4", 2)
# 每级踏面加重，暗示高低
line([(300, 566), (566, 566)], "#8FA699", 5)
line([(566, 638), (906, 638)], "#8FA699", 5)
line([(906, 710), (1252, 710)], "#8FA699", 5)
# 立面
poly([(566, 566), (566, 638), (574, 638), (574, 566)], "#C9D8CD")
poly([(906, 638), (906, 710), (914, 710), (914, 638)], "#C3D3C7")
poly([(1252, 710), (1252, 756), (1260, 756), (1260, 710)], "#BDCEC1")

# 3) 穴山（在台地之后，压住左上）
hill = [(40, BASE), (78, 660), (120, 570), (152, 486), (180, 460), (206, 486),
        (250, 574), (300, 646), (340, BASE)]
poly(hill, "#BFCCC1", "#A6B6AA", 2)
# 落脉
dashed((176, 486), (306, 560), "#92A69A", 3, 14, 9)
# 穴心
d.ellipse([(166*S), (446*S), (196*S), (474*S)], fill="#8C4B3A")

# 4) 龙虎内界（两缕细砂），立在台地边



# 5) 水：沿踏面下泻，从水口出
w = [(330, 566), (470, 568), (560, 570), (572, 642), (700, 644), (900, 646),
     (912, 714), (1050, 716), (1245, 720), (1290, 762), (1318, 800)]
line(w, WATER, 9)
line([(x, y+6) for x, y in w], "#A6C1BE", 2)

# 6) 水口夹砂
poly([(1246, 712), (1296, 748), (1272, 800), (1240, 772)], "#A3B5A8", "#8FA396", 2)
poly([(1352, 760), (1404, 818), (1368, 834), (1330, 806)], "#A3B5A8", "#8FA396", 2)
d.ellipse([(1330*S), (782*S), (1358*S), (808*S)], fill="#CFDCD3", outline="#93A69C", width=2*S)

# 7) 标注
label(288, 486, "小明堂", "贴身小坪，容拜跪", num=1)
label(560, 552, "中明堂", "龙虎之内，宜平正", num=2)
label(898, 618, "大明堂", "案山之内，容万马", num=3)
label(1050, 460, "案山", "穴前近案，如几如案", num=4)
dashed((1200, 530), (1300, 570), "#9FB4A6", 2, 10, 7)
label(1400, 356, "朝山", "远望之山，主气象", num=5)
dashed((1462, 424), (1495, 520), "#C0CEC4", 2, 10, 7)
label(1364, 862, "水口", "众水所出，须关锁", num=6, anchor="ct")

# 8) 说明框
d.rounded_rectangle([(1000*S), (108*S), (1560*S), (296*S)], radius=12*S, fill="#F8F5ED", outline="#E0D9C6", width=2*S)
d.text((1018*S, 124*S), "三格以穴为准，不以大小论贵贱", font=font(19, True), fill=INK)
for i, t in enumerate(["小明堂：穴下贴身，能容拜跪起坐即是",
                       "中明堂：龙虎之内，宜平正、无遮、无水劫",
                       "大明堂：龙虎之外、案山之内，宜开阔容众"]):
    d.text((1018*S, (160+i*34)*S), t, font=font(15), fill=SUB)
d.text((1018*S, (262)*S), "总须内局紧、外局宽", font=font(15), fill="#7D857D")

# 9) 标题、图注
d.text((78*S, 40*S), "明堂三格", font=font(44, True), fill=INK)
d.text((82*S, 96*S), "站在穴上向下看：三层院子一级级放宽，水穿堂而过，从水口出。", font=font(18), fill=SUB)
d.text((78*S, 872*S), "示意图，非实地比例；只讲形势位置，不作吉凶判断。", font=font(15), fill="#7D857D")

d.rectangle([(0, 0), (W*S-1, H*S-1)], outline="#E3DCC9", width=2*S)
img = img.resize((W, H), Image.LANCZOS)
out = "G:/mingli-site/docs/assets/fengshui/mingtang-tu.png"
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, optimize=True)
print("saved", out, img.size)


