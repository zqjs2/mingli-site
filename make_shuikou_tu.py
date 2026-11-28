# -*- coding: utf-8 -*-
"""水口示意图：下手砂、罗星、捍门、华表、北辰、禽星"""
from PIL import Image, ImageDraw, ImageFont
import math, os

S = 2
W, H = 1500, 950
img = Image.new("RGB", (W*S, H*S), "#F7F3E8")
d = ImageDraw.Draw(img)

F = "C:/Windows/Fonts/msyh.ttc"; FB = "C:/Windows/Fonts/msyhbd.ttc"
def font(sz, bold=False): return ImageFont.truetype(FB if bold else F, sz*S)
INK = "#2B3A3B"; SUB = "#4A5A5B"; GOLD = "#A8833F"; WATER = "#5E8896"

def P(s): return [(x*S, y*S) for x, y in s]
def poly(s, fill, outline=None, width=2):
    d.polygon(P(s), fill=fill)
    if outline: d.line(P(s+[s[0]]), fill=outline, width=width*S, joint="curve")
def line(s, color, width=2): d.line(P(s), fill=color, width=width*S, joint="curve")
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

# ---- 背景地面
d.rectangle([(0*S), (0*S), (W*S), (H*S)], fill="#F7F3E8")

# ---- 水：自上来，穿过峡口出
river = [(690, 150), (810, 150), (830, 400), (856, 600), (872, 720), (900, 830), (860, 900),
         (700, 900), (656, 830), (636, 720), (628, 600), (652, 400)]
poly(river, "#CFE0DB", "#AAC5BF", 3)
line([(700, 160), (690, 420), (668, 620), (700, 800), (690, 890)], "#7FA8A8", 3)
line([(806, 160), (820, 420), (846, 620), (872, 800), (850, 890)], "#7FA8A8", 3)

# ---- 左侧山（捍门之一）+ 上手砂
poly([(0, 950), (0, 300), (120, 200), (300, 180), (430, 260), (520, 380), (556, 520),
      (560, 700), (520, 790), (430, 850), (300, 900), (120, 950)], "#B3C0B5", "#9AAA9E", 2)
poly([(300, 180), (340, 420), (430, 600), (400, 900), (300, 900)], "#A7B6AB")

# ---- 右侧山（捍门之二）
poly([(1500, 950), (1500, 320), (1380, 210), (1200, 190), (1060, 280), (980, 400),
      (948, 540), (950, 710), (990, 800), (1080, 860), (1200, 910), (1380, 950)], "#B3C0B5", "#9AAA9E", 2)
poly([(1200, 190), (1160, 440), (1070, 610), (1100, 900), (1200, 900)], "#A7B6AB")

# ---- 下手砂：右侧山伸入水口的一段低砂
poly([(950, 706), (900, 690), (868, 726), (896, 760), (946, 742)], "#A9B8AD", "#93A69A", 2)
poly([(950, 712), (918, 706), (896, 726), (918, 744), (950, 736)], "#9FB0A5")

# ---- 峡口：华表（两座石柱）
poly([(640, 720), (664, 650), (700, 660), (700, 726)], "#96A89C", "#83968B", 2)
poly([(838, 726), (842, 660), (876, 650), (900, 720)], "#96A89C", "#83968B", 2)

# ---- 罗星：水口内的小圆丘
d.ellipse([(726*S), (786*S), (816*S), (846*S)], fill="#A2B3A7", outline="#8CA094", width=3*S)
d.arc([(748*S), (800*S), (794*S), (828*S)], 200, 340, fill="#8CA094", width=2*S)

# ---- 北辰：水中特立大石
poly([(700, 706), (760, 700), (782, 730), (770, 758), (712, 760), (692, 736)], "#93A69A", "#80958A", 2)

# ---- 禽星：水口砂上的小石
for (x, y, r) in ((880, 700, 7), (905, 742, 6), (560, 790, 8), (520, 748, 6)):
    d.ellipse([(x-r)*S, (y-r)*S, (x+r)*S, (y+r)*S], fill="#8FA398")

# ---- 标注
label(44, 292, "捍门", "水口两侧特起之山，如门之两扇", num=1)
dashed((300, 236), (170, 300), "#A6B7AB", 2, 10, 7)
label(1456, 300, "捍门", "两山对峙，关锁水口", num=2, anchor="rt")
dashed((1200, 236), (1330, 300), "#A6B7AB", 2, 10, 7)
label(1456, 620, "下手砂", "出水一侧兜收之砂", num=3, anchor="rt")
dashed((948, 700), (1380, 646), "#A6B7AB", 2, 10, 7)
label(1456, 744, "罗星", "水口内突起小丘，如星镇口", num=4, anchor="rt")
dashed((818, 800), (1370, 768), "#A6B7AB", 2, 10, 7)
label(44, 540, "华表", "水口两侧石柱，如门之柱", num=5)
dashed((660, 676), (350, 578), "#A6B7AB", 2, 10, 7)
label(44, 672, "北辰", "水中特立大石，镇口之重", num=6)
dashed((686, 728), (360, 706), "#A6B7AB", 2, 10, 7)
label(44, 830, "禽星", "水口砂上小石，也贵有", num=7)
dashed((556, 790), (350, 852), "#A6B7AB", 2, 10, 7)

# ---- 说明框
d.rounded_rectangle([(950*S), (60*S), (1460*S), (230*S)], radius=12*S, fill="#F8F5ED", outline="#E0D9C6", width=2*S)
d.text((968*S, 76*S), "水口：一地之门户", font=font(19, True), fill=INK)
for i, t in enumerate(["水口者，众水所出之处，古称「天门」",
                       "要关锁：两旁有砂、口内有石，去水曲折",
                       "最忌：水口空阔、直去无收、一望无拦"]):
    d.text((968*S, (112+i*32)*S), t, font=font(15), fill=SUB)

# ---- 标题、图注
d.text((60*S, 40*S), "水口关锁", font=font(42, True), fill=INK)
d.text((64*S, 96*S), "一个地的门户：出水处有没有砂石关拦，直接看出这一局收不收得住。", font=font(17), fill=SUB)
d.text((500*S, 900*S), "示意图，非实地比例；只讲形势位置，不作吉凶判断。", font=font(15), fill="#7D857D")

d.rectangle([(0, 0), (W*S-1, H*S-1)], outline="#E3DCC9", width=2*S)
img = img.resize((W, H), Image.LANCZOS)
out = "G:/mingli-site/docs/assets/fengshui/shuikou-tu.png"
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, optimize=True)
print("saved", out, img.size)

