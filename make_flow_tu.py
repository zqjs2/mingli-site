# -*- coding: utf-8 -*-
"""发文章流程图（网页端 GitHub → Cloudflare Pages）"""
from PIL import Image, ImageDraw, ImageFont
import os

S = 2
W, H = 1400, 1000
img = Image.new("RGB", (W*S, H*S), "#F7F3E8")
d = ImageDraw.Draw(img)

F = "C:/Windows/Fonts/msyh.ttc"; FB = "C:/Windows/Fonts/msyhbd.ttc"
def font(sz, bold=False): return ImageFont.truetype(FB if bold else F, sz*S)
INK = "#2B3A3B"; SUB = "#54605F"; GOLD = "#A8833F"; RED = "#8C4B3A"; GREEN = "#5F8168"

def P(s): return [(x*S, y*S) for x, y in s]
def num_badge(cx, cy, n, r=24, fill="#A8833F"):
    d.ellipse([(cx-r)*S, (cy-r)*S, (cx+r)*S, (cy+r)*S], fill=fill)
    ft = font(26, True); t = str(n); w = d.textlength(t, font=ft)
    d.text((cx*S - w/2, (cy - 17)*S), t, font=ft, fill="#FFFFFF")

def step(y, n, title, sub, color="#FAF7EE"):
    d.rounded_rectangle([(80*S), (y*S), (790*S), ((y+104)*S)], radius=14*S, fill=color, outline="#E2DBC8", width=2*S)
    num_badge(124, y+52, n)
    d.text((162*S, (y+16)*S), title, font=font(28, True), fill=INK)
    d.text((162*S, (y+62)*S), sub, font=font(19), fill=SUB)

def arrow(y0, y1):
    x = 435
    d.line([(x*S), (y0*S), (x*S), ((y1-16)*S)], fill="#C6B99B", width=3*S)
    d.polygon(P([(x-9, y1-18), (x+9, y1-18), (x, y1-2)]), fill="#C6B99B")

# 标题
d.text((80*S, 42*S), "发一篇文章的流程", font=font(46, True), fill=INK)
d.text((84*S, 104*S), "网页上改 → 提交 → 自动构建 1–2 分钟 → 线上就是新的", font=font(20), fill=SUB)

steps = [
    ("打开目标目录", "仓库 → docs / 对应栏目，比如 docs/qimen", ),
    ("Add file ▼ → Create new file", "文件名必须带 .md，如 docs/qimen/di4zhang.md"),
    ("第一行写标题，粘贴正文", "# 第四章 标题 —— 记得段与段之间空一行"),
    ("Commit changes… 再点一次", "弹窗里再按一次 Commit changes，才算真提交"),
]
y = 162
for i, (t, s) in enumerate(steps):
    step(y, i+1, t, s)
    if i < 3:
        arrow(y+104, y+140)
    y += 140

# 右侧：四个坑
bx0, by0, bx1, by1 = 850, 162, 1340, 700
d.rounded_rectangle([(bx0*S), (by0*S), (bx1*S), (by1*S)], radius=14*S, fill="#FFFFFF", outline="#E2DBC8", width=2*S)
d.text(((bx0+24)*S, (by0+18)*S), "四个最常见的坑", font=font(24, True), fill=RED)
pit = [
    ("没有 Add file 按钮", "没登录，右上角显示 Sign in"),
    ("提交成功但页面 404", "文件名漏了 .md，或建到了根目录"),
    ("页面能开，菜单里没有", "没进 mkdocs.yml（这条交给助手）"),
    ("图片变链接、点开 404", "路径层级算错，见下方说明"),
]
yy = by0 + 66
for t, s in pit:
    d.text(((bx0+24)*S, yy*S), "×  " + t, font=font(20, True), fill=INK)
    d.text(((bx0+24)*S, (yy+28)*S), s, font=font(16), fill=SUB)
    yy += 76

# 图片路径说明
d.rounded_rectangle([(850*S), (724*S), (1340*S), (858*S)], radius=12*S, fill="#F1EEE0", outline="#E2DBC8", width=2*S)
d.text((870*S, 738*S), "图片路径按“文章所在目录”退级", font=font(18, True), fill=GOLD)
d.text((870*S, 772*S), "docs/qimen/x.md            → ../../assets/a.png", font=font(16), fill=INK)
d.text((870*S, 800*S), "docs/fengshui/xingshi/x.md → ../../../assets/a.png", font=font(16), fill=INK)
d.text((870*S, 828*S), "退多退少一个都不报错，只是图不显示。", font=font(15), fill=SUB)

# 底部：分工
d.rounded_rectangle([(80*S), (742*S), (790*S), (858*S)], radius=12*S, fill="#EDF1EA", outline="#D6E0D3", width=2*S)
d.text((102*S, 758*S), "分工", font=font(20, True), fill=GREEN)
d.text((102*S, 794*S), "你：写、提交（就这两件）", font=font(17), fill=INK)
d.text((102*S, 822*S), "我：拉取、补导航、查图查链、出问题兜底", font=font(17), fill=INK)

# 页脚
d.text((80*S, 906*S), "确认是否已上线：等 1–2 分钟 → 打开 https://zqjs.ziqing.ccwu.cc/对应路径/ → 能打开就是成功", font=font(16), fill=SUB)
d.text((80*S, 940*S), "打不开别慌：先看文件名有没有 .md，再看仓库里那条提交记录在不在。", font=font(16), fill=SUB)

d.rectangle([(0, 0), (W*S-1, H*S-1)], outline="#E3DCC9", width=2*S)
img = img.resize((W, H), Image.LANCZOS)
out = os.path.join(os.path.expanduser("~"), "Desktop", "发文章流程图.png")
img.save(out, optimize=True)
print("saved", out, img.size)


