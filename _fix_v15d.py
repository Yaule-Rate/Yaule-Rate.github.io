# -*- coding: utf-8 -*-
path = "index.html"
html = open(path, encoding="utf-8").read()

# 1. svg 加 width="100%" 属性
old = '<svg id="radarSvg" viewBox="0 0 100 100" role="img" aria-label="技能雷达图"></svg>'
new = '<svg id="radarSvg" viewBox="0 0 100 100" width="100%" role="img" aria-label="技能雷达图"></svg>'
if old in html:
    html = html.replace(old, new, 1); print("svg attr OK")
else:
    print("FAIL svg attr")

# 2. CSS 双保险
old2 = ".radar-box svg { width: 100%; height: auto; display: block; }"
new2 = ".radar-box svg { width: 100% !important; height: auto; display: block; }"
if old2 in html:
    html = html.replace(old2, new2, 1); print("css OK")
else:
    print("FAIL css")

open(path, "w", encoding="utf-8").write(html)
