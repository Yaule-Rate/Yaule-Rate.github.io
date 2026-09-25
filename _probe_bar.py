# -*- coding: utf-8 -*-
from PIL import Image
im = Image.open("_shots/v16_bar4.jpg").convert("RGB")
w, h = im.size
# bars 行：前端开发在 y≈4150+156*0.4≈4212（crop offset 4150 + 156/800*400）
# 直接在整图上找：名字 x 106+480=586, y 4150+156=4306
x0, x1 = 480+240, 480+500   # 240 到 500（原图坐标，不超 1000）
y = 4306
row = []
for x in range(x0, x1, 6):
    r, g, b = im.getpixel((x, y))
    row.append("#%02x%02x%02x" % (r, g, b))
# 统计不同颜色
from collections import Counter
cnt = Counter(row)
print("colors at bar line:", cnt.most_common(6))
# 再扫几行
for yy in [4320, 4400, 4460]:
    c2 = Counter(im.getpixel((x, yy)) for x in range(x0, x1, 4))
    print(yy, c2.most_common(4))
