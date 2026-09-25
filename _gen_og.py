# -*- coding: utf-8 -*-
"""生成 1200x630 青色渐变分享卡片图 og-image.png"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
img = Image.new("RGB", (W, H), "#0284c7")
d = ImageDraw.Draw(img)
# 青色渐变（深到浅）
top = (2, 84, 199)      # #0256c7 深
bottom = (56, 189, 248) # #38bdf8 浅
for y in range(H):
    t = y / H
    r = int(top[0] + (bottom[0] - top[0]) * t)
    g = int(top[1] + (bottom[1] - top[1]) * t)
    b = int(top[2] + (bottom[2] - top[2]) * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# 右上角月亮
cx, cy, cr = W - 170, 150, 70
d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(255, 255, 255, 0))
# 月亮：白圆 + 偏移同色圆抠出月牙
d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(255, 255, 255))
d.ellipse([cx - cr + 38, cy - cr - 16, cx + cr + 38, cy + cr - 16], fill=(56, 189, 248))
# 星星
stars = [(100, 120), (240, 80), (380, 150), (560, 90), (700, 130), (840, 70), (1000, 180), (60, 260), (200, 300), (340, 240)]
for (sx, sy) in stars:
    d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 255, 255))

# 字体：中文字体找系统自带
import os
candidates = [
    "C:/Windows/Fonts/msyh.ttc",      # 微软雅黑
    "C:/Windows/Fonts/simhei.ttf",    # 黑体
    "C:/Windows/Fonts/simsun.ttc",    # 宋体
]
font_path = next((f for f in candidates if os.path.exists(f)), None)
def load(size):
    return ImageFont.truetype(font_path, size) if font_path else ImageFont.load_default()

f_big = load(72)
f_small = load(34)
d.text((90, 170), "Yaule", font=f_big, fill=(255, 255, 255))
d.text((90, 290), "失眠夜空间 · 个人主页", font=f_small, fill=(235, 250, 255))
d.text((90, 360), "咖啡 · 音乐 · 游戏 · 作品", font=f_small, fill=(220, 245, 255))
d.text((90, 470), "https://Yaule-Rate.github.io", font=f_small, fill=(240, 252, 255))

img.save("og-image.png", "PNG")
print("ok og-image.png", img.size)
