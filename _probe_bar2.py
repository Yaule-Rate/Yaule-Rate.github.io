# -*- coding: utf-8 -*-
from PIL import Image
from collections import Counter
im = Image.open("_shots/v16_bar5.jpg").convert("RGB")
w, h = im.size
print("size:", w, h)
# 前端开发行名字在 ~(586, 4306)。bar 区域扫描
for y in range(4280, 4360, 5):
    c = Counter(im.getpixel((x, y)) for x in range(720, 990, 3))
    top = c.most_common(3)
    blues = sum(1 for x in range(720, 990, 3) if im.getpixel((x, y))[2] > 180 and im.getpixel((x, y))[0] < 150)
    print(y, top, "blueish:", blues)
